# dotfiles

## Install
1. Clone this repo with `git clone https://github.com/marcelkoz/dotfiles`
2. Create a symlink to the `.sym_links.py` script with `ln -s {PATH TO SCRIPT} ~`
3. Run the symlinked script. Beforehand make sure the variables at the top of the file are configurated correctly. By default the script moves any existing files that conflict with the install into the directory `~/.sym_links_duplicates`. This is known as *safe mode* and can be toggled with the `safe_mode` variable.
