"""Audit manual_insert_questions.QUESTIONS for structural issues and obvious mismatches.

This script is intentionally conservative: it only flags issues it can detect reliably
(e.g. invalid correct letter, wrong option count, comment strongly implying a different
correct option).

Run:
  python3 audit_questions.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable


LETTERS = "ABCDE"


@dataclass(frozen=True)
class Finding:
    idx: int
    severity: str  # "ERROR" | "WARN"
    code: str
    message: str


def _letter_to_index(letter: str) -> int | None:
    if not isinstance(letter, str):
        return None
    letter = letter.strip().upper()
    if letter in LETTERS:
        return LETTERS.index(letter)
    return None


def _norm(s: str) -> str:
    return s.casefold().strip()


def _iter_option_mentions(comment: str, options: list[str]) -> list[int]:
    """Return option indices mentioned in comment, in encounter order."""
    if not comment or not options:
        return []

    comment_cf = comment.casefold()
    mentions: list[tuple[int, int]] = []  # (pos, opt_index)

    for opt_index, opt in enumerate(options):
        if not isinstance(opt, str) or not opt.strip():
            continue

        opt_cf = opt.casefold()

        # Numeric options: match whole number token to avoid 1 matching 10.
        if re.fullmatch(r"\d+", opt.strip()):
            pat = re.compile(rf"(?<!\d){re.escape(opt.strip())}(?!\d)")
            for m in pat.finditer(comment_cf):
                mentions.append((m.start(), opt_index))
            continue

        # Text options: plain substring.
        pos = comment_cf.find(opt_cf)
        while pos != -1:
            mentions.append((pos, opt_index))
            pos = comment_cf.find(opt_cf, pos + 1)

    mentions.sort(key=lambda x: x[0])
    return [opt_index for _, opt_index in mentions]


def _infer_from_comment(comment: str, options: list[str]) -> int | None:
    """Try to infer the intended answer index from comment.

    Heuristics:
    - If comment contains 'tehát'/'helyes' and mentions options, take the last mentioned.
    - Otherwise, if comment mentions exactly one option, take it.
    - Else, give up.
    """
    if not isinstance(comment, str) or not comment.strip():
        return None

    mentions = _iter_option_mentions(comment, options)
    if not mentions:
        return None

    triggers = ("tehát", "helyes", "vagyis", "eredmény", "összesen", "=", "=>")
    if any(t in comment.casefold() for t in triggers):
        return mentions[-1]

    uniq = sorted(set(mentions))
    if len(uniq) == 1:
        return uniq[0]

    return None


def audit_questions(questions: Iterable[dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []

    for idx, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            findings.append(Finding(idx, "ERROR", "not-a-dict", "Question entry is not a dict"))
            continue

        question_text = q.get("question")
        options = q.get("options")
        correct = q.get("correct")

        if not isinstance(question_text, str) or not question_text.strip():
            findings.append(Finding(idx, "ERROR", "missing-question", "Missing/empty 'question'"))

        if not isinstance(options, list):
            findings.append(Finding(idx, "ERROR", "missing-options", "Missing/invalid 'options' (expected list of 5)"))
            continue

        if len(options) != 5:
            findings.append(Finding(idx, "ERROR", "options-count", f"Options count is {len(options)} (expected 5)"))

        if any(not isinstance(o, str) for o in options):
            findings.append(Finding(idx, "ERROR", "option-type", "All options must be strings"))

        correct_index = _letter_to_index(correct) if isinstance(correct, str) else None
        if correct_index is None:
            findings.append(Finding(idx, "ERROR", "bad-correct", f"Invalid 'correct': {correct!r} (expected A-E)"))
        elif correct_index >= len(options):
            findings.append(Finding(idx, "ERROR", "correct-oob", "Correct letter points outside options"))

        # Comment consistency check
        comment = q.get("comment")
        if isinstance(comment, str) and comment.strip() and isinstance(options, list) and len(options) == 5:
            inferred = _infer_from_comment(comment, options)
            if inferred is not None and correct_index is not None and inferred != correct_index:
                findings.append(
                    Finding(
                        idx,
                        "WARN",
                        "comment-mismatch",
                        f"Comment suggests option {LETTERS[inferred]} ({options[inferred]!r}) but correct is {LETTERS[correct_index]} ({options[correct_index]!r})",
                    )
                )

    return findings


def main() -> None:
    import manual_insert_questions as m

    findings = audit_questions(m.QUESTIONS)
    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    print(f"Questions: {len(m.QUESTIONS)}")
    print(f"Errors: {len(errors)} | Warnings: {len(warns)}")

    # Print a compact report.
    for f in findings[:200]:
        print(f"[{f.severity}] #{f.idx} {f.code}: {f.message}")

    if len(findings) > 200:
        print(f"... ({len(findings) - 200} more findings)")

    # Exit nonzero if structural errors exist.
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
