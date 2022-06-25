from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt_passowrd(message):
    """
    Encrypts a message
    """
    key = load_key()
    print("***************")
    print(key)
    print("***************")
    encoded_message = message.encode()
    print("@@@@@@@")
    print(encoded_message)
    print("@@@@@@@")
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message
  
def decrypt_passowrd(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()  
