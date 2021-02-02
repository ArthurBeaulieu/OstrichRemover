# OstrichRemover

![](https://badgen.net/badge/version/1.5.4/blue) ![](https://badgen.net/badge/license/GPL-3.0/green)

##### Like your audio files to be correctly tagged ? *OstrichRemover* might help you !

This script is specially made to test a musical folder against the [ManaZeak naming convention](https://github.com/ManaZeak/ManaZeak/wiki/%5BPRJ%5D-Audio-Naming-convention). It is highly recommended to read the naming convention before going any further. Based on this convention, *OstrichRemover* was designed to work in four fields: verifying, pre-tagging, analyzing and generating stats on your musical library.

For any concerns, you can check the [wiki](https://github.com/ArthurBeaulieu/OstrichRemover/wiki), however, if you encounter any problem that is undocumented, please contact [support@manazeak.org](mailto:support@manazeak.org)

## Get started

This script uses `Python3`, and requires `mutagen`, `Pillow` (that replaced Python Image Library) and `PyICU`. Please ensure these are installed on your system, otherwise, with `pip` installed, run the command:

`# pip install -r requierements.txt`

When all requierements are installed, you can launch *OstrichRemover* in four main modes, and one additional command :

## Scan mode (`-s` or `--scan`)

Available options :
- `-d` or `--dump` to dump a JSON report in the `./output` folder ;
- `-v` or `--verbose` for a verbose output.

The script will crawl the folder you gave as an argument and will report you any error it found in your file naming / tagging. If specified with a `-d` of `--dump` flag, errors can be outputed in a JSON file, to be further reviewed in the `web-report/index.html` file (just drag and drop the json file in the input area).
*OstrichRemover* can detect **40 errors** per file (so far). Those errors are grouped in four categories that are detailed [in the wiki](https://github.com/ArthurBeaulieu/OstrichRemover/wiki/Tracked-Errors), respectively:

- *Category 1* – File system naming inconsistencies ;  
- *Category 2* – File system naming against ID3 tags ;  
- *Category 3* – ID3 tags inconsistencies ;  
- *Category 4* – Tags coherence with against album analysis.

Before running the script in scan mode, you must ensure that the folder you are about to test matches the [ManaZeak tree structure  and naming convention](https://github.com/ManaZeak/ManaZeak/wiki/Naming-convention), since other folder structure may results in a biased result. Then in your cloned repository, run:

`$ python ./OstrichRemover.py -s ./path/to/library/folder/`

The script computes a purity grade, that takes into account the total number of possible errors per track and the actual number of errors.

## Fill mode (`-f` or `--fill`)

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

*OstrichRemover* will may be able to fill the other following tags if a given condition is met :
- Label if the publisher tags was previously set.

In any case, if the filled track name doesn't fit the convention, it will be not tested. To perform a full scan over a given folder, run:

`$ python ./OstrichRemover.py -f ./path/to/library/folder/`

## Analyze mode (`-a` or `--analyze`)

Available options :
- `-d` or `--dump` to dump the analysis result in a json file.

The analysis mode is made to use any JSON dumps generated with the `-sd` or `--scan --dump` command. Just provide the path where all your dumps resides and let the script generates you a meta analysis of them. The main goal of this command is to prepare data to be displayed in a graph (hello d3js). To do so, run (add `-d` or `--dump` to generate the JSON report) :

`$ pyton ./OstrichRemover.py -a ./path/to/json/dumps/`

## Stat scan mode (`-t` or `--stat`)

Available options :
- `-d` or `--dump` to dump the stat scan result in a json file.

This mode will crawl the audio library, and collect stats about the number of unique artists (in all artist, performer, composer and producer fields), as well as for genres and labels. This way it offers a sorted list them so you can identify typos and such. To do so, run  (add `-d` or `--dump` to generate the JSON report) :

`$ pyton ./OstrichRemover.py -t ./path/to/library/folder/`

## Additional commands

### Clean mode (`-c` or `--clean`)

The script will crawl the folder you gave as an argument, to clean all existing track metadata. It is mainly crafted to prepare tracks to be filled later on, to avoid ambiguous tags to remain (for example TOTALTRACK, TOTALTRACKS, TRACKTOTAL...). Warning, this command will remove all tags in files with no remorses at all, use with caution and self-awarness. To do so, run:

`$ pyton ./OstrichRemover.py -c ./path/to/library/folder/`

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
- [x] Meta analyzer for scan dumps
- [x] Update web report to support meta analysis dumps
- [x] Web improvement (local storage, error handling, full responsive)
- [ ] Service usage to make ostrich call an output point when done ;
- [ ] Packaging in pip (PyPi)
- [ ] ManaZeak integration as a plugin

 You can still learn more about the following milestones and the current tasks on the associated [Trello board](https://trello.com/b/0nVfm0Xz/mzkostrichremover). Contributions and ideas welcome!
