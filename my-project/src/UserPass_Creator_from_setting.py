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

user_input = [int(d) for d in input("pass: ")]
item_counter = 0
chunk_num = []

for code in lol:
    item_counter = 0
    for num in code:
        item_counter += 1
    chunk_num.append(item_counter)

for num in chunk_num:
    chunk = user_input[:num]
    del user_input[:num]
    