from cryptography.fernet import Fernet
import os

class EncryptionUtility:
    def __init__(self, secret_key=None):
        if secret_key:
            self.key = secret_key
        else:
            self.key = self.load_or_generate_key()

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def load_key():
        return os.getenv("SECRET_KEY").encode() if os.getenv("SECRET_KEY") else None

    def load_or_generate_key(self):
        loaded_key = self.load_key()
        if loaded_key:
            return loaded_key
        else:
            generated_key = self.generate_key()
            os.environ["SECRET_KEY"] = generated_key.decode()  # Store as environment variable
            return generated_key

    def encrypt_data(self, data):
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data.encode()).decode()


    @staticmethod
    def encrypt_file(file_path, output_file_path):
        """
        Encrypts the contents of a file and writes the encrypted data to another file.

        Args:
            file_path (str): The path to the input file.
            output_file_path (str): The path to the output file where the encrypted data will be written.
        """

        with open(file_path, 'rb') as file:
            data = file.read()

        encrypted_data = EncryptionUtility.encrypt_data(data)

        with open(output_file_path, 'wb') as output_file:
            output_file.write(encrypted_data)


# Example usage
if __name__ == "__main__":
    encryption_utility = EncryptionUtility()

    # Example data
    config_data = "SENSITIVE_DATA_TO_BE_PROTECTED"

    # Encrypt data
    encrypted_data = encryption_utility.encrypt_data(config_data)
    print("Encrypted Data:", encrypted_data)

    # Decrypt data
    decrypted_data = encryption_utility.decrypt_data(encrypted_data)
    print("Decrypted Data:", decrypted_data)
