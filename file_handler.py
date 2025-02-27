# file_handler.py
import genanki
import os
import zipfile
import tempfile
import logging
from bs4 import BeautifulSoup
import html2markdown
import frontmatter

logger = logging.getLogger(__name__)

def read_file(path):
    """Read file content based on file type"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    file_ext = os.path.splitext(path)[1].lower()
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if file_ext == '.md':
            # For markdown files, check if they have YAML frontmatter
            parsed = frontmatter.parse(content)
            # Return both the content and any metadata
            return {
                'content': parsed.content,
                'metadata': parsed.metadata,
                'type': 'markdown'
            }
        elif file_ext == '.html':
            # For HTML files, convert to markdown for consistent processing
            soup = BeautifulSoup(content, 'html.parser')
            markdown_content = html2markdown.convert(content)
            return {
                'content': markdown_content,
                'html_content': content,  # Keep original HTML
                'metadata': {'title': soup.title.string if soup.title else 'Untitled'},
                'type': 'html'
            }
        else:
            # For other file types, just return content
            return {
                'content': content,
                'metadata': {},
                'type': 'unknown'
            }
    except Exception as e:
        logger.error(f"Error reading file {path}: {str(e)}")
        raise

def extract_notion_export(zip_path, extract_to=None):
    """Extract Notion export ZIP file"""
    if extract_to is None:
        extract_to = tempfile.mkdtemp()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Find main markdown file
        md_files = []
        for root, _, files in os.walk(extract_to):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        return {
            'extract_dir': extract_to,
            'md_files': md_files
        }
    except Exception as e:
        logger.error(f"Error extracting Notion export: {str(e)}")
        raise

def write_file(path, deck):
    """Write Anki deck to file"""
    try:
        package = genanki.Package(deck)
        package.write_to_file(path)
        return True
    except Exception as e:
        logger.error(f"Error writing Anki deck to {path}: {str(e)}")
        raise
