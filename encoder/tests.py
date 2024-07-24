from django.test import TestCase
from django.urls import reverse
import base64
import hashlib

def get_key(key):
    return hashlib.sha256(key.encode()).digest()  # 256-bit key

class EncoderDecoderTests(TestCase):
    def test_encode_text(self):
        key = 'testkey'
        response = self.client.post(reverse('encode_text'), {'text': 'Hello, World!', 'key': key})
        key = get_key(key)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad('Hello, World!'.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        encoded_text = iv + ct
        self.assertContains(response, encoded_text)

    def test_decode_text(self):
        key = 'testkey'
        key_hash = get_key(key)
        cipher = AES.new(key_hash, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad('Hello, World!'.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        encoded_text = iv + ct
        response = self.client.post(reverse('decode_text'), {'encoded_text': encoded_text, 'key': key})
        self.assertContains(response, 'Hello, World!')

    def test_invalid_decode_text(self):
        response = self.client.post(reverse('decode_text'), {'encoded_text': 'InvalidEncodedText', 'key': 'testkey'})
        self.assertContains(response, 'Invalid encoded text or key')
