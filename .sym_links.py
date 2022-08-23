#!/usr/bin/env python3
#
# ~/.sym_links.py
#

from pathlib import Path
import os

# safe mode
safe_mode = True

# indentation level
indent = '  '

# path variables
user_home   = Path.home()
dup_dest    = user_home / '.sym_links_duplicates'
source      = user_home / 'Repos/dotfiles'
config_dest = user_home / '.config'
config_src  = source    / '.config'
bin_dest    = user_home / '.bin'
bin_src     = source    / '.bin'

# rc files
# (source, destination)
rc_files = (
    (source / '.bashrc',  user_home),
    (source / '.zshrc',   user_home),
    (source / '.vimrc',   user_home),
    (source / '.inputrc', user_home),
)

# config files
# (source, destination)
config_files = (
    (config_src / 'kitty/kitty.conf', config_dest / 'kitty'),
    (source / '.sh_aliases',          user_home),
)

# bin files
# (source, destination)
bin_files = (
    (f'{bin_src}/trash', bin_dest),
)

class InvalidPairError(Exception):
    def __init__(self, reason, pair):
        super().__init__(reason)
        self.pair = pair

class FilePair:
    def __init__(self, source, destination):
        self.source      = Path(source)
        self.destination = Path(destination)

def create_destination_parent(pair: FilePair):
    print(indent, 'Ensuring ({0}) has a valid symlink destination...'.format(pair.destination))
    parent = pair.destination.parent.resolve()
    if not parent.exists():
        os.makedirs(parent, exist_ok=True)

def replace_destination_file(file_path: Path):
    if safe_mode:
        print(indent, '({0}) already exists, moving file...'.format(file_path))
        os.rename(file_path, dup_dest / file_path.name)
    else:
        print(indent, '({0}) already exists, removing file...'.format(file_path))
        os.remove(file_path)

def create_symlinks(files):
    for pair in files:
        pair = FilePair(*pair)

        create_destination_parent(pair)

        destination_file = pair.destination / pair.source.name
        if destination_file.exists():
            replace_destination_file(destination_file)    

        os.symlink(pair.source, destination_file)
        print(indent, 'Created symlink ({0}) -> ({1})'.format(pair.source, destination_file))

def verify_symlinks(files):
    for pair in files:
        if len(pair) != 2:
            raise InvalidPairError('not enough or too many items', pair)
        elif not Path(pair[0]).exists():
            raise InvalidPairError('source location does not exist', pair)

        print(indent, f'Verified ({pair[0]}) -> ({pair[1]})')

def link_files(file_type, files):
    print(f'Verifying {file_type} file symlinks...')
    verify_symlinks(files)
    print(f'Finished verifying {file_type} file symlinks.', end='\n\n')

    print(f'Creating {file_type} file symlinks...')
    create_symlinks(files)
    print(f'Finished creating {file_type} file symlinks.', end='\n\n')

def main():
    if safe_mode:
        os.makedirs(dup_dest, exist_ok=True)

    try:
        link_files('rc',     rc_files)
        link_files('config', config_files)
        link_files('bin',    bin_files)
    except InvalidPairError as err:
        print(indent, f'Failed to verify pair, {err}: {err.pair}') 

if __name__ == '__main__':
    main()
