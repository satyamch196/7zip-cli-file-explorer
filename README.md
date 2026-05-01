# 7zip CLI File Explorer
### A file explorer to explore files and folders of any archive supported by the 7z command with a shell-like interface.
## How to use ?
### You need to firstly create a txt file from the output of the 7z command using:
```
7z l ARCHIVE.7z | tee test-7z-file-index.txt
```
### Or if you are sure 7z will be able to read and list the archive and its contents,
### Or you simply don't want to fill your terminal screen then use:
```
7z l ARCHIVE.7Z > test-7z-file-index.txt
```
### Then change filename variable value to the filename of the file you just generated in the 7zip-python-dict-creator.py
### The generated dictionary should then be "passed" to the 7zip-cli-file-explorer.py file to get to the cli.
## Note on the folders in this repository:

| Folder Name | Description |
| ----------- | ----------- |
| `help-files` | Python scripts helpful for further development of this software |
| `misc-files` | Off-topic but potentially useful python scripts |
| `temp-files` | Helpful python scripts but should be removed in long run |
| `test-files` | Some 7zip archive lists that can be used to test the file explorer |
> [!NOTE]
> The file explorer and this README file are not complete yet, so it is a bit harder to understand/use for beginners.
