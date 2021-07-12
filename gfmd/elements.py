import base64
import re
import zlib

from marko.block import BlockElement


class RenderableMermaidBlock(BlockElement):

    priority = 10  # Try before the html block parser

    SUPPORTED_TYPES = ("mermaid", "plantuml")
    START_TOKEN = re.compile(rf"```({'|'.join(SUPPORTED_TYPES)})")
    END_TOKEN = "```"
    _parse_info = ("", "")

    def __init__(self, match):
        markup_language, diagram_src = match
        self.markup_language = markup_language
        self.diagram_src = diagram_src

    @classmethod
    def match(cls, source):
        m = source.expect_re(cls.START_TOKEN)
        if not m:
            return None
        cls._parse_info = m.groups()
        return m

    @classmethod
    def parse(cls, source):
        source.next_line()
        source.consume()

        diagram_lines = []

        while not source.exhausted:
            line = source.next_line()
            if line is None:
                break
            source.consume()

            if cls.END_TOKEN in line:
                break

            diagram_lines.append(line.lstrip())

        # Return just the mermaid diagram source
        return cls._parse_info[0], "".join(diagram_lines).strip()


class RenderableMermaidBlockRendererMixin(object):

    template = """![{language} diagram]({image_link})

"""

    def render_renderable_mermaid_block(self, element):
        """Markdown render!"""
        link = self.make_kroki_image_link(element.markup_language, element.diagram_src)
        return self.template.format(
            input_mermaid=element.diagram_src,
            image_link=link,
            language=element.markup_language,
        )

    def make_kroki_image_link(self, language, src):
        """See https://kroki.io/#how."""
        diagram = base64.urlsafe_b64encode(
            zlib.compress(src.encode("utf-8"), 9)
        ).decode("utf-8")
        return f"https://kroki.io/{language}/svg/{diagram}"


class RenderableMermaid:
    elements = [RenderableMermaidBlock]
    renderer_mixins = [RenderableMermaidBlockRendererMixin]
