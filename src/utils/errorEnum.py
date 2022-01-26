# Python imports
from enum import unique, Enum


@unique
## The enumeration containing all the keys of each possible errors.
class ErrorEnum(Enum):
    ## ------------
    ## Category 1 : Filesystem naming inconsistencies
    # ErrorCode 00 : Filename release artists doesn't match the artist folder name
    FILENAME_RELEASE_ARTIST_VS_ARTIST_FOLDER_NAME = {
        'errorCode': 0,
        'errorValue': "Filename release artists doesn't match the artist folder name"
    }
    # ErrorCode 01 : Filename year doesn't match the album folder name year
    FILENAME_YEAR_VS_ALBUM_FOLDER_NAME_YEAR = {
        'errorCode': 1,
        'errorValue': "Filename year doesn't match the album folder name year"
    }
    # ErrorCode 02 : Filename album doesn't match the album folder name
    FILENAME_ALBUM_VS_ALBUM_FOLDER_NAME = {
        'errorCode': 2,
        'errorValue': "Filename album doesn't match the album folder name"
    }
    # ErrorCode 17 : Year is not the same on all physical files of the album
    FILES_ALBUM_YEAR_NOT_EQUAL = {
        'errorCode': 17,
        'errorValue': "Year is not the same on all physical files of the album"
    }
    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    INCONSISTENT_FILENAME = {
        'errorCode': 18,
        'errorValue': "The Filename doesn't follow the naming pattern properly"
    }
    ## ------------
    ## Category 2 : Filesystem naming vs ID3 tags inconsistencies
    # ErrorCode 03 : Filename year doesn't math the track year tag
    FILENAME_YEAR_VS_YEAR_TAG = {
        'errorCode': 3,
        'errorValue': "Filename year doesn't math the track year tag"
    }
    # ErrorCode 04 : Folder name year doesn't math the track year tag
    FOLDER_NAME_YEAR_VS_YEAR_TAG = {
        'errorCode': 4,
        'errorValue': "Folder name year doesn't math the track year tag"
    }
    # ErrorCode 05 : Filename album doesn't match the track album
    FILENAME_ALBUM_VS_ALBUM_TAG = {
        'errorCode': 5,
        'errorValue': "Filename album doesn't match the track album"
    }
    # ErrorCode 06 : Folder name album doesn't match the track album
    FOLDER_NAME_ALBUM_VS_ALBUM_TAG = {
        'errorCode': 6,
        'errorValue': "Folder name album doesn't match the track album"
    }
    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    FILENAME_DISC_TRACK_NO_VS_DISC_TRACK_NO_TAG = {
        'errorCode': 7,
        'errorValue': "Filename disc+track number doesn't match the track disc+track number"
    }
    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    FILENAME_ARTIST_VS_ARTIST_TAG = {
        'errorCode': 8,
        'errorValue': "Filename artists doesn't match the track artist tag"
    }
    # ErrorCode 09 : Title remix artist doesn't match the track artist
    FILENAME_ARTIST_VS_REMIX_ARTIST = {
        'errorCode': 9,
        'errorValue': "Title remix artist doesn't match the filename artist"
    }
    # ErrorCode 10 : Filename title doesn't match the track title tag
    FILENAME_TITLE_VS_TITLE_TAG = {
        'errorCode': 10,
        'errorValue': "Filename title doesn't match the track title tag"
    }
    # ErrorCode 21 : Release artist folder name doesn't match the track album artist tag
    FOLDER_NAME_RELEASE_ARTISTS_VS_ALBUM_ARTIST_TAG = {
        'errorCode': 21,
        'errorValue': "Folder name release artist is not equal to the track album artist tag"
    }
    # ErrorCode 39 : Folder name release date doesn't match the track release date tag
    FOLDER_NAME_DATE_VS_RELEASE_DATE_TAG = {
        'errorCode': 39,
        'errorValue': "Folder name release date doesn't match the track release date tag"
    }
    ## ------------
    # Category 3 : ID3 tags inconsistencies
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    MISSING_TAGS = {
        'errorCode': 11,
        'errorValue': "Some tag requested by the naming convention aren't filled in track"
    }
    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    INCONSISTENT_PERFORMER = {
        'errorCode': 12,
        'errorValue': "Performer does not contains both the artist and the featuring artist"
    }
    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    MISS_ORDERED_TAGS = {
        'errorCode': 13,
        'errorValue': "Tags are in bad order"
    }
    # ErrorCode 19 : Cover is not a 1000x1000 jpg image
    INVALID_COVER = {
        'errorCode': 19,
        'errorValue': "The cover dimensions are incorrect and should be 1000x1000"
    }
    # ErrorCode 20 : Track has no cover
    MISSING_COVER = {
        'errorCode': 20,
        'errorValue': "The cover is missing from the file"
    }
    # ErrorCode 22 : Cover format is not optimized (not jpg)
    NOT_OPTIMAL_COVER = {
        'errorCode': 22,
        'errorValue': "The cover should be a jpg file for file size matters"
    }
    # ErrorCode 23 : BPM is not an integer
    FLOATING_BPM = {
        'errorCode': 23,
        'errorValue': "The BPM value is not an integer"
    }
    # ErrorCode 24 : Release year is not realistic (< 1900 or > today)
    UNLOGIC_YEAR = {
        'errorCode': 24,
        'errorValue': "Year tag can't precede 1900 or succeed today's year"
    }
    # ErrorCode 25 : Invalid country value. Use NATO country notation with 3 capital letters
    INVALID_LANG = {
        'errorCode': 25,
        'errorValue': "Invalid country trigram. Use NATO country notation with 3 capital letters"
    }
    # ErrorCode 26 : Unexisting country trigram. Check existing NATO values
    NONEXISTENT_LANG = {
        'errorCode': 26,
        'errorValue': "The lang tag value doesn't exists in the list given by NATO"
    }
    # ErrorCode 27 : Inconsistent genre tag
    INCONSISTENT_GENRE = {
        'errorCode': 27,
        'errorValue': "The genre tag value is not correctly formed"
    }
    # ErrorCode 28 : Unexisting genre tag
    UNEXISTING_GENRE = {
        'errorCode': 28,
        'errorValue': "The genre tag value doesn't match any of supported genres and styles"
    }
    # ErrorCode 29 : Invalid compilation tag
    INVALID_COMPILATION = {
        'errorCode': 29,
        'errorValue': "The compilation tag must be 0, 1, 2 or 3. Check naming convention for details"
    }
    # ErrorCode 32 : A tag in file doesn't have a unique field
    TAG_NOT_UNIQUE = {
        'errorCode': 32,
        'errorValue': "There is a tag that has several fields, which is unauthorized"
    }
    # ErrorCode 33 : The year tag doesn't match the year in released date tag
    YEAR_VS_RELEASE_YEAR = {
        'errorCode': 33,
        'errorValue': "The year tag doesn't match the year in released date tag"
    }
    # ErrorCode 35 : Cover has no description in tag
    NO_COVER_DESCRIPTION = {
        'errorCode': 35,
        'errorValue': "Cover has no description"
    }
    # ErrorCode 36 : Cover description doesn't match the fileName
    COVER_DESCRIPTION_NOT_MATCHING = {
        'errorCode': 36,
        'errorValue': "Cover description doesn't match cover filename"
    }
    # ErrorCode 37 : Release date tag is not using YYYY-MM-DD format
    WRONG_DATE_FORMAT = {
        'errorCode': 37,
        'errorValue': "Release date is not a valid date"
    }
    ## ------------
    # Category 4 : Track tags coherence with album metrics
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    ALBUM_TOTAL_TRACK_VS_TRACK_TOTAL_TRACK = {
        'errorCode': 14,
        'errorValue': "Computed album total track is not equal to the track total track tag"
    }
    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    ALBUM_DISC_TRACK_VS_TRACK_DISC_TRACK = {
        'errorCode': 15,
        'errorValue': "Computed album total disc track is not equal to the track total track tag"
    }
    # ErrorCode 16 : Computed album year is not equal to the track year tag
    ALBUM_YEAR_VS_TRACK_YEAR = {
        'errorCode': 16,
        'errorValue': "Computed album year is not equal to the track year tag"
    }
    # ErrorCode 30 : Label tag is not consistent over album tracks
    INCONSISTENT_LABELS = {
        'errorCode': 30,
        'errorValue': "Label tag is not consistent over album tracks"
    }
    # ErrorCode 31 : Lang tag is not consistent over album tracks
    INCONSISTENT_LANGUAGES = {
        'errorCode': 31,
        'errorValue': "Language tag is not consistent over album tracks"
    }
    # ErrorCode 34 : There is no cover, or there are more than one cover
    COVER_NOT_UNIQUE = {
        'errorCode': 34,
        'errorValue': "There is no cover, or there are more than one cover"
    }
    # ErrorCode 38 : Release date tag is not consistent over album tracks
    INCONSISTENT_RELEASE_DATE = {
        'errorCode': 38,
        'errorValue': "Release date tag is not consistent over album tracks"
    }
    ## ------------
    # Category 5 : Miscelaneous errors
    # ErrorCode 40 : The album folder doesn't contain any files
    EMPTY_ALBUM_FOLDER = {
        'errorCode': 40,
        'errorValue': "The album folder doesn't contain any files"
    }
    # ErrorCode 41 : The album folder only contain an image
    ALBUM_ONLY_HAS_COVER = {
        'errorCode': 41,
        'errorValue': "The album folder only contains a cover"
    }
