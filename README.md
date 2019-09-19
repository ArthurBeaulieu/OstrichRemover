# MzkOstrichRemover

![](https://badgen.net/badge/version/1.2.2/blue) ![](https://badgen.net/badge/license/GPL-3.0/green)

This script is a tool specially made to test a folder against the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention). It handles both the folder tree structure and the files themselves. It is highly recommended to read the naming convention before going any further, as explanations are raw. It was designed to work in two fields, verifying and tagging. Using arguments, you can use it the way you want.

## Get started

This script uses `Python3`, and requires `mutagen`, `Pillow` (that replaced Python Image Library) and `PyICU`. Please ensure these are installed, otherwise run in the project folder:

`# pip install -r requierements.txt`

When all requierements are installed, you can launch *MzkOstrichRemover* in three modes :

### Scan (`-s` or `--scan`)

The script will crawl the folder you gave as an argument and will report you any error it found in your file naming/tagging. If specified with a `-d` of `--dump` flag, errors can be outputed in a JSON file, to be further reviewed in the `web-reporte/index.html` file. *MzkOstrichRemover* can detect **27 errors** per file (so far). Those errors are grouped in four categories that are detailed [in the wiki](https://github.com/ManaZeak/MzkOstrichRemover/wiki/Tracked-Errors), respectively:

- *Category 1* – File system naming inconsistencies ;  
- *Category 2* – File system naming against ID3 tags ;  
- *Category 3* – ID3 tags inconsistencies ;  
- *Category 4* – Tags coherence with against album analysis ;  

During the scan, the script computes a purity grade, that takes into account the total number of possible errors per track and the actual number of errors.

At this point, you must ensure that the folder you are about to test match at least the recommended tree structure of the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention), since other folder structure may results in a biased result. Then in your cloned repository, run:

`$ ./MzkOstrichRemover.py -s ./path/to/library/folder/`

*NB*: You can also use flag such as `-v`/`--verbose` for a verbose output, `-d`/`--dump` to dump a JSON report in the `./output` folder.

### Fill (`-f` or `--fill`)

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

In any case, if the filled track name doesn't fit the convention, it will be not tested. To perform a fill scan over a given folder, run:

`$ ./MzkOstrichRemover.py -f ./path/to/library/folder/`

### Clean (`-c` or `--clean`)

The script will crawl the folder you gave as an argument, to clean all existing track metadata. It is mainly crafted to prepare tracks to be filled later on, to avoid ambiguous tags to remain (for example TOTALTRACK, TOTALTRACKS, TRACKTOTAL...). To do so, run:

`$ ./MzkOstrichRemover.py -c ./path/to/library/folder/`

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
- [ ] Specific errors (~~cover size~~, ~~album artist field~~, genre, ~~producer~~, ~~bpm~~)
- [ ] Custom scan (track, album or file errors only)
- [ ] Verbose option (with several levels)
- [ ] Qt interface

 You can still learn more about the following milestones and the current tasks on the associated [Trello board](https://trello.com/b/0nVfm0Xz/mzkostrichremover). Contributions welcome!
