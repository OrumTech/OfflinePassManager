import hashlib, base64
import random
import string

user_pass_dic = {}
while True:
    try:
        user_name_pass = input("write your username and password and seperated with comma or k for last changes:")
        if user_name_pass == "k":
            break
        user_name_pass = [i.strip() for i in user_name_pass.split(",")]
        user_pass_dic[user_name_pass[0]] = user_name_pass[1]
    except:
        print("please enter only user and pass or k")

print(user_pass_dic)

def hash_finder(listkey, listval):
    keys = [0]
    for i in listkey:
        keys.append(i + str(keys[0]))
        del keys[0]
    vals = [0]
    for i in listval:
        vals.append(i + str(vals[0]))
        del vals[0]

    item = keys[0] + vals[0]
    key_list_of_dic = {i for i in item}

    check = False
    hash_nums_map = []

    for num_part in range(1, len(list(key_list_of_dic))+1):
        if check == True:
            break
        if len(list(key_list_of_dic)) % num_part == 0:
            part_size = len(list(key_list_of_dic)) // num_part
            chunk = [set(list(key_list_of_dic)[i:i+part_size]) for i in range(0, len(list(key_list_of_dic)), part_size)]
            print(chunk)

            for n in range(len(chunk)):
                for s in range(100, 10000):
                    b85 = base64.b85encode(hashlib.sha512(str(s).encode()).digest()).decode()
                    if all(c in b85 for c in chunk[n]):
                        print('Found:', s, b85)
                        hash_nums_map.append(s)
                        check = True
                        break
    
    return list(set(hash_nums_map))

def master_pass_set(minimum_char):
    while True:
        master_password = input(f"Enter your password with {minimum_char} characters or exit")
        if master_password == "exit":
            break
        if minimum_char <= len(str(master_password)):
            print("your password Succesfully Saved")
            return master_password
            break
        else:
            print(f"your password too small, must be minimum {minimum_char} character")    

# def create_fake_dict(length, char_set, min_val=0, max_val=10):
#     fake_dict = {}
#     while len(fake_dict) < length:
#         key = random.choice(char_set)
#         value = random.randint(min_val, max_val)
#         fake_dict[key] = value   # اگر کلید تکراری باشد، طول تغییری نمی‌کند
#     return fake_dict

def mapping(hash_num_maps:list, master_password:str, hash_length:int):
    new_master_pass = [str(i) for i in master_password]
    new_master_pass = new_master_pass[:hash_length]
    list_of_tables = [] #>>> [{},{},...]
    randomize_cache = {} #>>> {1:2 , @:3 , ...Real    Fake 3:4} >>> random to list of tables
    all_chars = string.ascii_letters + string.digits + string.punctuation

    for number in range(len(hash_num_maps)):
        for hass , maspas in zip(str(hash_num_maps[number]), new_master_pass.copy()):
            randomize_cache[maspas] = hass
            del new_master_pass[new_master_pass.index(maspas)]

        while len(randomize_cache) < 50:
            key = random.choice(all_chars)
            if key not in randomize_cache:
                value = random.randint(0, 9)
                randomize_cache[key] = value

        items = list(randomize_cache.items()) 
        random.shuffle(items)
        shuffled_dict = dict(items)
        list_of_tables.append(shuffled_dict)
    
    # for _ in range(hallucinator_table):
    #     fake_dict = create_fake_dict(30, all_chars, 0, 10)
    #     list_of_tables.append(fake_dict)

    # random.shuffle(list_of_tables)

    return list_of_tables




# _______________________________________________________Run

# lol = hash_finder(user_pass_dic.keys(), user_pass_dic.values())

# pass_check = ""
# for i in lol:
#     pass_check += str(i)

# my_password = master_pass_set(len(pass_check))
# print(lol)
# list_of_encrypted = mapping(lol, my_password, len(pass_check))

# پسوردم اصلی رو جوری تغییر میده به عدد پیدا شده b85 تا بعدش بتونم یوزر و پسورد رو از هشش بیرون بکشم
