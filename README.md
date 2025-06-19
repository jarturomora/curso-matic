# curso-matic

**curso-matic** is a command-line interface (CLI) tool designed to help you efficiently manage online courses. It aims to simplify content translation, format conversion, link validation, and publishing on multiple e-learning platforms such as OpenEdX and Udemy.

## Key Features

* **Translate content** from English to Spanish using the ChatGPT API, with support for excluding specific sections like code blocks or keyword lists.
* **Convert Markdown to AsciiDoc** to prepare course content for various publishing platforms.
* **Check for broken links** in Markdown or AsciiDoc documents.
* **Publish courses** to e-learning platforms such as OpenEdX or Udemy (with proper credentials).

## Use Case Diagram

The following diagram summarizes the main features of `curso-matic` from the user's perspective:

![Use Case Diagram](img/use-case-diagram.png)

## 🔧 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jarturomora/curso-matic.git
    cd curso-matic
    ```

2. (Optional) Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies and the app in editable mode:

    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

4. Create a `.env` file with your OpenAI API key:

    ```env
    OPENAI_API_KEY=your-api-key-here
    ```

## 🚀 Usage: Translate a Markdown file

To translate a file from English to Spanish, preserving code blocks and specific keywords:

```bash
curso-matic translate file lesson1.md --exclude words.txt --output lesson1.es.md
```

* `lesson1.md`: your input file in English.
* `--exclude words.txt`: a list of keywords to preserve during translation.
* `--output lesson1.es.md`: (optional) the output file name.
