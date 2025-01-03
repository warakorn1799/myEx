from javax.crypto import Cipher, KeyGenerator
from java.security import KeyFactory
from java.security.spec import X509EncodedKeySpec, PKCS8EncodedKeySpec
from javax.crypto.spec import SecretKeySpec, IvParameterSpec, GCMParameterSpec
from java.util import Base64
import base64

class AESECB:
    def encrypt(self, plaintext, base64_key):
        key = base64.b64decode(base64_key)
        secret_key = SecretKeySpec(key, "AES")
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext, base64_key):
        key = base64.b64decode(base64_key)
        secret_key = SecretKeySpec(key, "AES")
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, secret_key)
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class AESCBC:
    def encrypt(self, plaintext, base64_key, iv):
        key = base64.b64decode(base64_key)
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
        cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key, iv_spec)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, ciphertext, base64_key, iv):
        key = base64.b64decode(base64_key)
        decoded_bytes = base64.b64decode(ciphertext)
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
        cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, secret_key, iv_spec)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class AESGCM:
    def encrypt(self, plaintext, base64_key, iv):
        key = base64.b64decode(base64_key)
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
        cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key, iv_spec)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, ciphertext, base64_key, iv):
        key = base64.b64decode(base64_key)
        decoded_bytes = base64.b64decode(ciphertext)
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
        cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, secret_key, iv_spec)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class RSA:
    def load_public_key_from_base64(self, base64_key):
        key_bytes = base64.b64decode(base64_key)
        key_spec = X509EncodedKeySpec(key_bytes)
        key_factory = KeyFactory.getInstance("RSA")
        return key_factory.generatePublic(key_spec)

    def load_private_key_from_base64(self, base64_key):
        key_bytes = base64.b64decode(base64_key)
        key_spec = PKCS8EncodedKeySpec(key_bytes)
        key_factory = KeyFactory.getInstance("RSA")
        return key_factory.generatePrivate(key_spec)

    def encryptRAW(self, public_key, plaintext):
        cipher = Cipher.getInstance("RSA/ECB/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, public_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decryptRAW(self, private_key, ciphertext):
        cipher = Cipher.getInstance("RSA/ECB/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, private_key)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = cipher.doFinal(encrypted_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

    def encryptPKCS1(self, public_key, plaintext):
        cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding")
        cipher.init(Cipher.ENCRYPT_MODE, public_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decryptPKCS1(self, private_key, ciphertext):
        cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding")
        cipher.init(Cipher.DECRYPT_MODE, private_key)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = cipher.doFinal(encrypted_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

    def encryptOAEP_SHA256(self, public_key, plaintext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")
        cipher.init(Cipher.ENCRYPT_MODE, public_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decryptOAEP_SHA256(self, private_key, ciphertext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")
        cipher.init(Cipher.DECRYPT_MODE, private_key)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = cipher.doFinal(encrypted_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")
    
    def encryptOAEP_SHA384(self, public_key, plaintext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-384AndMGF1Padding")
        cipher.init(Cipher.ENCRYPT_MODE, public_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decryptOAEP_SHA384(self, private_key, ciphertext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-384AndMGF1Padding")
        cipher.init(Cipher.DECRYPT_MODE, private_key)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = cipher.doFinal(encrypted_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")
    
    def encryptOAEP_SHA512(self, public_key, plaintext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-512AndMGF1Padding")
        cipher.init(Cipher.ENCRYPT_MODE, public_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decryptOAEP_SHA512(self, private_key, ciphertext):
        cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-512AndMGF1Padding")
        cipher.init(Cipher.DECRYPT_MODE, private_key)
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = cipher.doFinal(encrypted_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")
