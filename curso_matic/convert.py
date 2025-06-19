"""
curso_matic.convert
===================

CLI command that converts a Markdown file (.md) to AsciiDoc (.adoc)
using regular-expression substitutions.

Reference used:
https://docs.asciidoctor.org/asciidoc/latest/syntax-quick-reference/
"""

import re
from pathlib import Path
import typer

app = typer.Typer(help="Convert Markdown files to AsciiDoc format (regex-based).")


# ------------------------------------------------------------------------
# Regex-based transformer
# ------------------------------------------------------------------------

def md_to_asciidoc(src: str) -> str:
    """
    Convert **common-case** Markdown features to AsciiDoc using re.sub.

    Supported elements
    ------------------
    · Headings # … ######                      → = … ======
    · Bold **text** / __text__                → *text*
    · Italic *text* / _text_                  → _text_
    · Inline code `code`                      → +code+
    · Fenced code blocks ```lang\ncode\n```   → [source,lang]\n----\ncode\n----
    · Links [txt](url)                        → link:url[txt]
    · Images ![alt](url)                      → image::url[alt]
    · Unordered lists -, *, +                 → * item
    · Ordered lists 1. 2. …                   → . item
    """

    out = src

    # 1️⃣ fenced code blocks  ```lang\n...\n```
    def _fenced(m):
        lang = m.group(1) or ""
        body = m.group(2)
        header = f"[source,{lang}]\n" if lang else "[source]\n"
        return f"{header}----\n{body}\n----"
    out = re.sub(r"```(\w+)?\n(.*?)\n```", _fenced, out, flags=re.DOTALL)

    # 2️⃣ headings (do this **before** bold/italic)
    for i in range(6, 0, -1):  # from ###### to #
        md = r"^" + r"#" * i + r"\s+(.*)$"
        adoc = "=" * i + r" \1"
        out = re.sub(md, adoc, out, flags=re.MULTILINE)

    # 3️⃣ italic *text* / _text_  →  _text_
    out = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"_\1_", out)  # *italic*
    out = re.sub(r"(?<!_)_(?!_)([^_\n]+?)_(?!_)",r"_\1_", out)  # _italic_
    
    # 4️⃣ bold **text**  / __text__  →  *text*
    out = re.sub(r"\*\*(.+?)\*\*", r"*\1*", out)   # **bold**
    out = re.sub(r"__(.+?)__",     r"*\1*", out)   # __bold__

    # 5️⃣ inline code  `code`
    out = re.sub(r"`([^`]+?)`", r"+\\1+", out)

    # 6️⃣ images  ![alt](url)
    out = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"image::\2[\1]", out)

    # 7️⃣ links  [text](url)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"link:\2[\1]", out)

    # 7️⃣ unordered list items  (-, *, +)  ➞  * item
    out = re.sub(r"^\s*([-*+])\s+(.*)$", r"* \2", out, flags=re.MULTILINE)

    # 8️⃣ ordered list items  (1. 2. …)   ➞  . item
    out = re.sub(r"^\s*\d+\.\s+(.*)$", r". \1", out, flags=re.MULTILINE)

    # 9️⃣ ensure a BLANK line **BEFORE** every list item
    #    If the previous character is *not* a newline, insert an extra newline.
    #    (Prevents “paragraph* item” cases.)
    out = re.sub(
        r"([^\n])\n([*\.]\s+)",       # single newline before a list marker
        r"\1\n\n\2",                  # add another newline
        out
    )

    # 🔟 ensure a BLANK line **AFTER** every list item
    out = re.sub(
        r"^([*\.]\s+.+?)\n(?!\n)",    # list line followed by only ONE newline
        r"\1\n\n",                    # add another newline
        out,
        flags=re.MULTILINE,
    )


    # Blockquotes, tables, etc. can be added later if needed
    return out


# ------------------------------------------------------------------------
# Typer command
# ------------------------------------------------------------------------

@app.command("md-to-asciidoc")
def markdown_to_asciidoc(
    input_file: str = typer.Argument(..., help="Path to the Markdown (.md) file to convert"),
    output_file: str = typer.Option(
        None, help="Output file path (defaults to same name with .adoc extension)"
    ),
):
    """
    Convert **Markdown → AsciiDoc** using regex rules only (no external libs).
    """
    typer.echo(f"📖 Reading Markdown file: {input_file}")
    src_path = Path(input_file)
    md_text = src_path.read_text(encoding="utf-8")

    typer.echo(f"➡️ Converting Markdown file to AsciiDoc format...")
    adoc_text = md_to_asciidoc(md_text)

    out_path = Path(output_file) if output_file else src_path.with_suffix(".adoc")
    out_path.write_text(adoc_text, encoding="utf-8")

    typer.echo(f"✅ Converted to AsciiDoc: {out_path}")


if __name__ == "__main__":
    app()
