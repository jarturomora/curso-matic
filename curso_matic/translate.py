import typer
import os
import openai
import re
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv  # Load .env environment variables

# Create the main CLI app
app = typer.Typer()

# Load environment variables from .env (e.g., OPENAI_API_KEY)
load_dotenv()

# Regex pattern to identify code blocks (```...```)
CODE_BLOCK_PATTERN = re.compile(r"```.*?```", re.DOTALL)


def load_exclusion_keywords(path: Optional[str]) -> set:
    """
    Load keywords or phrases to exclude from translation.

    Args:
        path (str): Path to a text file with exclusion keywords (one per line)

    Returns:
        set: A set of excluded keywords
    """
    if not path:
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def extract_code_blocks(text: str):
    """
    Temporarily replace code blocks with placeholders.

    Args:
        text (str): Original Markdown content

    Returns:
        (text_without_code, placeholder_map): Text with code blocks replaced and list of (placeholder, code_block)
    """
    code_blocks = CODE_BLOCK_PATTERN.findall(text)
    placeholders = []
    for i, block in enumerate(code_blocks):
        placeholder = f"[[[CODE_BLOCK_{i}]]]"
        text = text.replace(block, placeholder, 1)
        placeholders.append((placeholder, block))
    return text, placeholders


def restore_code_blocks(text: str, placeholders: list[tuple[str, str]]) -> str:
    """
    Replace placeholders with the original code blocks.

    Args:
        text (str): Translated text with placeholders
        placeholders (list): List of (placeholder, original code block)

    Returns:
        str: Final text with code blocks restored
    """
    for placeholder, block in placeholders:
        text = text.replace(placeholder, block)
    return text

def mask_excluded_keywords(text: str, exclusion_keywords: set) -> str:
    """
    Replace each excluded keyword in the text with a masked version [[[KEYWORD]]]
    to prevent it from being translated by ChatGPT.

    Args:
        text (str): Input text
        exclusion_keywords (set): Set of words to preserve

    Returns:
        str: Masked text
    """
    for word in exclusion_keywords:
        # Only replace whole words using word boundaries
        text = re.sub(rf"\b({re.escape(word)})\b", r"[[[\1]]]", text)
    return text

def translate_with_openai(content: str) -> str:
    """
    Translate the input content using the ChatGPT API.

    Args:
        content (str): The text to translate

    Returns:
        str: Translated content
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Please define it in a .env file or export it.")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change to "gpt-3.5-turbo" for cost-saving
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional translator. "
                    "Translate the following Markdown content from English to Spanish. "
                    "Do not translate Markdown code blocks. "
                    "Do not translate any content wrapped in [[[ and ]]] — those are protected keywords."
                ),
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0.4,
    )
    return response.choices[0].message["content"]

# Unmask keywords after translation
def unmask_keywords(text: str) -> str:
    return re.sub(r"\[\[\[(.*?)\]\]\]", r"\1", text)

@app.command()
def file(
    path: str = typer.Argument(..., help="Path to the Markdown file to translate"),
    exclude: Optional[str] = typer.Option(None, help="Path to exclusion keywords file"),
    output: Optional[str] = typer.Option(None, help="Output file path (default: filename.es.md)"),
):
    """
    Translate a Markdown file from English to Spanish using the ChatGPT API.
    Code blocks and excluded content will not be translated.
    """
    typer.echo(f"📖 Reading: {path}")
    text = Path(path).read_text(encoding="utf-8")

    exclusion_keywords = load_exclusion_keywords(exclude)

    # Remove and store code blocks before translation
    text_no_code, placeholders = extract_code_blocks(text)

    # Mask excluded keywords so they are not translated
    masked_text = mask_excluded_keywords(text_no_code, exclusion_keywords)

    typer.echo("🌍 Sending text to ChatGPT for translation...")
    translated_text = translate_with_openai(masked_text)

    
    typer.echo("🔄 Restoring code blocks and unmasking keywords...")
    # Restore code blocks in the translated text
    final_text = restore_code_blocks(translated_text, placeholders)
    # Unmask excluded keywords in the final text    
    final_text = unmask_keywords(final_text)


    # Determine output file name
    out_path = output or f"{Path(path).stem}.es.md"
    Path(out_path).write_text(final_text, encoding="utf-8")

    typer.echo(f"✅ Translation complete. Output written to: {out_path}")
