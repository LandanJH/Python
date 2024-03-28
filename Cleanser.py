#!/bin/python3

import os
import re
import argparse
from typing import List

class User:
    def __init__(self, username, password, hash):
        self.username = username
        self.password = password
        self.hash = hash

def list_to_file(list, name): #done
#Function to take a list and puth the list in a file line-by-line
    file = open( name+'.cleaned', 'w')
    for items in list:
        file.write(items+"\n")
    file.close()
    print('Cleaning finished output will be in the file named', name+'.cleaned')    #also might be part of the problem

def Rem_Duplicates(hashes): #done
# Function ot remove the duplicates from a list
    hashes = list(dict.fromkeys(hashes))
    return (hashes)

def File_Clenser(input):            # might want to make sure that I can get NTLM hashes from this function
#Function to go through a file of DCC2 hashes and clean them up
    hash_list = []          # list of uncleaned hashes
    
    # Checking to make sure the file exists
    if (os.path.exists(input) == True):
        # open the file and add each hash into a list
        print('Starting Clense...')         #I'm assuming that this is part of the problem for the printing
        with open(input) as file: 
            hash_list = file.readlines()
        # clean the hashes from the list
        List_Cleanser(hash_list, 'tmp')
        # closing the file
        file.close()
    # just in case you put in the wrong file name
    else:  
        print('file does NOT exist')

def Secrets_Parser(input, pattern):
# Function to go through secrets folders and pull hashes
    hashes = []
    if (os.path.exists(input) == True):
        # open the file and starting to retrieve the DCC2 and NTLM hashes
        print('Starting parse...')          #I'm assuming this is part of the problem for the printing
        with open(input) as file:
            content = file.readlines()
        # Pull the hashes
        hashes = Pattern_Parser(content, pattern) 
    return hashes

def List_Cleanser (hash_list, input):       # might need to make sure that this function can parse NTLM
# Function to clean a list of dcc2 hashes
    tmp_hashes = []         # temporary placeholder
    tmp_hashes = Pattern_Parser (hash_list, pattern_DCC2)
    # go through the list and remove null bytes
    cleaned_hashes = Remove_null(tmp_hashes)
    # go through list and remove the duplicates
    cleaned_hashes = Rem_Duplicates(cleaned_hashes)
    # send the list to the 'list_to_file' function
    list_to_file(cleaned_hashes, input)

def Directory_Parser(pattern, directory, mode):
# this function will go through a directory and parse all the information from all the files
    hashes2 = []
    fileslist =  os.listdir(directory)
    for file in fileslist:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            hashes = Secrets_Parser(file_path, pattern)
            hashes2 = hashes + hashes2
        if (mode == 'DCC2'):
            List_Cleanser(hashes2, 'secretdumps.DCC2')
        else:
            hashes2 = Rem_Duplicates(hashes2)
            list_to_file(hashes2, 'secretdumps.NTLM')

def Match(hashes, cracked, pattern_HASH, pattern_CRACKED):
# This function will take the file of cracked passwords from hashcat and the NTLM files and match the username to the password
    if (os.path.isfile(hashes) == True and os.path.isfile(cracked) == True):
        # grabbing the hashes and cracked passwords from the input files
        print('Grabbing hashed to be matched')
        with open(hashes) as file:
            hashes_from_file = file.readlines()
            hashes_from_file = Remove_null(hashes_from_file)
            nonCracked_hash, nonCracked_username = Match_Parser(hashes_from_file, pattern_HASH)
            file.close()
        print('Grabbing cracked passwords')
        with open(cracked) as file:
            cracked_from_file = file.readlines()
            cracked_from_file = Remove_null(cracked_from_file)
            isCracked_hash, isCracked_password = Match_Parser(cracked_from_file, pattern_CRACKED)
            file.close()
    else:
        print('Cracked hash or Hash file does not exist, please check the filename')
    Matching(isCracked_hash, isCracked_password, nonCracked_hash, nonCracked_username)

def Remove_null(list): # done
# This function removes the null byte at the end of an item in a list
    list = [
        item.replace('\r', '').replace('\n','') for item in list              
    ]
    return list

def Pattern_Parser(list, pattern):
# This function uses regular expression to fing NTLM or DCC2 hashes and returns the hashes in a list
    hashes = []
    for x in range (len(list)):
        tmp = list[x]
        #if(pattern == '(\$DCC2\$)(.*)' or pattern == '(.*?):(.*?):(.*?):(.*?):::'): #DCC2 or NTLM
        regex = re.compile(pattern)
        hash = regex.search(tmp)
        if(hash !=  None):
            hashes.append(hash[0])
    return hashes

