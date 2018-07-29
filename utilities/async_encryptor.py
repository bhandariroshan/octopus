from cryptography.fernet import Fernet

'''
    
    This class handles encryption and decryption of message using fernet algorithm.
    We will need, cipher to decode message once we encode it, so save the cipher once you generate it.
    
'''

class AsyncEncryptor(object):
    @staticmethod
    def generate_keys():
        """

        :return:
        """

        key = Fernet.generate_key()  # this is your "password"
        cipher_suite = Fernet(key)

        return cipher_suite

    @staticmethod
    def encrypt_message(message, cipher):
        try:
            encoded = cipher.encrypt(message.encode('utf-8'))
            return encoded
        except Exception as e:
            print(str(e))
            return ''

    @staticmethod
    def decrypt_message(message, cipher):
        try:
            decoded_text = cipher.decrypt(message.encode('utf-8'))
        except Exception as e:
            print(str(e))
            decoded_text = ''
        return decoded_text