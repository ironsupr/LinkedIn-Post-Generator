"""
LinkedIn Post Generator - Main Entry Point

A tool for generating professional LinkedIn posts from aggregated tech content.

Usage:
    python main.py [COMMAND] [OPTIONS]

Commands:
    fetch            - Fetch new content from all sources
    generate         - Generate a LinkedIn post
    list-drafts      - List all draft posts
    review           - Review a specific draft
    mark-posted      - Mark a post as published
    stats            - Show statistics
    preview-content  - Preview top content
    workflow         - Show recommended workflow

Examples:
    # Daily: Fetch new content
    python main.py fetch

    # 2x Weekly: Generate a post
    python main.py generate --type news

    # Review before posting
    python main.py review --id 1

    # After posting to LinkedIn
    python main.py mark-posted --id 1

For detailed help on any command:
    python main.py [COMMAND] --help
"""

from src.cli.cli import cli

if __name__ == '__main__':
    cli()
