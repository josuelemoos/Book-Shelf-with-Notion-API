# Notion Book CLI

A Python CLI tool to log books, authors, tags, and reviews directly to a Notion Database from the terminal, without needing to open the browser.

## Features

- **Quick Logging:** Add books to your database via command line arguments.
- **Auto-Tagging:** Automatically creates new tags in Notion (Multi-select) if they don't exist.
- **Reviews:** Writes your review directly into the page body.
- **Interactive Mode:** Prompts for details if no arguments are provided.

## Prerequisites

- Python 3.x
- A Notion Account
- A Notion Integration Token

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/SEU-USUARIO/notion-book-cli.git](https://github.com/SEU-USUARIO/notion-book-cli.git)
   cd notion-book-cli

2. **Install dependencies**

Bash
pip install requests

3. **Configure Notion**

Go to Notion My Integrations and create a new integration to get your Internal Integration Token.

Open your Book Database on Notion, click ... > Connections and add your integration.

Copy the Database ID from the URL (the part before ?v=).

4. **Update the script**

Open AddBookToNotion.py.

Replace NOTION_TOKEN and DATABASE_ID with your credentials.

5. **USAGE**

**Option 1: Interactive Mode**

Just run the script and follow the prompts.

Bash
python add_livro.py

**Option 2: One-line Command**
Pass the arguments in this order: "Title" "Author" "Tags" "Review"

Bash
python add_livro.py "Dune" "Frank Herbert" "Sci-Fi, Classic" "A masterpiece about politics and sand."

