# Deploying Noan to Replit

Replit provides an extremely easy way to both develop and host Flask applications in one place.

## Step 1: Create a Replit Account

1. Go to [Replit](https://replit.com/) and sign up for a free account
2. Verify your email address and log in

## Step 2: Create a New Repl

1. Click the "+ Create" button
2. Select "Python" as the template
3. Name your Repl "Noan" or something similar
4. Click "Create Repl"

## Step 3: Upload Your Files

1. In the Files panel, upload all your project files
   - You can drag and drop files directly from your computer
   - Or use the "Upload file" button in the Files panel
2. Make sure to include all required files: app.py, templates/, static/, etc.

## Step 4: Configure the Repl

1. Create a file named `.replit` with the following content:
```
entrypoint = "app.py"
run = "python app.py"
```

2. Create a `pyproject.toml` file with the following content:
```toml
[tool.poetry]
name = "noan"
version = "0.1.0"
description = "Notion to Anki Converter"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
flask = "^2.3.3"
genanki = "^0.13.0"
beautifulsoup4 = "^4.12.2"
markdown = "^3.4.4"
python-frontmatter = "^1.0.0"
flask-wtf = "^1.1.1"
html2markdown = "^0.1.7"
requests = "^2.31.0"
tqdm = "^4.66.1"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## Step 5: Modify app.py for Replit

Ensure your app.py file has the correct host and port settings for Replit:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

## Step 6: Run Your Application

1. Click the "Run" button at the top of the page
2. Replit will install the dependencies and start your application
3. Your application will be available at the URL shown in the webview (usually something like `https://noan.yourusername.repl.co`)

## Step 7: Make Your Repl Always On (Optional, Requires Replit Pro)

1. Go to the "Tools" panel
2. Select "Always On"
3. Toggle it on to keep your application running even when you're not actively using it

## Advantages of Replit

- All-in-one environment for development and hosting
- Easy collaboration features
- No need to worry about deploying and managing servers
- Great for demonstrations and sharing your application
- Built-in database (Replit DB) if you need persistent storage later

## Limitations

- Free tier has memory and performance constraints
- Unless you enable "Always On" (paid feature), your application will sleep after a period of inactivity 