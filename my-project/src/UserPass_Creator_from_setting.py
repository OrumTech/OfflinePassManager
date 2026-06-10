from setting import *
import hashlib
import base64

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


# ------------------------------------------------------------- Recall to user and pass
# for lis in keys_index_tuple:
#     username = ""
#     for user in lis: 
#         indx, has = user
#         char = has[indx]
#         username += char
#     print(username)

# for lis in values_index_tuple:
#     password = ""
#     for user in lis: 
#         indx, has = user
#         char = has[indx]
#         password += char
#     print(password)

# باید ایندکس ها رو جایی ذخیره کنم.
# بعد از زدن پسورد اصلی هشی تولید میشه که با توجه به اینکه هش درست هست یا نه ساخت به ایندکس کد درست رو میده