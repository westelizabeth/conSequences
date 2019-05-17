#!/usr/bin/python3

import sys
import collections

aminoaciddictionary = {
    "Alanine": "A",
    "Glycine": "G",
    "Isoleucine": "I",
    "Leucine": "L",
    "Proline": "P",
    "Valine": "V",
    "Phenylalanine": "F",
    "Tryptophan": "W",
    "Tyrosine": "Y",
    "Aspartic Acid": "D",
    "Glutamic Acid": "E",
    "Arginine": "R",
    "Histidine": "H",
    "Lysine": "K",
    "Serine": "S",
    "Threonine": "T",
    "Cystenine": "C",
    "Methonine": "M",
    "Asparagine": "N",
    "Glutamine": "Q"
}


# def exhaustively_reaplce_one_aa(subseq):
#         for k in aminoaciddictionary:
#             amnacd = aminoaciddictionary.get(k)


def print_sites(list):
    x = 1
    for a, b in list:
        print("[" + str(x) + "]   (" + str(a) + " " + str(b) + ")")
        x += 1


def print_pairs(list):
    for a, b in list:
        print(a, b)


def make_pairs(list):
    a = 0
    pairlist = []
    while (a < len(list)):
        pair = (int(list[a]), int(list[a + 1]))
        pairlist.append(pair)
        a += 2
    return pairlist


def delete_specific_pattern(str1, pat):
    if pat in str1:
        newstr = str1.replace(pat, "")
        print(str1)
        print(newstr)
        print("Deleted " + str(str1.count(pat)) + " occurrences from sequence")


def replace_pat1_with_pat2(str1, pat1, pat2):
    print(str1)
    if pat1 in str1:
        newstr = str1.replace(pat1, pat2)
        print(newstr)
    else:
        print("Pattern attempting to be replaced does not exist in sequence")


def unique_list_letters_in_string(str1):
    alist = list(set(str1))
    print(alist)
    blist = collections.Counter(str1)
    print(blist)


def delete_all_occurrences_of_x(str1, x):
    newstr = str1.replace(x, "")
    print(str1)
    print(newstr)


def replace_every_instance_of_x_with_y(str1, x, y):
    y1 = aminoaciddictionary.get(y)
    print(y1)
    newstr = str1.replace(x, y1)
    print(newstr)


def replace_every_instance_of_x_with_y_return(str1, x, y):
    y1 = aminoaciddictionary.get(y)
    newstr = str1.replace(x, y1)
    return(newstr)


def get_key(v):
    for key, value in aminoaciddictionary.items():
        if value == v:
            return key


