from javax.crypto import Cipher, KeyGenerator
from javax.crypto.spec import SecretKeySpec, IvParameterSpec, GCMParameterSpec
from java.util import Base64
import base64

class AESECB:
    def encrypt(self, plaintext, base64_key):
        key = base64.b64decode(base64_key)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        secret_key = SecretKeySpec(key, "AES")
	cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
	return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext, base64_key):
        key = base64.b64decode(base64_key)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        secret_key = SecretKeySpec(key, "AES")
	cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, secret_key)
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class AESCBC:
    def encrypt(self, plaintext, base64_key, iv):
        key = base64.b64decode(base64_key)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        if len(iv.encode('utf-8')) != 16:
            raise ValueError("Invalid IV size. IV must be 16 bytes.")
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
        cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key, iv_spec)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, ciphertext, base64_key, iv):
        key = base64.b64decode(base64_key)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        if len(iv.encode('utf-8')) != 16:
            raise ValueError("Invalid IV size. IV must be 16 bytes.")
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
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        if len(iv.encode('utf-8')) != 16:
            raise ValueError("Invalid IV size. IV must be 16 bytes.")
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
	cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, secret_key, iv_spec)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, ciphertext, base64_key, iv):
        key = base64.b64decode(base64_key)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes.")
        if len(iv.encode('utf-8')) != 16:
            raise ValueError("Invalid IV size. IV must be 16 bytes.")
        decoded_bytes = base64.b64decode(ciphertext)
        secret_key = SecretKeySpec(key, "AES")
        iv_spec = IvParameterSpec(iv.encode("utf-8"))
	cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, secret_key, iv_spec)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")
