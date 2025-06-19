import typer
from curso_matic import translate, convert  # Import modules

# Create the main CLI app
app = typer.Typer(
    help="curso-matic: A CLI tool to manage online courses.",
    no_args_is_help=True
)

# Add the 'translate' command group from translate.py
app.add_typer(
    translate.app,
    name="translate",
    help="Translate Markdown files from English to Spanish using the ChatGPT API."
)

# Add the 'convert' command group from convert.py
app.add_typer(
    convert.app,
    name="convert",
    help="Convert Markdown files to AsciiDoc format."
)

# Entry point for CLI
if __name__ == "__main__":
    app()