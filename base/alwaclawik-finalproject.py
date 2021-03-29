#Alex Waclawik
#alwaclawik-finalproject.py
#December 10th, 2019

#Note for grader: PythonAnywhere console can be tempermental, so when copy pasting the long binary text you may have to copy it into another blank txt file, then copy it back one line at a time.
#This seems to be a limitation of PythonAnywhere, as I had no issues running the code in an IDE and copy pasting. 

#import libraries
import hashlib
import random
import string

#define key variables and arrays
cipherText = []
decodedText = []

#main function that takes user input and calls the corresponding function
def main():
    keepGoing = True
    while keepGoing:
        userResponse = menu()
        if userResponse == "1":
            encodeText()
            cipherText.clear()
        elif userResponse == "2":
            decodeText()
            cipherText.clear()
        elif userResponse == "0":
            print ("Shutting Down...")
            keepGoing = False
        else:
            print ("Error: Invalid Input")

#simple menu that prints out and asks the user what they would like to do
def menu():
    print ("""

    Alex's POS (Pretty OK Security) Encryption Tool // Version 1.0

    0) Shut Down
    1) Encrypt
    2) Decrypt
        """)
    userInput = input("Select Option: ")
    return (userInput)

#function that encrypts user input
def encodeText():
    plainText = input("Text to be encrypted: ")

    #puts input in proper case and checks length before moving forward
    plainText = plainText.upper()
    plainText = plainText.replace(" ", "")
    if any(char in string.punctuation for char in plainText):
        print("Error: Letters and numbers only")
        return
    elif len(plainText) > 48:
        print("Error: 48 Character Limit")
        return
    elif len(plainText) < 48:
        lessthan48 = True
    else:
        pass

    #take MD5 hash of 'plainText' and put it in proper case
    plainHash = hashlib.md5(plainText.encode()).hexdigest()
    plainHash = plainHash.upper()

    #fills in the remaining characters with '-'
    if lessthan48:
        extraValues = 48 - len(plainText)
        for x in range(extraValues):
            plainText = plainText + "-"
    else:
        pass

    #encode 'plainText' and 'plainHash' into binary
    plainText = encodeBinary(plainText)
    plainHash = encodeBinary(plainHash)

    #make 'plainText' and 'plainHash' into lists
    plainText = list(plainText)
    plainHash = list(plainHash)

    #compare 'plainText' and 'plainHash' via XOR operation
    xorHash = plainHash + plainHash
    XOR(plainText, xorHash)

    #find remaining length, and fill with random values
    length = len(cipherText) + len(plainHash)

    fillerNumber = 1024 - length
    fillerBinary = randomBinary(fillerNumber)

    #join the encryped message, hash, and filler all into one list
    cipherText1 = cipherText + fillerBinary
    cipherText2 = cipherText1 + plainHash

    #convert to string for output to user
    cipherString = ''.join([str(elem) for elem in cipherText2])
    print("Encrypted Text: ")
    print(" ")
    print(cipherString)

#function that converts values into binary
def encodeBinary(target):
    binaryEncode = {
        "A": "01000001",
        "B": "01000010",
        "C": "01000011",
        "D": "01000100",
        "E": "01000101",
        "F": "01000110",
        "G": "01000111",
        "H": "01001000",
        "I": "01001001",
        "J": "01001010",
        "K": "01001011",
        "L": "01001100",
        "M": "01001101",
        "N": "01001110",
        "O": "01001111",
        "P": "01010000",
        "Q": "01010001",
        "R": "01010010",
        "S": "01010011",
        "T": "01010100",
        "U": "01010101",
        "V": "01010110",
        "W": "01010111",
        "X": "01011000",
        "Y": "01011001",
        "Z": "01011010",
        "0": "00000000",
        "1": "00000001",
        "2": "00000010",
        "3": "00000011",
        "4": "00000100",
        "5": "00000101",
        "6": "00000110",
        "7": "00000111",
        "8": "00001000",
        "9": "00001001",
        "-": "10101010",
        }
    for x in binaryEncode:
        #translate using 'binaryEncode' dictionary and join back into target
        target = ''.join([binaryEncode.get(x, x) for x in target])
        #return value
        return (target)

