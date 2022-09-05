from cryptography.fernet import Fernet
import os

print(type(os.getcwd()))
key = Fernet.generate_key()
file = open("encryption_key.txt", "wb")
file.write(key)
file.close()