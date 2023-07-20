import os
import re
import argparse

def list_to_file(list, name):
#Function to take a list and puth the list in a file line-by-line
    file = open( name+'.cleaned', 'w')
    for items in list:
        file.write(items+"\n")
    file.close()
    print('Cleaning finished output will be in the file named', name+'.cleaned')

def Rem_Duplicates(hashes):
# Function ot remove the duplicates from a list
    hashes = list(dict.fromkeys(hashes))
    return (hashes)

def File_Clenser(input):
#Function to go through a file of DCC2 hashes and clean them up
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
        print('Starting parse...')
        with open(input) as file:
            content = file.readlines()
        # Pull the hashes
        for x in range (len(content)):
            hash = re.finditer(pattern, content[x])
            for match in hash:
                hashes.append(match.group())
    return hashes

def List_Cleanser (hash_list, input):
# Function to clean a list of dcc2 hashes
    tmp_hashes = []         # temporary placeholder

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
    cleaned_hashes = Rem_Duplicates(cleaned_hashes)
    # send the list to the 'list_to_file' function
    list_to_file(cleaned_hashes, input)

def Directory_Parser(pattern, directory, mode):
    hashes2 = []
    fileslist =  os.listdir(directory)
    for file in fileslist:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            #print (file_path)
            hashes = Secrets_Parser(file_path, pattern)
            hashes2 = hashes + hashes2
            print(hashes2)
        if (mode == 'DCC2'):
            List_Cleanser(hashes2, 'secretdumps.DCC2')
        else:
            hashes2 = Rem_Duplicates(hashes2)
            list_to_file(hashes, 'sectretsdump.NTLM')

    
if __name__ == "__main__":
    # Argument parcer stuff
    parser = argparse.ArgumentParser(description='Hash cleaner for the Domain Caches Credentials 2 hash type')
    parser.parse_args
    parser.add_argument('-f', '--FILE', type=str, help='File path of the file with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-d', '--DIRECTORY', type=str, help='Directory path of the files with the uncleaned DCC2 hashes', default=None)
    parser.add_argument('-s', '--SECRETS', type=str, help='Path of the file with the secret dump hashes', default=None)
    parser.add_argument('-m', '--MODE', type=str, help='Type of hash to be found from secretsdump files DCC2 or NTLM', default=None)
    args = parser.parse_args()

    # Regex patterns
    pattern_DCC2 = r"(\$DCC2\$)(.*)"
    pattern_NTLM = r"(.*?):(.*?):(.*?):(.*?):::"

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
    else:
        File_Clenser(args.FILE)
