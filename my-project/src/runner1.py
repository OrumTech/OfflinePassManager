from UserPass_Creator_from_setting1 import *
from setting1 import *
import json
import os
import sys
import hashlib
import base64
#-----------------------------------------------------------------SETTINGS
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    with open(resource_path('vault_data.json'), 'r') as f:
        data = json.load(f)
    list_of_encrypted = data['list_of_encrypted']
    chunk_num = data['chunk_num']
    keys_index = data['keys_index']
    values_index = data['values_index']
except FileNotFoundError:
    print("Corrupted executable: Missing payload.")
    sys.exit()

#-----------------------------------------------------------------CODE MAN

chunking = chunk_num
master_pass = [str(d) for d in input("enter your password: ")]

input_to_hash = []

for num in chunking:
    input_to_hash.append(master_pass[:num])
    del master_pass[:num]

# ------------------------------------------------------------

hash_li = []
i_hash_list = 0
for chunk in input_to_hash:
    new_gen_hash = ""
    for char in chunk:
        new_gen_hash += str(list_of_encrypted[i_hash_list].get(char))
        i_hash_list += 1
    new_gen_hash = int(new_gen_hash)
    hash_li.append(new_gen_hash)

# ------------------------------------------------------------

hash_lit = []
for has in hash_li:
    a = hashlib.sha512(str(has).encode()).digest()
    b = base64.b85encode(a).decode()
    hash_lit.append(b)

# ------------------------------------------------------------

index_of_keys = keys_index
index_of_values = values_index

print("\n--- Decrypted Data ---")
for lis in index_of_keys:
    username = ""
    for user in lis: 
        indx, has = user
        char = hash_lit[has][indx]
        username += char
    print(f"Username: {username}")

for lis in index_of_values:
    password = ""
    for user in lis: 
        indx, has = user
        char = hash_lit[has][indx]
        password += char
    print(f"Password: {password}")
    
input("\nPress Enter to exit...")