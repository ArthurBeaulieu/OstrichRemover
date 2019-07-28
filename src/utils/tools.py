# Python imports
import os

# Project imports
from src.utils.errorEnum import ErrorEnum


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
    forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|', '\'']
    for x in range(0, len(string)):
        if string[x] in forbiddenChars:
            string[x] = '-'
    return string


# Sanitize items in a given array and replace all forbidden char with a `-`
def removeSpecialCharFromArray(array):
    forbiddenChars = ['*', '/', '\\', ':', ';', '?', '<', '>', '\"', '|', '\'']
    output = []
    for item in array:
        string = ''
        for x in range(0, len(item)):
            if item[x] in forbiddenChars:
                string += '-'
            else:
                string += item[x]
        output.append(string)
    return output