def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    while True:
        action = input("[A] View Amino Acid Dictionary \n"
                       "[B] View AA Single Code Letters in AAD \n"
                       "[C] Manipulate sequence \n"
                       "[D] Generate new with given * sites \n"
                       "[Q] quit \n").upper()
        if action not in "ABCDQ" or len(action) != 1:
            print("I don't know how to do that")
            continue
        elif action == 'A':
            for aminoacid in aminoaciddictionary:
                print(aminoacid)
        elif action == 'B':
            for aa in aminoaciddictionary.values():
                print(aa)
        elif action == 'C':
            seq = input("Sequence to edit? ").upper()
            print(seq)
            a = True
            while a:
                action = input("[X] Replace options\n"
                               "[Y] Delete options\n"
                               "[Z] Insert options\n"
                               "[R] Change sequence\n"
                               "[T] Unique list of letters in sequence & count\n"
                               "[Q] Back \n").upper()

                if action not in "XYZRTQ" or len(action) != 1:
                    print("I don't know how to do that")
                    continue
                ###########################################################################################
                elif action == 'X':  # 2
                    print("Replace")
                    x = True
                    while x:
                        action = input("[a] Replace all of one letter\n"
                                       "[b] Replace pattern\n"
                                       "[q] Back\n").lower()
                        if action not in "abq" or len(action) != 1:
                            print("I don't know how to do that")
                            continue
                        # replace one at a time
                        # replace all of one letter
                        elif action == 'a':
                            print("hello")
                            temp1 = 'A'
                            temp2 = "Arginine"
                            replace_every_instance_of_x_with_y(seq, temp1, temp2)
                        # replace patterns with new one
                        elif action == 'b':
                            temppat1 = "ABC"
                            temppat2 = "XY"
                            replace_pat1_with_pat2(seq, temppat1, temppat2)
                        elif action == 'q':
                            x = False
                ###########################################################################################
                elif action == 'Y':  # 1
                    print("Delete")
                    y = True
                    while y:
                        action = input("[a] Delete all of one letter \n"
                                       "[b] Delete all occurrences of specific pattern \n"
                                       "[q] Back \n").lower()
                        if action not in "abq" or len(action) != 1:
                            print("I don't know how to do that")
                            continue
                        # delete all of one letter
                        elif action == 'a':
                            letter_to_delete = input("Letter code to delete: ").upper()
                            delete_all_occurrences_of_x(seq, letter_to_delete)
                        # delete specific patterns
                        elif action == 'b':
                            temppat = seq[1:3]
                            print("TEMPPAT: seq[1:3] " + temppat)
                            delete_specific_pattern(seq, temppat)
                        # delete chunks up to (12?)
                        # delete one (or x) at a time
                        elif action == 'q':
                            y = False
                ###########################################################################################
                elif action == 'Z':  # 3
                    print("Insert")
                    # insert single character
                    # insert specific chunk/after specific occurrence
                    print(seq)
                elif action == 'R':
                    seq = input("Enter new sequence: ").upper()
                    print(seq)
                elif action == 'T':
                    unique_list_letters_in_string(seq)
                elif action == 'Q':
                    a = False
        ###########################################################################################
        elif action == 'D':
            print(
                "This function expects a single sequence containing only letters and then followed with integer pairs.\n"
                "No Error handling so it is up to you, the user to not mess up!\nEXAMPLE  ABCDEABCDEABCDE 2 4 7 12  \n")
            userinput = input("Please enter a sequence to edit & site index pairs. (Zero indexed) ")
            input_list = userinput.split(" ")
            seq = input_list[0].upper()
            print(seq)
            if isEven(len(input_list)):
                print("User Error: Even number of arguments")
            else:
                # hkstchkstchkstc 2 4 10 13
                del input_list[0]
                pairlist = make_pairs(input_list)
                print_pairs(pairlist)
            a = True
            while a:
                action = input("[a] Exhaustively replace single amino acid throughout a site \n"
                               "[b] Exhaustively delete one amino acid at a time throughout a site \n"
                               "[c] Replace all occurrences of an amino acid in a site\n"
                               # "[d] The Most Exhaustive it can be for a single site\n"
                               "[q] Back \n").lower()
                if action not in "abcdq" or len(action) != 1:
                    print("I don't know how to do that")
                    continue
                ###########################################################################################
                elif action == 'a':
                    print("Specified sites are :")
                    print_sites(pairlist)
                    site = int(input("select a site: "))
                    print("site ", pairlist[site - 1])
                    siteSubStr = seq[pairlist[site - 1][0]:pairlist[site - 1][1] + 1]
                    print("Here are the " + str(len(
                        siteSubStr) * 20) + " variations of the sequence when exhaustively replacing single amino acids in site " + str(
                        pairlist[site - 1]) + ":")

                    for x in siteSubStr:
                        for k in aminoaciddictionary:
                            amnacd = aminoaciddictionary.get(k)
                            variation = siteSubStr.replace(x, amnacd)
                            # variation = exhaustively_reaplce_one_aa(siteSubStr)
                            print(seq[:pairlist[site - 1][0]] + variation + seq[pairlist[site - 1][1] + 1:])
                ###########################################################################################
                elif action == 'b':
                    print("Specified sites are :")
                    print_sites(pairlist)
                    site = int(input("select a site: "))
                    print("site ", pairlist[site - 1])
                    siteSubStr = seq[pairlist[site - 1][0]:pairlist[site - 1][1] + 1]
                    print("Here are the " + str(len(
                        siteSubStr) ) + " variations of the sequence when exhaustively deleting single amino acids at a time in site " + str(
                        pairlist[site - 1]) + ":")

                    for x in siteSubStr:
                        variation = siteSubStr.replace(x, "")
                        print(seq[:pairlist[site - 1][0]] + variation + seq[pairlist[site - 1][1] + 1:])
                ###########################################################################################

                #this is bad if there is any repetition in the substring BTW
                elif action == 'c':
                    print("Specified sites are :")
                    print_sites(pairlist)
                    site = int(input("select a site: "))
                    print("site ", pairlist[site - 1])
                    siteSubStr = seq[pairlist[site - 1][0]:pairlist[site - 1][1] + 1]
                    print("Here are the " + str(len(
                        siteSubStr)) + " variations of the sequence when replacing all occurrences of a single amino acids in site " + str(
                        pairlist[site - 1]) + ":")
                    for x in siteSubStr:
                        for k in aminoaciddictionary:
                            amnacd = aminoaciddictionary.get(k)
                            variation = replace_every_instance_of_x_with_y_return(siteSubStr, x, amnacd)
                            print(seq[:pairlist[site - 1][0]] + variation + seq[pairlist[site - 1][1] + 1:])


                elif action == 'd':
                    print("Specified sites are :")
                    print_sites(pairlist)
                    site = int(input("select a site: "))
                    print("site ", pairlist[site - 1])
                    siteSubStr = seq[pairlist[site - 1][0]:pairlist[site - 1][1] + 1]
                    print("Here are the " + str(len(
                        siteSubStr) * 20) + " variations of the sequence when exhaustively replacing single amino acids in site " + str(
                        pairlist[site - 1]) + ":")

                    for x in siteSubStr:
                        for k in aminoaciddictionary:
                            amnacd = aminoaciddictionary.get(k)
                            variation = siteSubStr.replace(x, amnacd)
                            # variation = exhaustively_reaplce_one_aa(siteSubStr)
                ###########################################################################################
                elif action == 'q':
                    a = False
        elif action == 'Q':
            sys.exit()

# "[V] print key for value A (Alanine) \n" ... key = get_key("A")... print(key)
# "[K] print value for key Alanine (A) \n" .... print(aminoaciddictionary.get("Alanine"))
