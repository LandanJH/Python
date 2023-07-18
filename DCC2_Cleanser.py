# this script takes in a file with dcc2 hashes and clenses the hash for ease of use
import os
import argparse

def list_to_file(list, name):
# prints a list to a file line by line
    file = open( name+'.cleaned', 'w')
    for items in list:
        file.write(items+"\n")
    file.close()

def Clenser(input):
# cleaner function
    hash_list = []          # list of uncleaned hashes
    cleaned_hashes = []     # list of cleaned hashes
    tmp_hashes = []         # temporary placeholder
    
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
        # closing the file and printing out the filteres hashes
        file.close()
        # send the list to the 'list_to_file' function
        list_to_file(cleaned_hashes, input)
    # just in case you put in the wrong file name
        print('Cleaning finished output will be in the file named', input+'.cleaned')
    else:  
        print('file does NOT exist')

# Argument parcer stuff
parser = argparse.ArgumentParser(description='Hash cleaner for the Domain Caches Credentials 2 hash type')
parser.parse_args
parser.add_argument('-f', type=str, help='Path of the file with the uncleaned DCC2 hashes', default=None)
args = parser.parse_args()

if (args.f == None):
    raise Exception('Please be sure to include the filename')
else:
    # taking in the file name
    print('Please enter the file name:')
    Clenser(args.f)
