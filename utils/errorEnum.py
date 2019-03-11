# Python imports
from enum import unique, Enum


@unique
## The enumeration containing all the keys of each possible errors.
class ErrorEnum(Enum):
## ------------
## Category 1 : Filesystem naming inconsistencies
    # ErrorCode 00 : Filename release artists doesn't match the artist foldername
    FILENAME_RELEASE_ARTIST_VS_ARTIST_FOLDERNAME = 0

    # ErrorCode 01 : Filename year doesn't match the album foldername year
    FILENAME_YEAR_VS_ALBUM_FOLDERNAME_YEAR = 1

    # ErrorCode 02 : Filename album doesn't match the album foldername
    FILENAME_ALBUM_VS_ALBUM_FOLDERNAME = 2

    # ErrorCode 17 : Year is not the same on all physical files of the album
    FILES_ALBUM_YEAR_NOT_EQUAL = 17

    # ErrorCode 18 : The Filename doesn't follow the naming pattern properly
    INCONSISTENT_FILENAME = 18

## ------------
## Category 2 : Filesystem naming vs ID3 tags inconsistencies
    # ErrorCode 03 : Filename year doesn't math the track year tag
    FILENAME_YEAR_VS_YEAR_TAG = 3

    # ErrorCode 04 : Foldername year doesn't math the track year tag
    FOLDERNAME_YEAR_VS_YEAR_TAG = 4

    # ErrorCode 05 : Filename album doesn't match the track album
    FILENAME_ALBUM_VS_ALBUM_TAG = 5

    # ErrorCode 06 : Foldername album doesn't match the track album
    FOLDERNAME_ALBUM_VS_ALBUM_TAG = 6

    # ErrorCode 07 : Filename disc+track number doesn't match the track disc+track number
    FILENAME_DISC_TRACK_NO_VS_DISC_TRACK_NO_TAG = 7

    # ErrorCode 08 : Filename artists doesn't match the track artist tag
    FILENAME_ARTIST_VS_ARTIST_TAG = 8

    # ErrorCode 09 : Title remix artist doesn't match the track artist
    FILENAME_ARTIST_VS_REMIX_ARTIST = 9

    # ErrorCode 10 : Filename title doesn't match the track title tag
    FILENAME_TITLE_VS_TITLE_TAG = 10

## ------------
# Category 3 : ID3 tags inconsistencies
    # ErrorCode 11 : Some tag requested by the naming convention aren't filled in track
    MISSING_TAGS = 11

    # ErrorCode 12 : Performer does not contains both the artist and the featuring artist
    INCONSISTENT_PERFORMER = 12

    # ErrorCode 13 : Performer does not contains both the artist and the featuring artist
    MISSORDERED_TAGS = 13

    # ErrorCode 19 : Cover is invalid (not 1000x1000 jpg/png)
    INVALID_COVER = 19

    # ErrorCode 20 : Track has no cover
    MISSING_COVER = 20

## ------------
# Category 4 : Track tags coherence with album metrics
    # ErrorCode 14 : Computed album total track is not equal to the track total track tag
    ALBUM_TOTAL_TRACK_VS_TRACK_TOTAL_TRACK = 14

    # ErrorCode 15 : Computed album disc track is not equal to the track disc track tag
    ALBUM_DISC_TRACK_VS_TRACK_DISC_TRACK = 15

    # ErrorCode 16 : Computed album year is not equal to the track year tag
    ALBUM_YEAR_VS_TRACK_YEAR = 16
