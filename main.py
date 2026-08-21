import random
import string

def main():
    print("=== RANDOM PASSWORD GENERATOR ===")
    
    length = int(input("Enter password length (e.g., 8, 12): "))

    use_upper = input("Include Uppercase letters A-Z? (y/n): ").lower() == 'y'
    use_digits = input("Include Numbers 0-9? (y/n): ").lower() == 'y'
    use_special = input("Include Special symbols (!@#$)? (y/n): ").lower() == 'y'

    chars = string.ascii_lowercase

    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()-_"

    password = ""
    for _ in range(length):
        password += random.choice(chars)

    print("\n--------------------------------")
    print("Your Random Password is:", password)
    print("--------------------------------")

if __name__ == "__main__":
    main()
