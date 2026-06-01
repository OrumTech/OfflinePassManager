import hashlib
import base64
import os

user = input("pass1")

hash_sha = hashlib.sha256(user.encode()).hexdigest()
passw = "59e2f402d3a3da68fa5f597bd7f8a64ee1108fb4ab00be51aa6bd88b9cc66951"

encoder1 = {0:2, 1:6, 2:5, 3:8, 4:3, 5:6, 6:9, 7:2, 8:1, 9:8}
encoder2 = {0:5, 1:7, 2:3, 3:6, 4:7, 5:2, 6:8, 7:3, 8:2, 9:4}
encoder3 = {0:7, 1:4, 2:5, 3:6, 4:8, 5:4, 6:9, 7:2, 8:5, 9:3}
usersec = [int(d) for d in input("pass2: ")]

chunk1 , chunk2, chunk3 = usersec[:4], usersec[4:8], usersec[8:]
chunk11 = [encoder1.get(i) for i in chunk1]
ps1 = str(chunk11[0]) + str(chunk11[1]) + str(chunk11[2]) + str(chunk11[3])
chunk22 = [encoder2.get(i) for i in chunk2]
ps2 = str(chunk22[0]) + str(chunk22[1]) + str(chunk22[2]) + str(chunk22[3])
chunk33 = [encoder3.get(i) for i in chunk3]
ps3 = str(chunk33[0]) + str(chunk33[1]) + str(chunk33[2])

hash_sha2 = hashlib.sha256(ps1.encode()).digest()
hash_b641 = base64.b85encode(hash_sha2).decode()

hash_sha22 = hashlib.sha256(ps2.encode()).digest()
hash_b642 = base64.b85encode(hash_sha22).decode()

hash_sha222 = hashlib.sha256(ps3.encode()).digest()
hash_b643 = base64.b85encode(hash_sha222).decode()


print(hash_b641)
print(hash_b642)
print(hash_b643)

if os.path.getsize(r"D:\DockerFiles\Project\pass.py") == 2266:
    print("0K")

if hash_sha == passw:

    print("login succesfull")
    elname = hash_b643[20] + hash_b641[31] + hash_b641[20] + hash_b641[33] + hash_b643[20] + hash_b643[20] + hash_b641[33] + hash_b641[34] + "." + hash_b641[31
        ] + hash_b641[19] + hash_b641[5] + hash_b643[20] + hash_b642[23] + hash_b641[0] + hash_b643[13]
    elps = hash_b641[35] + hash_b643[0] + hash_b643[39] + hash_b643[34] + hash_b641[33] + hash_b643[28] + hash_b641[35] + hash_b642[13] + hash_b642[11] + hash_b641[34
        ] + hash_b641[33] + hash_b641[19] + hash_b641[35]
    print(f"your username is: {elname} and pass is {elps}")