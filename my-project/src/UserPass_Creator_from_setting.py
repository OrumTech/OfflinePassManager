from setting import *

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

print(user_input_to_hash)
# 15 OK
for i in user_input_to_hash:
    hash_num = ''
    for char in i:
        hash_num += str(list_of_encrypted[user_input_to_hash.index(i)].get(char))
    hash_num = int(hash_num)
    print(hash_num)