#function that compares two variables via XOR operation
def XOR(plainText, plainHash):
    for x in range(len(plainText)):
        if plainHash[x] > plainText[x]:
            cipherText.append(1)
        elif plainHash[x] < plainText[x]:
            cipherText.append(1)
        else:
            cipherText.append(0)

#function that produces random filler binary values
def randomBinary(fillerNumber):
    fillerBinary = []
    for x in range(fillerNumber):
        fillerBinary.append(random.randint(0, 1))
    return (fillerBinary)

#function that decrypts user input
def decodeText():
    decryptText = input("Text to be decrypted: ")
    #verify input is correct length
    if len(decryptText) != 1024:
        print("Error: Must be 1024 characters")
    else:
        pass

    #turn 'decryptText' into a list
    decryptList = list(decryptText)

    #find the hash in 'decryptList'
    plainHash = decryptList[768:]

    #find the message in 'decryptList'
    plainText = decryptList[:384]

    #compare 'plainText' and 'plainHash' via XOR operation
    xorHash = plainHash + plainHash
    XOR2(plainText, xorHash)

    #convert 'plainHash' and 'plainText' from binary
    decodedHash = decodeBinary(plainHash)
    decodedText = decodeBinary(cipherText)

    #join 'decodedText' and 'decodedHash' into strings for output
    stringHash = ''.join([str(elem) for elem in decodedHash])
    #put 'stringHash' in proper case
    stringHash = stringHash.lower()
    stringText = ''.join([str(elem) for elem in decodedText])

    #take another hash of the decrypted text to compare to original hash
    testHash = hashlib.md5(stringText.encode()).hexdigest()

    #output results to user
    print("Decrypted Message: {}".format(stringText))
    print(" ")
    if stringHash == testHash:
        print("{} == {}".format(stringHash, testHash))
        print(" ")
        print("Message has been untampered with.")
    else:
        print("{} != {}".format(stringHash, testHash))
        print(" ")
        print("Message has been tampered with.")

#function that converts values back from binary
def decodeBinary(target):
    decodeLength = len(target) // 8
    a = 0
    b = 8
    decodeList = []
    for x in range(decodeLength):
        decodeList[a:b] = [''.join(target[a:b])]
        a = a + 8
        b = b + 8
    binaryDecode = {
        "01000001": "A",
        "01000010": "B",
        "01000011": "C",
        "01000100": "D",
        "01000101": "E",
        "01000110": "F",
        "01000111": "G",
        "01001000": "H",
        "01001001": "I",
        "01001010": "J",
        "01001011": "K",
        "01001100": "L",
        "01001101": "M",
        "01001110": "N",
        "01001111": "O",
        "01010000": "P",
        "01010001": "Q",
        "01010010": "R",
        "01010011": "S",
        "01010100": "T",
        "01010101": "U",
        "01010110": "V",
        "01010111": "W",
        "01011000": "X",
        "01011001": "Y",
        "01011010": "Z",
        "00000000": "0",
        "00000001": "1",
        "00000010": "2",
        "00000011": "3",
        "00000100": "4",
        "00000101": "5",
        "00000110": "6",
        "00000111": "7",
        "00001000": "8",
        "00001001": "9",
        "10101010": "",
        }
    for x in binaryDecode:
        #translate using 'binaryDecode' and join back into 'target'
        decodedList = []
        decodedList[:] = [binaryDecode.get(e, '') for e in decodeList]
    return (decodedList)

#additional XOR function for decoding as the cipherText cannot be appended by integers
def XOR2(plainText, plainHash):
    for x in range(len(plainText)):
        if plainHash[x] > plainText[x]:
            cipherText.append("1")
        elif plainHash[x] < plainText[x]:
            cipherText.append("1")
        else:
            cipherText.append("0")

if __name__=="__main__":
    main()