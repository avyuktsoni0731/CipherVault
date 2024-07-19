from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


class Encryptor():
    # Function to generate a random key
    def generate_random_key(length=32):
        return os.urandom(length)

    # Function to encrypt a file
    def encrypt_file(input_file: str, output_file: str):
        # Generate a random key
        key = Encryptor.generate_random_key()
        
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
        with open(f'{output_file}.enc', 'wb') as f:
            f.write(iv + ciphertext)
        
        # Print the key for later decryption
        print(f"Encryption key (keep this safe): {key.hex()}")

    # Function to decrypt a file
    def decrypt_file(input_file: str, key: str, output_file: str):
        try:
            
            print(f'Input File: {input_file}\nKey: {key}')
            
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
        except:
            print('Incorrect Key!')

if __name__ == "__main__":
    # # Example usage
    
    
    # # Encrypt a file
    # input_file = '../test-data/spectreseek.png'
    # filename = os.path.basename(input_file)
    # print(input_file + '.enc')
    # print(filename+'.enc')
    # # encrypted_file = f'../test-data/{filename}'
    # # new_filename = filename.split('.')[0]+'.'+filename.split('.')[-2]

    # # print(new_filename)

    # # decrypt_file_path = f'{new_filename}'

    # # Encryptor.encrypt_file(input_file, input_file)
    
    # # Decrypt the file
    # # The key should be copied from the output of the encryption step
    # key = input("Enter the encryption key to decrypt the file: ")
    # Encryptor.decrypt_file(input_file + '.enc', key, './')
    # # print(f"File decrypted and saved as .")
    
        # Example usage
    
    # Encrypt a file
    input_file = "../test-data/spectreseek.png"
    filename = os.path.basename(input_file)
    # print(filename)
    # encrypted_file = "example.enc"
    decrypt_file_path = f"../test-data/decrypted/{filename}"
    
    # Encryptor.encrypt_file(input_file, input_file)
    
    # Decrypt the file
    # The key should be copied from the output of the encryption step
    key = "256225049a46cf75805d9d58dbad4728cfad7d92457fb7ec794dfa8bc36072f0"
    # key = input("Enter the encryption key to decrypt the file: ")
    Encryptor.decrypt_file('/var/folders/5v/2qxxqd7d041gd2pwzqr0lkvw0000gn/T/tmp5irq0mdy/IMG_5733.JPG.enc', key, decrypt_file_path)
    # Encryptor.decrypt_file(input_file + '.enc', key, decrypt_file_path)
    # print(f"File decrypted and saved as {decrypt_file_path}")