from javax.crypto import Cipher, KeyGenerator
from javax.crypto.spec import SecretKeySpec, IvParameterSpec, GCMParameterSpec
from java.util import Base64

class AESECB:
    def __init__(self, key_size):
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid key size. Supported sizes: 128, 192, 256.")
        self.keygen = KeyGenerator.getInstance("AES")
        self.keygen.init(key_size)
        self.secret_key = self.keygen.generateKey()
        print("Key (Base64):", Base64.getEncoder().encodeToString(self.secret_key.getEncoded()).decode('utf-8'))
        print("Key (Hex):", ''.join('{:02x}'.format(byte) for byte in self.secret_key.getEncoded()))

    def encrypt(self, plaintext):
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, self.secret_key)
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        print("Ciphertext (HEX):", ''.join('%02x' % byte for byte in encrypted_bytes))
	print("Ciphertext (BASE64):",Base64.getEncoder().encodeToString(encrypted_bytes))
        return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext):
        cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, self.secret_key)
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class AESCBC:
    def __init__(self, key_size):
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid key size. Supported sizes: 128, 192, 256.")
        self.keygen = KeyGenerator.getInstance("AES")
        self.keygen.init(key_size)
        self.secret_key = self.keygen.generateKey()
        self.iv = Cipher.getInstance("AES/CBC/PKCS5Padding").getParameters().getParameterSpec(IvParameterSpec).getIV()
        print("Key (Base64):", Base64.getEncoder().encodeToString(self.secret_key.getEncoded()).decode('utf-8'))
        print("Key (Hex):", ''.join('{:02x}'.format(byte) for byte in self.secret_key.getEncoded()))
	print("IV (Base64):", Base64.getEncoder().encodeToString(self.iv).decode('utf-8'))
	print("IV (Hex):", ''.join('{:02x}'.format(byte) for byte in self.iv))

    def encrypt(self, plaintext):
        cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, self.secret_key, IvParameterSpec(self.iv))
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        print("Ciphertext (HEX):", ''.join('{:02x}'.format(byte) for byte in encrypted_bytes))
	print("Ciphertext (BASE64):",Base64.getEncoder().encodeToString(encrypted_bytes))
        return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext):
        cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, self.secret_key, IvParameterSpec(self.iv))
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")

class AESGCM:
    def __init__(self, key_size):
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid key size. Supported sizes: 128, 192, 256.")
        self.keygen = KeyGenerator.getInstance("AES")
        self.keygen.init(key_size)
        self.secret_key = self.keygen.generateKey()
	self.iv = Cipher.getInstance("AES/CBC/NoPadding").getParameters().getParameterSpec(IvParameterSpec).getIV()
        print("Key (Base64):", Base64.getEncoder().encodeToString(self.secret_key.getEncoded()).decode('utf-8'))
        print("Key (Hex):", ''.join('{:02x}'.format(byte) for byte in self.secret_key.getEncoded()))
        print("IV (Base64):", Base64.getEncoder().encodeToString(self.iv).decode('utf-8'))
        print("IV (Hex):", ''.join('{:02x}'.format(byte) for byte in self.iv))

    def encrypt(self, plaintext):
        cipher = Cipher.getInstance("AES/GCM/NoPadding")
        iv = bytearray([0] * 12)
        cipher.init(Cipher.ENCRYPT_MODE, self.secret_key, GCMParameterSpec(128, iv))
        encrypted_bytes = cipher.doFinal(plaintext.encode("utf-8"))
        print("Ciphertext (HEX):", ''.join('%02x' % byte for byte in encrypted_bytes))
        print("Ciphertext (BASE64):",Base64.getEncoder().encodeToString(encrypted_bytes))
	return Base64.getEncoder().encodeToString(encrypted_bytes)

    def decrypt(self, ciphertext):
        cipher = Cipher.getInstance("AES/GCM/NoPadding")
        iv = bytearray([0] * 12)
        cipher.init(Cipher.DECRYPT_MODE, self.secret_key, GCMParameterSpec(128, iv))
        decoded_bytes = Base64.getDecoder().decode(ciphertext)
        decrypted_bytes = cipher.doFinal(decoded_bytes)
        return bytearray(decrypted_bytes).decode("utf-8")
