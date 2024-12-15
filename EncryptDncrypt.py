from javax.crypto import Cipher, KeyGenerator
from javax.crypto.spec import SecretKeySpec
from java.util import Base64

class AESCipher:
    def __init__(self, key_size=128):
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid key size. Supported sizes: 128, 192, 256.")
        self.keygen = KeyGenerator.getInstance("AES")
        self.keygen.init(key_size)
        self.secret_key = self.keygen.generateKey()

    def encrypt(self, plaintext):
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, self.secret_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext):
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, self.secret_key)
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")