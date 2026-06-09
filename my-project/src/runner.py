from UserPass_Creator_from_setting import *
from setting import *


decoder = list_of_encrypted
print(f"FROM RUNNER {decoder}")

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

# for user in range(len(index_of_keys)):
#     for num , has in zip(index_of_keys[user]):
#         pass

for lis in index_of_keys:
    username = ""
    for user in lis: 
        indx, has = user
        char = hash_lit[has][indx]
        username += char
    print(username)