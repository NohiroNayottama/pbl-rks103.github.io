from flask import Flask, render_template, request, send_file, session
import os
import random

secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key

# Set the static folder
app.static_folder = '{{ url_for('static', filename='style.css') }}'

# Fungsi Caesar Cipher
def caesar_cipher(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

@app.route('/')
def index():
    return render_template('index.html', text="", key="", result_text="", cipher_text="", brute_force_results={})

@app.route('/process', methods=['POST'])
def process():
    text = request.form.get('text', '')
    result_text = text  # Initialize result_text with the original text

    if 'action' in request.form:
        action = request.form['action']
        if action == 'upload':
            uploaded_file = request.files['uploaded_file']
            if uploaded_file:
                uploaded_text = uploaded_file.read().decode('utf-8')
                text = uploaded_text
        elif action == 'encrypt':
            key = int(request.form['key'])
            result_text = caesar_cipher(text, key)
        elif action == 'decrypt':
            key = int(request.form.get('key', 0))
            result_text = caesar_cipher(text, -key)

    return render_template('index.html', text=text, key=request.form.get('key', ''), result_text=result_text, brute_force_results={})


@app.route('/encrypt', methods=['POST'])
def encrypt():
    plain_text = request.form['text']
    key = int(request.form['key'])
    cipher_text = caesar_cipher(plain_text, key)
    return render_template('index.html', text=plain_text, key=key, result_text=cipher_text, action='encrypt')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    cipher_text = request.form['text']
    key = int(request.form['key'])
    plain_text = caesar_cipher(cipher_text, -key)
    return render_template('index.html', text=cipher_text, key=key, result_text=plain_text, action='decrypt')

@app.route('/bruteforce', methods=['POST'])
def bruteforce():
    cipher_text = request.form['cipher_text']
    brute_force_results = {}
    for key in range(1, 26):
        result = caesar_cipher(cipher_text, -key)
        brute_force_results[key] = result
    return render_template('index.html', brute_force_results=brute_force_results, cipher_text=cipher_text)

if __name__ == '__main__':
    app.run(debug=True)
