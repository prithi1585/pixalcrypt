from flask import Flask, request, send_file, render_template, jsonify, url_for
from PIL import Image
from stegano import lsb
import io
import os

app = Flask(__name__)

# Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# Home Page (Encryption/Decryption Tool)
@app.route('/tool')
def home():
    return render_template('vs.html')

# Encrypt Route
@app.route('/encrypt', methods=['POST'])
def encrypt():
    image_file = request.files['image']
    message = request.form['message']

    # Save the uploaded image temporarily
    image = Image.open(image_file)
    image_path = "original_image.png"
    image.save(image_path)

    # Hide the message in the image
    secret_image = lsb.hide(image_path, message)
    secret_image_path = "secret_image.png"
    secret_image.save(secret_image_path)

    # Send the encoded image for download
    return send_file(secret_image_path, mimetype='image/png', as_attachment=True, download_name='encrypted_image.png')

# Decrypt Route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    image_file = request.files['image']

    # Save the uploaded image temporarily
    image = Image.open(image_file)
    image_path = "uploaded_image.png"
    image.save(image_path)

    # Reveal the hidden message
    hidden_message = lsb.reveal(image_path)

    return jsonify({'message': hidden_message})

# Run the app with correct port binding for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
