import hashlib, base64

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

def cutter(listkey, listval):
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
    
    return hash_nums_map

cutter(user_pass_dic.keys(), user_pass_dic.values())

# پسوردم اصلی رو جوری تغییر میده به عدد پیدا شده b85 تا بعدش بتونم یوزر و پسورد رو از هشش بیرون بکشم
