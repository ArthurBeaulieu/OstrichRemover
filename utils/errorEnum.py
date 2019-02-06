from enum import unique, Enum


@unique
## The enumeration containing all the keys of each possible errors.
class ErrorEnum(Enum):
	# 0 : Track release artists and artist folder name doesn't match
    # 1 : Track year and file name year doesn't match
    # 2 : Track year and folder name year doesn't match
    # 3 : Track album and file name album doesn't match
    # 4 : Track album and folder name album doesn't match
    # 5 : Track disc+track number and file name disc+track number doesn't match
    # 6 : Track artists and file name artists doesn't match
    # 7 : Track title and file name title doesn't match*
