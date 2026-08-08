#!/usr/bin/env python3
"""Validate a Claim-Evidence Ledger and its cross-references."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: jsonschema. Install it with: python -m pip install jsonschema"
    ) from exc


def format_path(parts: list[object]) -> str:
    if not parts:
        return "$"
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def duplicate_ids(items: list[dict], key: str) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        value = item[key]
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def cross_reference_errors(data: dict) -> list[str]:
    errors: list[str] = []
    source_items = {
        item["source_id"]: item for item in data["evidence_sources"]
    }
    sources = set(source_items)
    claims = {item["claim_id"] for item in data["claims"]}
    projects = {item["project_id"] for item in data["projects"]}
    requirements = {item["requirement_id"] for item in data["jd_requirements"]}

    if data["stage"] != "ingested" and not data["claims"]:
        errors.append(f"stage {data['stage']} requires at least one claim")

    for items, key, label in (
        (data["evidence_sources"], "source_id", "evidence source"),
        (data["claims"], "claim_id", "claim"),
        (data["projects"], "project_id", "project"),
        (data["jd_requirements"], "requirement_id", "JD requirement"),
    ):
        for value in sorted(duplicate_ids(items, key)):
            errors.append(f"duplicate {label} id: {value}")

    for claim in data["claims"]:
        project_id = claim["project_id"]
        if project_id is not None and project_id not in projects:
            errors.append(
                f"claim {claim['claim_id']} references unknown project {project_id}"
            )
        for ref in claim["evidence_refs"]:
            if ref["source_id"] not in sources:
                errors.append(
                    f"claim {claim['claim_id']} references unknown source "
                    f"{ref['source_id']}"
                )
        if project_id is not None and project_id in projects:
            project = next(
                item for item in data["projects"] if item["project_id"] == project_id
            )
            if claim["claim_id"] not in project["claim_ids"]:
                errors.append(
                    f"claim {claim['claim_id']} is missing from project "
                    f"{project_id} claim_ids"
                )

        direct_refs = [
            ref
            for ref in claim["evidence_refs"]
            if ref["source_id"] in source_items
            and source_items[ref["source_id"]]["inspected"]
            and source_items[ref["source_id"]]["level"] in {"L3", "L4"}
            and ref["relation"] in {"SUPPORTS", "PARTIALLY_SUPPORTS"}
        ]
        if claim["status"] == "VERIFIED" and not any(
            ref["relation"] == "SUPPORTS" for ref in direct_refs
        ):
            errors.append(
                f"claim {claim['claim_id']} is VERIFIED without inspected "
                "L3/L4 supporting evidence"
            )
        if claim["status"] == "PARTIALLY_VERIFIED" and not direct_refs:
            errors.append(
                f"claim {claim['claim_id']} is PARTIALLY_VERIFIED without "
                "inspected L3/L4 evidence"
            )
        if claim["status"] == "SUPPORTED" and not any(
            ref["relation"] == "SUPPORTS" for ref in claim["evidence_refs"]
        ):
            errors.append(
                f"claim {claim['claim_id']} is SUPPORTED without a supporting "
                "evidence relationship"
            )
        if claim["status"] == "CONTRADICTED":
            if not claim["contradictions"]:
                errors.append(
                    f"claim {claim['claim_id']} is CONTRADICTED without a reason"
                )
            if not any(
                ref["relation"] == "CONTRADICTS"
                for ref in claim["evidence_refs"]
            ):
                errors.append(
                    f"claim {claim['claim_id']} is CONTRADICTED without a "
                    "contradicting evidence relationship"
                )
        if claim["status"] == "UNVERIFIED" and not (
            claim["missing_evidence"]
            or any(
                ref["relation"] in {"NOT_FOUND", "INACCESSIBLE"}
                for ref in claim["evidence_refs"]
            )
        ):
            errors.append(
                f"claim {claim['claim_id']} is UNVERIFIED without a search "
                "failure or missing-evidence note"
            )

    for source in data["evidence_sources"]:
        start = source["line_start"]
        end = source["line_end"]
        if start is not None and end is not None and end < start:
            errors.append(
                f"source {source['source_id']} line_end precedes line_start"
            )

    for project in data["projects"]:
        for claim_id in project["claim_ids"]:
            if claim_id not in claims:
                errors.append(
                    f"project {project['project_id']} references unknown claim {claim_id}"
                )
            else:
                claim = next(
                    item for item in data["claims"] if item["claim_id"] == claim_id
                )
                if claim["project_id"] != project["project_id"]:
                    errors.append(
                        f"project {project['project_id']} includes claim {claim_id} "
                        f"owned by project {claim['project_id']}"
                    )
        for component in project["architecture"]:
            for source_id in component["evidence_source_ids"]:
                if source_id not in sources:
                    errors.append(
                        f"project {project['project_id']} architecture references "
                        f"unknown source {source_id}"
                    )
        value = project["value"]
        if value is not None:
            expected = 20 * (
                0.25 * value["technical_depth"]
                + 0.20 * value["ownership"]
                + 0.25 * value["target_relevance"]
                + 0.20 * value["evidence_strength"]
                + 0.10 * value["differentiation"]
            )
            if not math.isclose(value["score"], expected, abs_tol=0.11):
                errors.append(
                    f"project {project['project_id']} value score is {value['score']}, "
                    f"expected {expected:.1f}"
                )
            expected_recommendation = (
                "MUST_KEEP"
                if value["score"] >= 80
                else "KEEP"
                if value["score"] >= 65
                else "OPTIONAL"
                if value["score"] >= 45
                else "REMOVE"
            )
            if (
                value["recommendation"] != expected_recommendation
                and not value["override_reason"]
            ):
                errors.append(
                    f"project {project['project_id']} recommendation is "
                    f"{value['recommendation']}, expected {expected_recommendation}; "
                    "provide override_reason"
                )

    for requirement in data["jd_requirements"]:
        for claim_id in requirement["evidence_claim_ids"]:
            if claim_id not in claims:
                errors.append(
                    f"JD requirement {requirement['requirement_id']} references "
                    f"unknown claim {claim_id}"
                )

    if data["inputs"]["job_description"] is None and requirements:
        errors.append("JD requirements must be empty when job_description is null")

    scores = data["scores"]
    if scores is not None:
        category_keys = [item["key"] for item in scores["categories"]]
        if len(category_keys) != len(set(category_keys)):
            errors.append("score category keys must be unique")

        raw_total = sum(item["score"] for item in scores["categories"])
        max_total = sum(item["max"] for item in scores["categories"])
        normalized = 100 * raw_total / max_total
        if not math.isclose(scores["raw_total"], raw_total, abs_tol=0.01):
            errors.append(
                f"raw_total is {scores['raw_total']}, expected {raw_total:.2f}"
            )
        if not math.isclose(scores["max_total"], max_total, abs_tol=0.01):
            errors.append(
                f"max_total is {scores['max_total']}, expected {max_total:.2f}"
            )
        if not math.isclose(
            scores["normalized_total"], normalized, abs_tol=0.11
        ):
            errors.append(
                f"normalized_total is {scores['normalized_total']}, "
                f"expected {normalized:.1f}"
            )

        has_jd = data["inputs"]["job_description"] is not None
        has_jd_category = "jd-match-ats" in category_keys
        if has_jd != has_jd_category:
            expectation = "present" if has_jd else "absent"
            errors.append(
                f"jd-match-ats category must be {expectation} for this input set"
            )

        expected_categories = {
            "technical-credibility": 20,
            "agent-architecture-depth": 20,
            "engineering-difficulty": 15,
            "ownership": 15,
            "measurable-impact": 10,
            "technical-communication": 10,
            "structure-readability": 5,
        }
        if has_jd:
            expected_categories["jd-match-ats"] = 5
        actual_categories = {
            item["key"]: item["max"] for item in scores["categories"]
        }
        if set(actual_categories) != set(expected_categories):
            missing = sorted(set(expected_categories) - set(actual_categories))
            extra = sorted(set(actual_categories) - set(expected_categories))
            errors.append(
                f"score categories mismatch; missing={missing}, extra={extra}"
            )
        for key in set(actual_categories) & set(expected_categories):
            if actual_categories[key] != expected_categories[key]:
                errors.append(
                    f"score category {key} max is {actual_categories[key]}, "
                    f"expected {expected_categories[key]}"
                )

        for category in scores["categories"]:
            if category["score"] > category["max"]:
                errors.append(
                    f"score {category['key']} exceeds max "
                    f"({category['score']} > {category['max']})"
                )
            for claim_id in category["evidence_claim_ids"]:
                if claim_id not in claims:
                    errors.append(
                        f"score {category['key']} references unknown claim {claim_id}"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an agent-resume-reviewer Claim-Evidence Ledger."
    )
    parser.add_argument(
        "ledger", help="Path to ledger JSON, or - to read JSON from stdin"
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "schemas"
        / "claim-evidence-ledger.schema.json",
        help="Path to JSON Schema",
    )
    args = parser.parse_args()

    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        ledger_label = "<stdin>" if args.ledger == "-" else args.ledger
        ledger_text = (
            sys.stdin.read()
            if args.ledger == "-"
            else Path(args.ledger).read_text(encoding="utf-8")
        )
        data = json.loads(ledger_text)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    errors = [
        f"{format_path(list(error.path))}: {error.message}"
        for error in schema_errors
    ]
    if not schema_errors:
        errors.extend(cross_reference_errors(data))

    if errors:
        print(f"INVALID: {ledger_label}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"VALID: {ledger_label} "
        f"({len(data['claims'])} claims, {len(data['evidence_sources'])} sources)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
