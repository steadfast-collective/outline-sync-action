#!/usr/local/bin/python3.8
import argparse
from pathlib import Path

import marko
from marko.md_renderer import MarkdownRenderer
#from marko.ast_renderer import ASTRenderer
from .elements import RenderableMermaid


def run():

    # Parse program input
    parser = argparse.ArgumentParser(
        description="Updated embedded mermaid diagrams in markdown."
    )
    parser.add_argument(
        "files",
        metavar="file",
        type=str,
        nargs="*",
        help="The files to render. Parse none to render all files.",
    )
    args = parser.parse_args()
    files = args.files

    # If no files passed, run on everything
    if not files:
        files = Path(".").rglob("*.md")

    markdown_parser = marko.Markdown(renderer=MarkdownRenderer, extensions=[RenderableMermaid])

    for file in files:
        print(f"Processing {file}... ", end="")
        file = Path(file)
        new_file = markdown_parser.convert(file.read_text())

        if new_file != file:
            print("Updated... ", end="")
            file.write_text(new_file)
        else:
            print("Skipped... ", end="")

        print("Done.")


if __name__ == "__main__":
    run()
