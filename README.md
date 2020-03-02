# MzkOstrichRemover

![](https://badgen.net/badge/version/1.2.6/blue) ![](https://badgen.net/badge/license/GPL-3.0/green)

##### Like your audio files to be correctly tagged ? *MzkOstrichRemover* might help you !

This script is a tool specially made to test a folder against the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention). It handles both the folder tree structure and the files themselves. It is highly recommended to read the naming convention before going any further, as explanations are raw. It was designed to work in two fields, verifying and tagging. Using arguments, you can use it the way you want.

If you encounter any problem that is undocumented, please contact [support@manazeak.org](mailto:support@manazeak.org)

## Get started

This script uses `Python3`, and requires `mutagen`, `Pillow` (that replaced Python Image Library) and `PyICU`. Please ensure these are installed, otherwise run in the project folder (`pip` must be installed on the system):

`# pip install -r requierements.txt`

When all requierements are installed, you can launch *MzkOstrichRemover* in three modes :

### Scan (`-s` or `--scan`)

Available options :
- `-d` or `--dump` to dump a JSON report in the `./output` folder ;
- `-v` or `--verbose` for a verbose output.

The script will crawl the folder you gave as an argument and will report you any error it found in your file naming / tagging. If specified with a `-d` of `--dump` flag, errors can be outputed in a JSON file, to be further reviewed in the `web-report/index.html` file (just drag and drop the json file in the input area).
*MzkOstrichRemover* can detect **28 errors** per file (so far). Those errors are grouped in four categories that are detailed [in the wiki](https://github.com/ManaZeak/MzkOstrichRemover/wiki/Tracked-Errors), respectively:

- *Category 1* – File system naming inconsistencies ;  
- *Category 2* – File system naming against ID3 tags ;  
- *Category 3* – ID3 tags inconsistencies ;  
- *Category 4* – Tags coherence with against album analysis.

Before running the script in scan mode, you must ensure that the folder you are about to test matches the [ManaZeak tree structure  and naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention), since other folder structure may results in a biased result. Then in your cloned repository, run:

`$ python ./MzkOstrichRemover.py -s ./path/to/library/folder/`

The script computes a purity grade, that takes into account the total number of possible errors per track and the actual number of errors.

### Fill (`-f` or `--fill`)

Available options :
- `-v` or `--verbose` for a verbose output ;
- `-e` or `--errors` to only display errors that occured.

The script will also crawl the folder you gave as an argument, but this time it will fill the file tags, using the filename. This script usage assumes that you have already properly named the file in the tested folder. According to the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention),  it will automatically fill the following tags:

- title ;
- artist ;
- album title ;
- album artist ;
- year ;
- performer ;
- track number ;
- total track ;
- disc number ;
- total disc ;
- cover.

*MzkOstrichRemover* will may be able to fill the other following tags if a given condition is met :
- Label if the publisher tags was previously set.

In any case, if the filled track name doesn't fit the convention, it will be not tested. To perform a full scan over a given folder, run:

`$ python ./MzkOstrichRemover.py -f ./path/to/library/folder/`

### Clean (`-c` or `--clean`)

The script will crawl the folder you gave as an argument, to clean all existing track metadata. It is mainly crafted to prepare tracks to be filled later on, to avoid ambiguous tags to remain (for example TOTALTRACK, TOTALTRACKS, TRACKTOTAL...). To do so, run:

`$ pyton ./MzkOstrichRemover.py -c ./path/to/library/folder/`

---

## Features

##### v1.0
- [x] Complete scanning process and error check
- [x] Verbose output (display track errors as a tree after scan)
- [x] JSON dump (as a `-d` option)
- [x] Basic web view for JSON dumps

##### v2.0
- [x] Fill tag from filename mode
- [x] Clean tags of given folder
- [x] Specific errors (~~cover size~~, ~~album artist field~~, ~~genre~~, ~~producer~~, ~~bpm~~)
- [ ] Verbose option (with several levels)
- [ ] Qt interface

 You can still learn more about the following milestones and the current tasks on the associated [Trello board](https://trello.com/b/0nVfm0Xz/mzkostrichremover). Contributions and ideas welcome!
