import re
import logging
import html

logger = logging.getLogger(__name__)

# Regular expression patterns
BULLET_PATTERN = r'^- (.*?)$|^\* (.*?)$'  # Match both - and * bullets
SUB_BULLET_PATTERN = r'^\s{2,4}- (.*?)$|^\s{2,4}\* (.*?)$'  # Match sub-bullets with flexible spacing
CLOZE_BRACKET_PATTERN = r'\[(.*?)\]'  # [Text] for Cloze deletion type 1
CLOZE_PAREN_PATTERN = r'\((.*?)\)'    # (Text) for Cloze deletion type 2
CLOZE_CURLY_PATTERN = r'\{(.*?)\}'    # {Text} for Cloze deletion type 3
TOGGLE_PATTERN = r'<details>(.*?)<summary>(.*?)</summary>(.*?)</details>'  # Notion toggles

def parse(content_data, mode, options=None):
    """
    Parse markdown content based on mode and options
    
    Args:
        content_data: Dictionary containing content and metadata
        mode: Parsing mode (anki_front_back, anki_cloze, anki_basic_and_reversed, etc.)
        options: Additional options for parsing
        
    Returns:
        List of parsed notes
    """
    if options is None:
        options = {}
    
    content = content_data.get('content', '')
    content_type = content_data.get('type', 'markdown')
    
    # Clean up line endings and ensure consistent format
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    if mode == 'anki_front_back':
        return parse_front_back(content, options)
    elif mode == 'anki_cloze':
        return parse_cloze(content, options)
    elif mode == 'anki_basic_and_reversed':
        return parse_basic_and_reversed(content, options)
    elif mode == 'anki_toggle':
        return parse_toggles(content, options)
    else:
        logger.warning(f"Unknown parse mode: {mode}, falling back to front_back")
        return parse_front_back(content, options)

def parse_front_back(content, options=None):
    """Parse content for front and back cards"""
    if options is None:
        options = {}
    
    result = []
    lines = content.split('\n')
    
    bullet_pattern = re.compile(BULLET_PATTERN)
    sub_bullet_pattern = re.compile(SUB_BULLET_PATTERN)
    
    current_front = None
    
    for i, line in enumerate(lines):
        bullet_match = bullet_pattern.match(line)
        if bullet_match:
            # Found a bullet point - potential front of card
            if current_front is not None and i + 1 < len(lines):
                # Check if the next line is a sub-bullet for the back
                next_line = lines[i + 1]
                sub_match = sub_bullet_pattern.match(next_line)
                if sub_match:
                    # Extract the content (first non-None group)
                    back_content = next(filter(None, sub_match.groups()))
                    front_content = current_front
                    # Add to result if both front and back have content
                    if front_content and back_content:
                        result.append((html.escape(front_content.strip()), 
                                       html.escape(back_content.strip())))
            
            # This bullet becomes the current front
            current_front = next(filter(None, bullet_match.groups()))
    
    return result

def parse_cloze(content, options=None):
    """Parse content for cloze deletion cards"""
    if options is None:
        options = {}
    
    result = []
    # Split content by blank lines or periods to find cloze sentences
    pattern = r'([^.\n]+(?:\[.*?\]|\(.*?\)|\{.*?\})[^.\n]*\.)'
    cloze_items = re.findall(pattern, content)
    
    for item in cloze_items:
        # Process the cloze item
        cloze_text = item.strip()
        
        # Apply cloze formatting for different bracket types
        cloze_count = 1
        
        # Process square brackets [text] as {{c1::text}}
        for match in re.finditer(CLOZE_BRACKET_PATTERN, cloze_text):
            cloze_text = cloze_text.replace(match.group(0), 
                                           f'{{{{c{cloze_count}::{match.group(1)}}}}}', 1)
            cloze_count += 1
        
        # Process parentheses (text) as {{c2::text}}
        for match in re.finditer(CLOZE_PAREN_PATTERN, cloze_text):
            cloze_text = cloze_text.replace(match.group(0), 
                                           f'{{{{c{cloze_count}::{match.group(1)}}}}}', 1)
            cloze_count += 1
            
        # Process curly braces {text} as {{c3::text}}
        for match in re.finditer(CLOZE_CURLY_PATTERN, cloze_text):
            cloze_text = cloze_text.replace(match.group(0), 
                                           f'{{{{c{cloze_count}::{match.group(1)}}}}}', 1)
            cloze_count += 1
        
        # Only add if there were cloze deletions
        if cloze_count > 1:
            result.append(html.escape(cloze_text))
    
    return result

def parse_basic_and_reversed(content, options=None):
    """Parse content for basic and reversed cards (front<->back)"""
    if options is None:
        options = {}
    
    # Get regular front-back cards
    front_back_cards = parse_front_back(content, options)
    
    # Create reversed versions (back->front) and append both versions
    result = []
    for front, back in front_back_cards:
        # Add normal direction
        result.append((front, back))
        # Add reversed direction if option enabled
        if options.get('include_reversed', True):
            result.append((back, front))
    
    return result

def parse_toggles(content, options=None):
    """Parse Notion toggles as front-back cards"""
    if options is None:
        options = {}
    
    result = []
    # Find all toggle blocks (often used in Notion exports)
    toggle_matches = re.finditer(TOGGLE_PATTERN, content, re.DOTALL)
    
    for match in toggle_matches:
        summary = match.group(2).strip()
        details = match.group(3).strip()
        
        if summary and details:
            result.append((html.escape(summary), html.escape(details)))
    
    return result
