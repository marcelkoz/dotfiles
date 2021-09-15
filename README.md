# dotfiles

## Install

### Requirements
- Git
- Python 3.6+

### Instructions
Clone this git repo.
```
git clone https://github.com/marcelkoz/dotfiles
```

Create a symlink to the `.sym_links.py` python script in your home directory. 
```
ln -s {PATH TO SCRIPT} ~
```

#### Script
Before running the python script make sure it is configured correctly.

##### Safe Mode
Safe mode is turned on by default.
Symlinks cannot be created if a file already exists in the destination - the syscall fails.
To counteract this the script has two choices: delete the file or move it.
Safe mode moves the conflicting files into a predefined directory, `~/.sym_links_duplicates` by default. 
This means no data loss occurs since the files are kept. 
Turning off safe mode means the script will just delete the files.
To turn off safe mode simply set the `safe_mode` variable to `False`.
```python
safe_mode = False
```
