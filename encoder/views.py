from django.shortcuts import render
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib

def get_key(key):
    return hashlib.sha256(key.encode()).digest()  # 256-bit key

def encode_text(request):
    if request.method == 'POST' and 'text' in request.POST and 'key' in request.POST:
        text = request.POST['text']
        key = get_key(request.POST['key'])
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        encoded_text = iv + ct
        return render(request, 'encoder/index.html', {'encoded_text': encoded_text})
    return render(request, 'encoder/index.html')

def decode_text(request):
    if request.method == 'POST' and 'encoded_text' in request.POST and 'key' in request.POST:
        encoded_text = request.POST['encoded_text']
        key = get_key(request.POST['key'])
        try:
            iv = base64.b64decode(encoded_text[:24])
            ct = base64.b64decode(encoded_text[24:])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decoded_text = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        except (ValueError, KeyError):
            decoded_text = "Invalid encoded text or key"
        return render(request, 'encoder/index.html', {'decoded_text': decoded_text})
    return render(request, 'encoder/index.html')
