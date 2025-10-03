import string
import random  # <-- this was missing

length = int(input("Enter password length: "))

letters = string.ascii_letters
numbers = string.digits
symbols = string.punctuation
all_chars = letters + numbers + symbols

password = ""
for _ in range(length):
    password += random.choice(all_chars)

print("Your password is: " + password)
