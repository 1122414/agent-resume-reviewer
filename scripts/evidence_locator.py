#!/usr/bin/env python3
"""Rank local repository files that may support a resume claim."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


CONCEPTS: dict[str, tuple[str, ...]] = {
    "planning": (
        "planner",
        "planning",
        "plan_step",
        "task_graph",
        "action_proposal",
        "计划",
        "规划",
    ),
    "execution": (
        "executor",
        "execute_action",
        "action_handler",
        "dispatch",
        "tool_call",
        "执行器",
        "工具调用",
    ),
    "replan": (
        "replan",
        "re-plan",
        "planner_reentry",
        "retry_after_validation",
        "validation_failure",
        "strategy_retry",
        "recover",
        "recovery",
        "重新规划",
        "异常触发",
    ),
    "verification": (
        "verifier",
        "verify",
        "validator",
        "validation",
        "evidence_check",
        "critic",
        "assertion",
        "验证",
        "校验",
    ),
    "state": (
        "state",
        "checkpoint",
        "snapshot",
        "resume_token",
        "event_log",
        "persistence",
        "durable",
        "状态",
        "检查点",
    ),
    "memory-context": (
        "memory",
        "history_buffer",
        "vector_store",
        "retrieval",
        "context",
        "conversation_state",
        "记忆",
        "上下文",
    ),
    "observation": (
        "observation",
        "freshness",
        "stale",
        "ttl",
        "version_check",
        "environment_state",
        "观察",
        "新鲜度",
    ),
    "orchestration": (
        "orchestrator",
        "orchestration",
        "workflow",
        "state_machine",
        "router",
        "scheduler",
        "runtime",
        "编排",
        "运行时",
    ),
    "evaluation": (
        "evaluation",
        "eval",
        "benchmark",
        "success_rate",
        "failure_label",
        "regression",
        "golden_set",
        "评测",
        "基准",
        "成功率",
    ),
    "tracing-replay": (
        "trace",
        "tracing",
        "span",
        "telemetry",
        "trajectory",
        "replay",
        "audit_log",
        "追踪",
        "回放",
    ),
    "safety-permissions": (
        "permission",
        "policy",
        "allowlist",
        "sandbox",
        "guardrail",
        "authorization",
        "权限",
        "安全",
    ),
    "multi-agent": (
        "multi_agent",
        "multi-agent",
        "supervisor",
        "handoff",
        "agent_role",
        "shared_state",
        "多智能体",
        "多代理",
    ),
}

TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".md",
    ".php",
    ".proto",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

PRIORITY_DIRS = {
    "agent",
    "agents",
    "benchmark",
    "benchmarks",
    "docs",
    "eval",
    "evals",
    "executor",
    "memory",
    "orchestrator",
    "planner",
    "runtime",
    "src",
    "test",
    "tests",
}

STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "before",
    "agent",
    "agents",
    "are",
    "because",
    "build",
    "built",
    "can",
    "create",
    "created",
    "design",
    "designed",
    "develop",
    "developed",
    "for",
    "from",
    "have",
    "how",
    "implement",
    "implemented",
    "into",
    "its",
    "that",
    "the",
    "their",
    "this",
    "system",
    "using",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
    "构建",
    "设计",
    "实现",
    "系统",
}


@dataclass
class Candidate:
    path: str
    score: float
    matched_concepts: list[str]
    matched_terms: list[str]
    snippets: list[dict[str, object]]


def repository_revision(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def activated_concepts(claim: str) -> list[str]:
    lowered = claim.casefold()
    return [
        name
        for name, aliases in CONCEPTS.items()
        if any(alias.casefold() in lowered for alias in aliases)
    ]


def claim_tokens(claim: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}|[\u4e00-\u9fff]{2,}", claim)
    return sorted(
        {
            token.casefold()
            for token in tokens
            if token.casefold() not in STOPWORDS
        }
    )


def iter_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(repo).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue
        if path.suffix.casefold() not in TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue
        yield path


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []


def count_occurrences(text: str, term: str) -> int:
    if re.fullmatch(r"[a-z0-9_-]+", term):
        pattern = rf"(?<![a-z0-9_-]){re.escape(term)}(?![a-z0-9_-])"
        return len(re.findall(pattern, text))
    return text.count(term)


def rank_file(
    repo: Path,
    path: Path,
    active: list[str],
    direct_tokens: list[str],
) -> Candidate | None:
    relative = path.relative_to(repo).as_posix()
    path_text = relative.casefold()
    lines = read_lines(path)
    if not lines:
        return None
    content = "\n".join(lines).casefold()

    matched_concepts: list[str] = []
    matched_terms: set[str] = set()
    score = 0.0
    snippets: list[dict[str, object]] = []

    for concept in active:
        aliases = CONCEPTS[concept]
        concept_hit = False
        for alias in aliases:
            term = alias.casefold()
            path_hits = count_occurrences(path_text, term)
            content_hits = count_occurrences(content, term)
            if path_hits or content_hits:
                concept_hit = True
                matched_terms.add(alias)
                score += min(path_hits, 2) * 4.0
                score += min(content_hits, 8) * 1.0
        if concept_hit:
            matched_concepts.append(concept)

    for token in direct_tokens:
        path_hits = count_occurrences(path_text, token)
        content_hits = count_occurrences(content, token)
        if path_hits or content_hits:
            matched_terms.add(token)
            score += min(path_hits, 2) * 2.0
            score += min(content_hits, 5) * 0.5

    if not matched_terms:
        return None

    if any(part.casefold() in PRIORITY_DIRS for part in path.relative_to(repo).parts):
        score += 2.0
    if any(part.casefold() in {"test", "tests", "eval", "evals", "benchmarks"} for part in path.relative_to(repo).parts):
        score += 1.0

    terms_for_snippets = sorted(
        {term.casefold() for term in matched_terms}, key=len, reverse=True
    )
    for number, line in enumerate(lines, start=1):
        lowered = line.casefold()
        hits = [term for term in terms_for_snippets if term in lowered]
        if hits:
            snippets.append(
                {
                    "line": number,
                    "text": line.strip()[:240],
                    "matched_terms": hits[:5],
                }
            )
            if len(snippets) == 3:
                break

    return Candidate(
        path=relative,
        score=round(score, 2),
        matched_concepts=sorted(matched_concepts),
        matched_terms=sorted(matched_terms),
        snippets=snippets,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rank repository files that may contain evidence for a resume claim. "
            "Candidates require human or agent inspection before verification."
        )
    )
    parser.add_argument("--repo", type=Path, required=True, help="Local repo path")
    parser.add_argument("--claim", required=True, help="Resume claim to locate")
    parser.add_argument("--max-results", type=int, default=15)
    parser.add_argument(
        "--min-score", type=float, default=1.0, help="Minimum candidate score"
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.is_dir():
        parser.error(f"repository path is not a directory: {repo}")
    if args.max_results < 1:
        parser.error("--max-results must be at least 1")

    active = activated_concepts(args.claim)
    tokens = claim_tokens(args.claim)
    candidates = [
        candidate
        for path in iter_files(repo)
        if (
            candidate := rank_file(repo, path, active, tokens)
        )
        and candidate.score >= args.min_score
    ]
    candidates.sort(key=lambda item: (-item.score, item.path))

    output = {
        "repo": str(repo),
        "revision": repository_revision(repo),
        "claim": args.claim,
        "activated_concepts": active,
        "direct_tokens": tokens,
        "notice": (
            "These are search candidates, not verified evidence. "
            "Inspect behavior and claim alignment before assigning status."
        ),
        "candidates": [
            asdict(candidate) for candidate in candidates[: args.max_results]
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
