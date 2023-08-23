from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    uploaded_files = get_uploaded_files()
    return render_template('kod.html', uploaded_files=uploaded_files)

def get_uploaded_files():
    uploaded_dir = os.path.join(os.getcwd(), "uploaded")
    return os.listdir(uploaded_dir)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nie wybrano pliku"

    file = request.files['file']
    if file.filename == '':
        return "Nie wybrano pliku"

    uploaded_dir = os.path.join(os.getcwd(), "uploaded")
    os.makedirs(uploaded_dir, exist_ok=True)

    file.save(os.path.join(uploaded_dir, file.filename))
    return "Plik został przesłany pomyślnie"

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    uploaded_dir = os.path.join(os.getcwd(), "uploaded")
    return send_from_directory(uploaded_dir, filename)

@app.route('/filelist', methods=['GET'])
def file_list():
    uploaded_files = get_uploaded_files()
    return render_template('file_list.html', uploaded_files=uploaded_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12346)
