from itertools import product
import string

min_len = int(input("Enter the minimum length of the word in the wordlist: "))
max_len = int(input("Enter maximum length of the word in the wordlist: "))
counter = 0
character = string.ascii_lowercase+string.ascii_uppercase+string.digits+string.punctuation

file_open = open("generated_wordlist.txt",'w')

for i in range(min_len,max_len+1):
    for j in product(character,repeat=i):
        word = "".join(j)
        file_open.write(word)
        file_open.write('\n')
        counter+=1
print("Wordlist of {} words created".format(counter))