from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Function to generate a random key
def generate_random_key(length=32):
    return os.urandom(length)

# Function to encrypt a file
def encrypt_file(input_file: str, output_file: str):
    # Generate a random key
    key = generate_random_key()
    
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    
    # Create an AES Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Read the input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # Pad the plaintext to be a multiple of the block size (128 bits for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Write the IV and ciphertext to the output file
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)
    
    # Print the key for later decryption
    print(f"Encryption key (keep this safe): {key.hex()}")

# Function to decrypt a file
def decrypt_file(input_file: str, key: str, output_file: str):
    # Convert the key from hex to bytes
    key = bytes.fromhex(key)
    
    # Read the input file
    with open(input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    
    # Create an AES Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    # Write the plaintext to the output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)

if __name__ == "__main__":
    # Example usage
    
    # Encrypt a file
    input_file = "IMG_6701.jpg"
    encrypted_file = "image.enc"
    decrypt_file_path = "example_decrypted.jpg"
    
    # encrypt_file(input_file, encrypted_file)
    
    # Decrypt the file
    # The key should be copied from the output of the encryption step
    key = input("Enter the encryption key to decrypt the file: ")
    decrypt_file(encrypted_file, key, decrypt_file_path)
    print(f"File decrypted and saved as {decrypt_file_path}")
