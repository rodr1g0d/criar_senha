import secrets
import string

# Gera uma senha forte com 20 caracteres import as libs e seja feliz
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(20))
password

print(password)

# https://c340-187-101-169-197.ngrok-free.app
