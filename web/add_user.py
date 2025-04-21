from crypto import compute_data_hash
import os

new_user = input("Enter new user: ")
new_pass = input("Enter new password: ")
new_pass_hash = compute_data_hash(new_pass)

new_user_data = ':'.join([new_user, new_pass_hash])

with open("pwfile_hash.txt", "w") as file:
    file.write(new_user_data)