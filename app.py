import os
import tempfile
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
import file_handler
import markdown_parser
import anki_generator

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Config
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'noan_uploads')
ALLOWED_EXTENSIONS = {'md', 'html', 'zip'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Store the file path in session
        session_data = {
            'filepath': filepath,
            'filename': filename
        }
        
        # For ZIP files (Notion exports)
        if filename.endswith('.zip'):
            try:
                # Extract the ZIP
                extract_info = file_handler.extract_notion_export(filepath)
                session_data['extract_dir'] = extract_info['extract_dir']
                session_data['md_files'] = extract_info['md_files']
                
                # Redirect to file selection if multiple files
                if len(extract_info['md_files']) > 1:
                    return render_template('select_file.html', 
                                          files=extract_info['md_files'],
                                          session_data=session_data)
                
                # If only one file, use that
                session_data['filepath'] = extract_info['md_files'][0]
                
            except Exception as e:
                flash(f'Error extracting ZIP file: {str(e)}')
                return redirect(url_for('index'))
        
        return render_template('convert.html', session_data=session_data)
    
    flash('File type not allowed')
    return redirect(url_for('index'))

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Get file path and conversion options
        filepath = request.form.get('filepath')
        mode = request.form.get('mode', 'anki_front_back')
        deck_name = request.form.get('deck_name', 'My Deck')
        include_tags = request.form.get('include_tags', 'on') == 'on'
        tags = request.form.get('tags', '').split(',') if include_tags else []
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Read the file
        file_content = file_handler.read_file(filepath)
        
        # Parse based on mode
        options = {
            'include_reversed': request.form.get('include_reversed', 'off') == 'on',
        }
        
        parsed_data = markdown_parser.parse(file_content, mode, options)
        
        if not parsed_data:
            flash('No cards found in the document. Check your formatting or try a different mode.')
            return redirect(url_for('index'))
        
        # Generate Anki deck
        anki_options = {
            'deck_name': deck_name,
            'tags': tags,
            'extra': request.form.get('extra', '')
        }
        
        deck = anki_generator.generate_anki_cards(parsed_data, mode, anki_options)
        
        # Save the deck to a temporary file
        output_filename = f"{deck_name.replace(' ', '_')}.apkg"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        file_handler.write_file(output_path, deck)
        
        # Prepare preview data
        preview_data = []
        
        if mode == 'anki_front_back' or mode == 'anki_basic_and_reversed':
            for i, (front, back) in enumerate(parsed_data[:5]):  # Show first 5 cards
                preview_data.append({
                    'id': i + 1,
                    'front': front,
                    'back': back
                })
        elif mode == 'anki_cloze':
            for i, text in enumerate(parsed_data[:5]):  # Show first 5 cards
                preview_data.append({
                    'id': i + 1,
                    'text': text
                })
        
        return render_template('download.html', 
                              output_filename=output_filename,
                              deck_name=deck_name,
                              card_count=len(parsed_data),
                              preview_data=preview_data,
                              mode=mode)
    
    except Exception as e:
        logger.exception("Error in conversion process")
        flash(f'Error converting file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        flash('File not found')
        return redirect(url_for('index'))
    
    return send_file(filepath, 
                    mimetype='application/octet-stream',
                    download_name=filename,
                    as_attachment=True)

@app.route('/preview', methods=['POST'])
def preview():
    try:
        # Get file content and options for preview
        filepath = request.form.get('filepath')
        mode = request.form.get('mode', 'anki_front_back')
        
        # Read the file
        file_content = file_handler.read_file(filepath)
        
        # Parse a sample for preview
        options = {
            'include_reversed': request.form.get('include_reversed', 'off') == 'on',
            'max_cards': 5  # Limit preview to 5 cards
        }
        
        parsed_data = markdown_parser.parse(file_content, mode, options)
        preview_data = []
        
        if mode == 'anki_front_back' or mode == 'anki_basic_and_reversed':
            for i, (front, back) in enumerate(parsed_data[:5]):
                preview_data.append({
                    'id': i + 1,
                    'front': front,
                    'back': back
                })
        elif mode == 'anki_cloze':
            for i, text in enumerate(parsed_data[:5]):
                preview_data.append({
                    'id': i + 1,
                    'text': text
                })
        
        return jsonify({
            'success': True,
            'preview': preview_data,
            'mode': mode
        })
    
    except Exception as e:
        logger.exception("Error generating preview")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 