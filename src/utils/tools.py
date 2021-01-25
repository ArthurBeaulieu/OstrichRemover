# Python imports
import os
import sys
import datetime
# Project imports
from src.utils.errorEnum import ErrorEnum
from src.references.refForbiddenChar import RefForbiddenChar


# Creates a directory if and only if it doesn't exists yet
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Something unexpected append when creating {}'.format(directory))


# Converts a given number to a properly formatted file size
def convertBytes(num):
    for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.2f %s' % (num, i)
        num /= 1024.0


# Check if string begins with a dot
def prefixDot(charList):
    if charList[0] == '.':
        return True
    else:
        return False


# Check if string begins with three dots
def prefixThreeDots(charList):
    if charList[0] == '.' and charList[1] == '.' and charList[2] == '.':
        return True
    else:
        return False


# Check if string ends with a dot
def suffixDot(charList):
    if charList[len(charList) - 1] == '.':
        return True
    else:
        return False


# Check if string ends with three dots
def suffixThreeDots(charList):
    if charList[len(charList) - 1] == '.' and charList[len(charList) - 2] == '.' and charList[len(charList) - 3] == '.':
        return True
    else:
        return False


# Compute the purity percentage according to the error enum length and the errors counter
def computePurity(errorCounter, tracksSample):
    totalPossibleError = tracksSample * len(ErrorEnum)
    return round(100 - round((errorCounter * 100) / totalPossibleError, 2), 2)


# Sanitize a given string and replace all forbidden char with a `-`
def removeSpecialCharFromString(string):
    # Checking first that the differents char are bc of an illegal symbol
    for x in range(0, len(string)):
        if string[x] in RefForbiddenChar.forbiddenChars:
            string[x] = '-'
    return string


# Sanitize items in a given array and replace all forbidden char with a `-`
def removeSpecialCharFromArray(array):
    output = []
    for item in array:
        string = ''
        for x in range(0, len(item)):
            if item[x] in RefForbiddenChar.forbiddenChars:
                string += '-'
            else:
                string += item[x]
        output.append(string)
    return output


# Prompt user to yes an action
def queryYesNo(question, default='yes'):
    valid = { 'yes': True, 'y': True, 'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == "yes":
        prompt = ' [Y/n] '
    elif default == "no":
        prompt = ' [y/N] '
    else:
        raise ValueError("> Invalid default answer in source code: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


# Validate date formatting
def validateDateFormat(string):
    try:
        datetime.datetime.strptime(string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def insertInListIfNotExisting(inputList, insertionList):
    for item in insertionList:
        if item not in inputList:
            inputList.append(item)
    return inputList
