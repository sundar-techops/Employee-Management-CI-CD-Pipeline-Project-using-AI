#!/usr/bin/env python3
"""
AI Release Notes Generator
After a successful deployment, reads recent git commits and generates
a clean, professional changelog using Claude AI.
"""

import os
import subprocess
import anthropic
from datetime import datetime


def get_git_commits() -> str:
    """Get the last 15 commit messages."""
    try:
        result = subprocess.check_output(
            ["git", "log", "-15", "--pretty=format:%h | %an | %s", "--no-merges"],
            stderr=subprocess.STDOUT
        )
        return result.decode("utf-8")
    except subprocess.CalledProcessError:
        return "Could not retrieve git commits"


def generate_release_notes(commits: str, build_number: str) -> str:
    """Use Claude to generate formatted release notes."""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY environment variable not set."

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Build #{build_number} of the Employee Management API just deployed successfully.\n\n"
                    f"Recent commits:\n{commits}\n\n"
                    "Generate clean release notes with these sections:\n"
                    "## What's New (Added features)\n"
                    "## Bug Fixes\n"
                    "## Improvements\n\n"
                    "Each item should be a single bullet point.\n"
                    "If there's nothing for a section, write 'No changes'.\n"
                    "Write as if publishing to end users and developers."
                )
            }
        ]
    )

    return response.content[0].text


def main():
    build_number = os.environ.get("BUILD_NUMBER", "unknown")

    print("=" * 60)
    print("AI RELEASE NOTES GENERATOR")
    print("=" * 60)

    commits = get_git_commits()
    print(f"Commits analyzed:\n{commits}\n")

    release_notes = generate_release_notes(commits, build_number)
    print(release_notes)

    # Write the release notes file
    today = datetime.now().strftime("%Y-%m-%d")
    with open("RELEASE_NOTES.md", "w") as out:
        out.write(f"# Release Notes — Build #{build_number}\n")
        out.write(f"**Released:** {today}\n\n")
        out.write(release_notes)

    print("\n✅ Release notes saved to RELEASE_NOTES.md")


if __name__ == "__main__":
    main()