from setting import *
import hashlib
import base64
import os

lol = hash_finder(user_pass_dic.keys(), user_pass_dic.values())

pass_check = ""
for i in lol:
    pass_check += str(i)

my_password = master_pass_set(len(pass_check))
print(lol)
list_of_encrypted = mapping(lol, my_password, len(pass_check))
print(list_of_encrypted)

# باید وقتی setting انجام شد و دیکشنری رو ساخت خودش رو از بین ببره
# بعد از ساخت encrypt dic, chunk pass, map to chunk to dic, user passes caller

user_input = [str(d) for d in input("pass: ")]
# تا اینجا درسته خط 14 pass میشه. بعدش اینا باید حذف بشند.
item_counter = 0
chunk_num = []

for code in lol:
    item_counter = 0
    for num in str(code):
        item_counter += 1
    chunk_num.append(item_counter)

print(chunk_num)
user_input_to_hash = []

for num in chunk_num:
    user_input_to_hash.append(user_input[:num])
    del user_input[:num]

print(f"IIIIIIIIIIIII {user_input_to_hash}")
# 15 OK
hash_num_list = []
for i in user_input_to_hash:
    hash_num = ''
    for char in i:
        hash_num += str(list_of_encrypted[user_input_to_hash.index(i)].get(char))
    # hash_num = int(hash_num)
    hash_num_list.append(hash_num)

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
print(f"JJJJJJJJJJJJJJJJJ {hash_lis}")
#------------------------------------------------------------ Exp
hash_list = []
for has in hash_num_list:
    a = hashlib.sha512(has.encode()).digest()
    b = base64.b85encode(a).decode()
    hash_list.append(b)

print(hash_list)
#----------------------------------------------------------find and create The Username/Email and Password in hash
uuu = []
ppp = []
print(user_pass_dic)
for kw in user_pass_dic.keys(): # ['sdsd','sdsd', ...]
    for char in kw:
        for idx, hash_str in enumerate(hash_list):
            pos = hash_str.find(char)
            if pos != -1:
                uuu.append((pos,hash_str))

for kw in user_pass_dic.values(): # ['sdsd','sdsd', ...]
    for char in kw:
        for idx, hash_str in enumerate(hash_list):
            pos = hash_str.find(char)
            if pos != -1:
                ppp.append((pos,hash_str))

print(uuu)
print(ppp)

# همین الان فهمیدم که من دیکشنری ناشت مستر پسورد به عدد هش رو ندارم !
# بلکه دیکشنری کلید به مقدار یوز و پسورد ها رو دارم!!
# شایدم نمی دونم ؛ باید برسسی کنم