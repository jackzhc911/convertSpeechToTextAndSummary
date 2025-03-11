from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Call the web service to get the transcription
        with open(file_path, 'rb') as f:
            response = requests.post(
                'http://127.0.0.1:8000/v1/audio/transcriptions',
                files={'file': f},
                data={'model': 'whisper-1'}
            )
        
        if response.status_code != 200:
            return 'Failed to get transcription', response.status_code
        
        transcription_text = response.text
        transcription_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'transcription.txt')
        with open(transcription_file_path, 'w', encoding='utf-8') as transcription_file:
            transcription_file.write(transcription_text)
        
        # Call the Ollama service to summarize the transcription
        ollama_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2',
                'prompt': transcription_text,
                'stream': False
            }
        )
        
        if ollama_response.status_code == 200:
            summary = ollama_response.json()
            summary_text = summary.get('response', 'No response found')
            summary_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'summary.txt')
            with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary_text)
            
            return jsonify({
                'transcription_file': 'transcription.txt',
                'summary_file': 'summary.txt'
            })
        else:
            return 'Failed to get summary', ollama_response.status_code

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@app.route('/result', methods=['POST'])
def result():
    transcription_file = request.form.get('transcription_file')
    summary_file = request.form.get('summary_file')
    return render_template('result.html', transcription_file=transcription_file, summary_file=summary_file)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(debug=True)