def Match_Parser (list, pattern):
# Function to grab the hash username and password information and return lists containing that information
    hashList = []
    otherList = []
    for x in range (len(list)):
        tmp = list[x]
        regex = re.compile(pattern)
        hash = regex.search(tmp)
        if (pattern == '(.*?):(.*)(.*):(.*):::'): # non cracked hash 
            hashList.append(hash[4]) # should relate to the hash
            otherList.append(hash[1]) # should relate to the username
        elif (pattern == '(.*?):(.*)'): # cracked hash
            hashList.append(hash[1]) # should relate to the hash
            otherList.append(hash[2]) # should relate to the password
        else:
            print('something went wrong')
    return hashList, otherList
        
# For the regex for the matching function
#   Hashes
#       group 1: username
#       group 4: hash
#
#   cracked
#       group 1: hash
#       group 2: password

def Matching (isCracked_hash, isCracked_password, nonCracked_hash, nonCracked_username):
    for y in range (len(nonCracked_hash)):
        for x in range (len(isCracked_hash)):
            if (isCracked_hash[x] == nonCracked_hash[y]):
                if(isCracked_password[x] == ''):
                    isCracked_password[x] = '(NO_PASSWORD_DATA)'
                crackedAccount = User(nonCracked_username[y], nonCracked_hash[y], isCracked_password[x])
                userList.append(crackedAccount)
    userList_to_file()

def userList_to_file():
    file = open( 'Credentials', 'w')
    for x in range (len(userList)):
        file.write(userList[x].username+"   ")
        file.write(userList[x].hash+"   ")
        file.write(userList[x].password + "\n")
    file.close()
    print('Cleaning finished output will be in the file named Credentials')

def relay_Parser(relayFile):
    # Checking to make sure the file exists
    if (os.path.exists(relayFile) == True):
        try:
            data = {}
            with open(relayFile) as file:
                for line in file.readlines():
                    split = line.split(":")
                    if split[0] not in data.keys():
                        data[split[0]] = line
            for k in data.keys():
                print(data[k].strip(), end='\n')
        except Exception as e:
            print(str(e))
    

    
if __name__ == "__main__":
    # Userlist for the matching part of the program
    userList: List[User] = []

    # Argument parcer stuff
    parser = argparse.ArgumentParser(description='Hash cleaner for the Domain Caches Credentials 2 hash type')
    parser.parse_args
    parser.add_argument('-d', '--DIRECTORY', type=str, help='Directory path of the files with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-f', '--FILE', type=str, help='File path of the file with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-m', '--MODE', type=str, help='Type of hash to be found from secretsdump files DCC2 or NTLM', default=None)
    parser.add_argument('-M', '--MATCH', type=str, help='Match the cracked password with the user of that password', default=None)
    parser.add_argument('-s', '--SECRETS', type=str, help='Path of the file with the secret dump hashes', default=None)
    parser.add_argument('-r', '--RELAY', type=str, help='Path of the relay_HashType file that responder dumps hashes to', default=None)
    args = parser.parse_args()

    # Regex patterns
    pattern_DCC2 = r"(\$DCC2\$)(.*)"            
    pattern_NTLM = r"(.*?):(.*?):(.*?):(.*?):::"
    pattern_HASH = r"(.*?):(.*)(.*):(.*):::"        # need to capture groups 1 for the username and 4 for the hash
    pattern_CRACKED= r"(.*?):(.*)"                  # for use with the cracked password file group 1 is the hash and group 2 is the username

    if (args.FILE == None and args.SECRETS == None and args.DIRECTORY == None and args.RELAY == None): 
        print('Please be sure to include the filename: -f [FILENAME]')
    elif(args.SECRETS != None):
        if (args.MODE == 'DCC2'):
            hashes = Secrets_Parser(args.SECRETS, pattern_DCC2 )
            List_Cleanser(hashes, 'secretdumps.DCC2')
        elif (args.MODE == 'NTLM'):
            hashes = Secrets_Parser(args.SECRETS, pattern_NTLM )
            hashes = Rem_Duplicates(hashes)
            list_to_file(hashes, 'sectretsdump.NTLM')
        else:
            print('Please specify the mode: -m [DCC2 / NTLM]')
    elif(args.DIRECTORY != None):
        if (args.MODE == 'DCC2'):
            Directory_Parser(pattern_DCC2, args.DIRECTORY, 'DCC2')
        elif (args.MODE == 'NTLM'):
            Directory_Parser(pattern_NTLM, args.DIRECTORY, 'NTLM')
        else:
            print('Please specify the mode: -m [DCC2 / NTLM]')
    elif(args.MATCH != None):
        if (args.MATCH == '' and args.FILE == ''):
            print('Please include the file with the NTLM hashes and the file with the cracked hashes')
        else:
            Match(args.FILE, args.MATCH, pattern_HASH, pattern_CRACKED)
    elif(args.RELAY != None):
        relay_Parser(args.RELAY)
    else:
        File_Clenser(args.FILE)
