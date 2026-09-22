#!/usr/bin/env python3
"""
AI Build Failure Analyzer
When Jenkins build fails, this script reads the log and uses Claude AI
to diagnose the root cause and suggest a concrete fix.
"""

import os
import sys
import anthropic


def analyze_build_failure(log_file_path: str) -> str:
    """Read the build log and get AI diagnosis."""

    # Read the log file
    try:
        with open(log_file_path, "r", encoding="utf-8", errors="replace") as f:
            full_log = f.read()
    except FileNotFoundError:
        return "Error: Log file not found at " + log_file_path

    # Use only the last 6000 characters — the failure is usually at the end
    log_tail = full_log[-6000:]

    # Call the Anthropic Claude API
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY environment variable not set."

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a senior DevOps engineer reviewing a failed Jenkins CI build log.\n\n"
                    "BUILD LOG (last portion):\n"
                    f"```\n{log_tail}\n```\n\n"
                    "Analyze this log and respond with:\n"
                    "1. **Root Cause** (2-3 sentences max)\n"
                    "2. **Exact Fix** (the specific command or code change needed)\n"
                    "3. **Prevention** (one line on how to avoid this next time)\n\n"
                    "Be specific. No generic advice. Reference actual lines from the log."
                )
            }
        ]
    )

    return response.content[0].text


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_failure.py <path-to-log-file>")
        sys.exit(1)

    log_file = sys.argv[1]

    print("=" * 60)
    print("AI BUILD FAILURE ANALYSIS")
    print("=" * 60)

    analysis = analyze_build_failure(log_file)
    print(analysis)

    # Write to file so Jenkins can archive it
    with open("ai_failure_summary.md", "w", encoding="utf-8") as out:
        out.write("# AI Build Failure Analysis\n\n")
        out.write(f"**Log file analyzed:** `{log_file}`\n\n")
        out.write(analysis)

    print("\n✅ Analysis saved to ai_failure_summary.md")


if __name__ == "__main__":
    main()