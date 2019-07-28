# MzkOstrichRemover

![](https://badgen.net/badge/version/1.1.3/blue) ![](https://badgen.net/badge/license/GPL-3.0/green)

This script is a tool specially made to test a folder against the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention). It handles both the folder tree structure and the files themselves. It is highly recommended to read the naming convention before going any further, as explanations are raw.

*MzkOstrichRemover* can detect **27 errors** per file (so far). Those errors are grouped in four categories that are detailed [in the wiki](https://github.com/ManaZeak/MzkOstrichRemover/wiki/Tracked-Errors), respectively:

- *Category 1* – File system naming inconsistencies ;  
- *Category 2* – File system naming against ID3 tags ;  
- *Category 3* – ID3 tags inconsistencies ;  
- *Category 4* – Tags coherence with against album analysis ;  

During the scan, the script computes a purity grade, that takes into account the total number of possible errors per track and the actual number of errors.

## Get started

This script uses `Python3`, and requires `mutagen`, `Pillow` (that replaced Python Image Library) and `PyICU`. Please ensure these are installed, otherwise run in the project folder:

`# pip install -r requierements.txt`

At this point, you must ensure that the folder you are about to test match at least the recommended tree structure of the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention), since other folder structure may results in the script failure. Then in your cloned repository, run:

`$ ./MzkOstrichRemover.py ./path/to/library/folder/`

*NB*: use `-h` for help, `-v` for a verbose output, `-d` to dump a JSON report in the `./output` folder.

## Features

##### v1.0
- [x] Complete scanning process and error check
- [x] Verbose output (display track errors as a tree after scan)
- [x] JSON dump (as a `-d` option)
- [x] Basic web view for JSON dumps

##### v2.0
- [ ] Specific errors (~~cover size~~, ~~album artist field~~, genre, ~~producer~~, ~~bpm~~)
- [ ] Custom scan (track, album or file errors only)
- [ ] Verbose option (with several levels)
- [ ] Qt interface

 You can still learn more about the following milestones and the current tasks on the associated [Trello board](https://trello.com/b/0nVfm0Xz/mzkostrichremover). Contributions welcome!
