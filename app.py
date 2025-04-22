from flask import Flask, request, jsonify, send_file
import os
import uuid
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_to_exe():
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if file is a Python file
    if not file.filename.endswith('.py'):
        return jsonify({'error': 'File must be a Python script (.py)'}), 400
    
    # Save the uploaded file
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
    os.makedirs(upload_dir, exist_ok=True)
    
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Get conversion options from request
    options = request.form.to_dict()
    
    try:
        # Build pyinstaller command based on options
        cmd = ['pyinstaller', '--onefile', '--distpath', upload_dir]
        
        if options.get('appType') == 'windowed':
            cmd.append('--windowed')
        
        if options.get('icon'):
            # Handle icon upload and add to command
            pass
        
        cmd.append(filepath)
        
        # Run pyinstaller
        result = subprocess.run(
            cmd,
            cwd=upload_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Conversion failed',
                'details': result.stderr
            }), 500
        
        # Find the generated exe file
        exe_name = filename.replace('.py', '.exe')
        exe_path = os.path.join(upload_dir, exe_name)
        
        if not os.path.exists(exe_path):
            # Try alternative path (pyinstaller sometimes changes names)
            for f in os.listdir(upload_dir):
                if f.endswith('.exe'):
                    exe_path = os.path.join(upload_dir, f)
                    break
        
        return jsonify({
            'success': True,
            'download_url': f'/download/{unique_id}/{os.path.basename(exe_path)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<unique_id>/<filename>')
def download_file(unique_id, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_id, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)