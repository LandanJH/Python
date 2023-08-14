import os
import re
import argparse

def list_to_file(list, name):
#Function to take a list and put the list in a file line-by-line
    file = open( name+'.cleaned', 'w')
    for items in list:
        file.write(items+"\n")
    file.close()
    print('Cleaning finished output will be in the file named', name+'.cleaned')    #also might be part of the problem

def Rem_Duplicates(hashes):
# Function ot remove the duplicates from a list
    hashes = list(dict.fromkeys(hashes))
    return (hashes)

def File_Clenser(input):                    # Apperently this function isn't using the regular expression needed for DCC2 hashes
#Function to go through a file of DCC2 hashes and clean them up
    hash_list = []          # list of uncleaned hashes
    cleaned_hashes = []     # list of cleaned hashes
    tmp_hashes = []         # temporary placeholder
    
    # Checking to make sure the file exists
    if (os.path.exists(input) == True):
        # open the file and add each hash into a list
        print('Starting Clense...')         #I'm assuming that this is part of the problem for the printing
        with open(input) as file:
            hash_list = file.readlines()
        # going through the list and cleaning the hashes
        for x in range(len(hash_list)):
            hash = hash_list[x]
            tmp = hash[hash.find('$'):]
            tmp_hashes.append(tmp)
            # this bit removes the newline characters
            cleaned_hashes = Remove_null(tmp_hashes)

        # go through the list and remove the duplicates
        cleaned_hashes = Rem_Duplicates(cleaned_hashes)
        # closing the file
        file.close()
        # send the list to the 'list_to_file' function
        list_to_file(cleaned_hashes, input)
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
        print('here')
        hashes = Pattern_Parser(content, pattern) 

    #might need the below code incase I break Something
#        for x in range (len(content)):
#            hash = re.finditer(pattern, content[x])
#            for match in hash:
#                hashes.append(match.group())

    return hashes

def List_Cleanser (hash_list, input):
# Function to clean a list of dcc2 hashes
    tmp_hashes = []         # temporary placeholder

    for x in range(len(hash_list)):
        hash = hash_list[x]
        tmp = hash[hash.find('$'):]
        tmp_hashes.append(tmp)
        # this bit removes the newline characters
        cleaned_hashes = Remove_null(tmp_hashes)

    # Keeping the code below just in case I messed this up somewhere
#        cleaned_hashes = [
#            item.replace('\r', '').replace('\n','')
#            for item in tmp_hashes              
#        ]

    # go through list and remove the duplicates
    cleaned_hashes = Rem_Duplicates(cleaned_hashes)
    # send the list to the 'list_to_file' function
    list_to_file(cleaned_hashes, input)

def Directory_Parser(pattern, directory, mode):
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
# This function will take the file of cracked passwods from hashcat and the NTLM files and match the username to the password
    hashes_from_file = []
    cracked_from_file = []
    if (os.path.isfile(hashes) == True and os.path.isfile(cracked) == True):
        # grabbing the hashes and cracked passwords from the input files
        print('Grabbing hashed to be matched')
        with open(hashes) as file:
            hashes_from_file = file.readlines()
            hashes_from_file = Remove_null(hashes_from_file)
            hashes_from_file = Pattern_Parser(hashes_from_file, pattern_HASH)
            #print(hashes_from_file)
            file.close()
        print('Grabbing cracked passwords')
        with open(cracked) as file:
            cracked_from_file = file.readlines()
            cracked_from_file = Remove_null(cracked_from_file)
            cracked_from_file = Pattern_Parser(cracked_from_file, pattern_CRACKED)
            #print(cracked_from_file)
            file.close()
    else:
        print('Cracked hash or Hash file does not exist, please check the filename')

def Remove_null(list):
# This function removes the null byte at the end of an item in a list
    list = [
        item.replace('\r', '').replace('\n','') for item in list              
    ]
    return list

def Pattern_Parser(list, pattern):
# This function SHOULD go through a list and parse based on the regex pattern (MIGHT NOT WORK PROPERLY ATM)
############################################################
    class User:
        def __init__(self, username, password, hash):
            self.username = []
            self.password = []                                  #this section is in the wrong function but will fix later
            self.hash = []
    Users = [
        User("mary", "Password1!", "somerandomhash")
    ]
############################################################

    hashes = []
    for x in range (len(list)):
        tmp = list[x]
        if(pattern == '(\$DCC2\$)(.*)' or pattern == '(.*?):(.*?):(.*?):(.*?):::'): #DCC2 or NTLM
            regex = re.compile(pattern)
            hash = regex.search(tmp)
            if(hash !=  None):
                hashes.append(hash[0])
        else:
            Matches = [] # 2-D array that will hold the username, hash, and password information that will be put into a file [username], [hash], [password]
            tmp = list[x]
            regex = re.compile(pattern)
            hash = regex.search(tmp)
            #print(hash[4])
            
#        for match in hash:
            #hashes.append(match.group())
#            list.append(match.group())
    for user in Users:
        print(user.username)
        print(user.password)
        print(user.hash)
    return hashes
        
# For the regex for the matching function
#   Hashes
#       group 1: username
#       group 4: hash
#
#   cracked
#       group 1: hash
#       group 2: password
    
if __name__ == "__main__":
    # Argument parcer stuff
    parser = argparse.ArgumentParser(description='Hash cleaner for the Domain Caches Credentials 2 hash type')
    parser.parse_args
    parser.add_argument('-d', '--DIRECTORY', type=str, help='Directory path of the files with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-f', '--FILE', type=str, help='File path of the file with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-m', '--MODE', type=str, help='Type of hash to be found from secretsdump files DCC2 or NTLM', default=None)
    parser.add_argument('-M', '--MATCH', type=str, help='Match the cracked password with the user of that password', default=None)
    parser.add_argument('-s', '--SECRETS', type=str, help='Path of the file with the secret dump hashes', default=None)
    args = parser.parse_args()

    # Regex patterns
    pattern_DCC2 = r"(\$DCC2\$)(.*)"            
    pattern_NTLM = r"(.*?):(.*?):(.*?):(.*?):::"
    pattern_HASH = r"(.*?):(.*)(.*):(.*):::"        # need to capture groups 1 for the username and 4 for the hash
    pattern_CRACKED= r"(.*?):(.*)"                  # for use with the cracked password file group 1 is the hash and group 2 is the username

    if (args.FILE == None and args.SECRETS == None and args.DIRECTORY == None):
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
    else:
        File_Clenser(args.FILE)


    #currently need to fix the bug where it prints multiple lines when parsing through the files
    #   I could create another function that will tell the user that the program is finished
    #could also add an option to match all of the cracked hashes to the users that they belong to
    #   look in the discord to find the example file to write the code for
    #   also need to make some new regex to parse the hashed and passwords
    #there is also an issue with the regular expression for the DCC2 hashes where it grabs everything with "$"
    #   maybe
    #   Correction, there is a problem with the file cleanser function where it isn't using the regular expression
