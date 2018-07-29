from cryptography.fernet import Fernet
key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)
encoded_text = cipher_suite.encrypt("Hello stackoverflow!".encode('utf-8'))
print(encoded_text)
decoded_text = cipher_suite.decrypt(b'gAAAAABbXMPOCAhmqPy6vVqkK2ykVWFRutsFVb0maCSnZHJe-OhFEYml64ovvOg3f0EMUvDZpFN-R7rV8X-T9gvdFjoDyqhUeg==')
print(decoded_text)