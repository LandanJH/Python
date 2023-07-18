# this script takes in a file with dcc2 hashes and clenses the hash for ease of use
#import argparse 
#import colorama
import os

###################################################################################
#                                                                                 #
#     could use arg parse to add a file argument as well as a way to specify      #
#                   which kind of hash that is in the file                        #
#                                                                                 #
###################################################################################


def list_to_file(list, name):
    file = open( name+'.cleaned', 'w')
    for items in list:
        file.write(items+"\n")
    file.close()

# start of the main program
hash_list = []          # list of uncleaned hashes
cleaned_hashes = []     # list of cleaned hashes
tmp_hashes = []

# taking in the file name
print('Please enter the file name:')
input = input()

# Checking to make sure the file exists
if (os.path.exists(input) == True):
    # open the file and add each hash into a list
    print('Starting Clense...')
    with open(input) as file:
        hash_list = file.readlines()
    # going through the list and cleaning the hashes
    for x in range(len(hash_list)):
        hash = hash_list[x]
        tmp = hash[hash.find('$'):]
        tmp_hashes.append(tmp)
        # this bit removes the newline characters
        cleaned_hashes = [
            item.replace('\r', '').replace('\n','')
            for item in tmp_hashes              
        ]
    # go through list and remove the duplicates
    cleaned_hashes = list(dict.fromkeys(cleaned_hashes))
    print(cleaned_hashes)
    # closing the file and printing out the filteres hashes
    file.close()
    # send the list to the 'list_to_file' function
    list_to_file(cleaned_hashes, input)

    for hash in cleaned_hashes:
        print(hash)
# just in case you put in the wrong file name
else:  
    print('file does NOT exist')
