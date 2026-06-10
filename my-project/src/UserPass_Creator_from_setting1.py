from setting1 import *
import hashlib
import base64
import json
import subprocess
import os

lol = hash_finder(user_pass_dic.keys(), user_pass_dic.values())

pass_check = ""
for i in lol:
    pass_check += str(i)

my_password = master_pass_set(len(pass_check))
list_of_encrypted = mapping(lol, my_password, len(pass_check))

user_input = [str(d) for d in input("pass: ")]

item_counter = 0
chunk_num = []

for code in lol:
    item_counter = 0
    for num in str(code):
        item_counter += 1
    chunk_num.append(item_counter)

user_input_to_hash = []

for num in chunk_num:
    user_input_to_hash.append(user_input[:num])
    del user_input[:num]

#------------------------------------------------------------ New 6/9/2026
hash_lis = []

i_hash_list = 0
for chunk in user_input_to_hash:
    new_gen_hash = ""
    for char in chunk:
        new_gen_hash += str(list_of_encrypted[i_hash_list].get(char))
        i_hash_list += 1
    new_gen_hash = int(new_gen_hash)
    hash_lis.append(new_gen_hash)
#------------------------------------------------------------ Exp -- > Updated
hash_list = []
for has in hash_lis:
    a = hashlib.sha512(str(has).encode()).digest()
    b = base64.b85encode(a).decode()
    hash_list.append(b)

#----------------------------------------------------------find and create The Username/Email and Password in hash
hash_dic = {}
for idx, has in enumerate(hash_list):
    hash_dic[has] = idx
#--------------//////\\\\\\
# Change This section:
# wich hash must append by a tuple in the keys_index and values_indes

keys_index_tuple = []
values_index_tuple = []
keys_index = []
values_index = []

for kw in user_pass_dic.keys(): # ['sdsd','sdsd', ...]
    uuu = []
    uui = []
    for char in kw:
        for idx, hash_str in enumerate(hash_list):
            pos = hash_str.find(char)
            if pos != -1:
                if len(uuu) > 0:
                    if (uuu[-1][1])[uuu[-1][0]] != hash_str[pos]:
                        uuu.append((pos,hash_str))
                        uui.append((pos,hash_dic.get(hash_str)))
                else:
                    uuu.append((pos,hash_str))
                    uui.append((pos,hash_dic.get(hash_str)))
    keys_index_tuple.append(uuu)
    keys_index.append(uui)

for kw in user_pass_dic.values(): # ['sdsd','sdsd', ...]
    ppp = []
    ppi = []
    for char in kw:
        for idx, hash_str in enumerate(hash_list):
            pos = hash_str.find(char)
            if pos != -1:
                if len(ppp) > 0:
                    if (ppp[-1][1])[ppp[-1][0]] != hash_str[pos]:
                        ppp.append((pos,hash_str))
                        ppi.append((pos,hash_dic.get(hash_str)))
                else:
                    ppp.append((pos,hash_str))
                    ppi.append((pos,hash_dic.get(hash_str)))
    values_index_tuple.append(ppp)
    values_index.append(ppi)

#---------------------------------------------------------------
print("\n[+] Setup Stage Completed.")
print("[+] Encrypting and saving payload map...")

vault_data = {
    "list_of_encrypted": list_of_encrypted,
    "chunk_num": chunk_num,
    "keys_index": keys_index,
    "values_index": values_index
}

with open('vault_data.json', 'w') as f:
    json.dump(vault_data, f)

print("[+] Compiling Secure Runner EXE (Please wait...)")

subprocess.run([
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--console",
    "--add-data", f"vault_data.json{os.pathsep}.",
    "runner1.py"
])

print("[+] Destroying setup traces (JSON file)...")

if os.path.exists('vault_data.json'):
    os.remove('vault_data.json')

print("\n=========================================")
print("[!] SUCCESS! Your standalone executable is ready.")
print("[!] You can find 'runner.exe' inside the 'dist' folder.")
print("=========================================")