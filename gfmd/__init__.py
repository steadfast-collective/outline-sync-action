#!/usr/local/bin/python3.8

import argparse
import base64
from dataclasses import dataclass
from pathlib import Path
import re
import sys
import zlib


# Note, this only handles the normal case of triple-` at the moment,
# but more backticks are possible.
START_TOKEN = "<!-- gfmd-start -->"
END_TOKEN = "<!-- gfmd-end -->"
CODE_START_TOKEN = "```mermaid"
CODE_END_TOKEN = "```"


TEMPLATE = """<!-- gfmd-start -->
![Mermaid diagram]({image_link})

<details>
<summary><sup><sub>Diagram source code</sub></sup></summary>

```mermaid
{input_mermaid}
```
</details>
<!-- gfmd-end -->"""


def make_kroki_image_link(src):
    """See https://kroki.io/#how."""
    diagram = base64.urlsafe_b64encode(zlib.compress(src.encode("utf-8"), 9)).decode("utf-8")
    return f"https://kroki.io/mermaid/svg/{diagram}"


def template_diagram(mermaid_src, link):
    return TEMPLATE.format(input_mermaid=mermaid_src, image_link=link)


@dataclass
class Replacement:
    start: int
    end: int
    new_content: str


def process_markdown_file(markdown: str):
    """Find all the fenced blocks and process them. Return new file content."""
    replacements = []
    for match in re.finditer(START_TOKEN, markdown):
        block = markdown[match.start() :]
        code_block = block[block.index(CODE_START_TOKEN) + len(CODE_START_TOKEN) :]
        code_block = code_block[: code_block.index(CODE_END_TOKEN)].strip()

        replacements.append(
            Replacement(
                start=match.start(),
                end=match.start() + block.index(END_TOKEN) + len(END_TOKEN),
                new_content=template_diagram(code_block, make_kroki_image_link(code_block)),
            )
        )

    # Make later substitutions first
    replacements.sort(key=lambda x: x.start, reverse=True)

    if not replacements:
        return None

    for replacement in replacements:
        markdown = markdown[: replacement.start] + replacement.new_content + markdown[replacement.end :]

    return markdown

def run():

    # Parse program input
    parser = argparse.ArgumentParser(description='Updated embedded mermaid diagrams in markdown.')
    parser.add_argument('files', metavar='file', type=str, nargs='*', help='The files to render. Parse none to render all files.')
    args = parser.parse_args()
    files = args.files

    # If no files passed, run on everything
    if not files:
        files = Path(".").rglob("*.md")

    for file in files:
        print(f"Processing {file}... ", end="")
        file = Path(file)
        if (new_file := process_markdown_file(file.read_text())) :
            print("Updated... ", end="")
            file.write_text(new_file)
        else:
            print("Skipped... ", end="")
        print("Done.")


if __name__ == "__main__":
    run()
