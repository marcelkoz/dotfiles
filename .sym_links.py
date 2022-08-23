#!/usr/bin/env python3
#
# ~/.sym_links.py
#

from pathlib import Path
import os
import typing

class FilePair:
    def __init__(self, source, destination):
        self.source      = Path(source)
        self.destination = Path(destination)

    def verify(self):
        if not Path(source).exists():
            raise InvalidPairError('source location does not exist', self)

    def __str__(self):
        return f'FilePair {{ Source: ({self.source}) Destination: ({self.destination}) }}'

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
    FilePair(source / '.bashrc',  user_home),
    FilePair(source / '.zshrc',   user_home),
    FilePair(source / '.vimrc',   user_home),
    FilePair(source / '.inputrc', user_home),
)

# config files
# (source, destination)
config_files = (
    FilePair(config_src / 'kitty/kitty.conf', config_dest / 'kitty'),
    FilePair(source / '.sh_aliases',          user_home),
)

# bin files
# (source, destination)
bin_files = (
    FilePair(bin_src / 'trash', bin_dest),
)

class InvalidPairError(Exception):
    def __init__(self, reason, pair):
        super().__init__(reason)
        self.pair = pair

def create_destination_parent(pair: FilePair):
    print(indent, 'Ensuring ({0}) has a valid symlink destination...'.format(pair.destination))
    parent = pair.destination.parent.resolve()
    if not parent.exists():
        os.makedirs(parent, exist_ok=True)

def replace_destination_file(file_path: Path):
    print(indent, '({0}) already exists, {1}moving file...'.format(file_path, '' if safe_mode else 're'))

    if safe_mode:
        os.rename(file_path, dup_dest / file_path.name)s
    else:
        os.remove(file_path)

def create_symlinks(pairs: typing.List[FilePair]):
    for pair in pairs:
        create_destination_parent(pair)

        destination_file = pair.destination / pair.source.name
        if destination_file.exists():
            replace_destination_file(destination_file)    

        os.symlink(pair.source, destination_file)
        print(indent, 'Created symlink ({0}) -> ({1})'.format(pair.source, destination_file))

def verify_symlinks(pairs: typing.List[FilePair]):
    for pair in pairs:
        pair.verify()
        print(indent, f'Verified ({pair.source}) -> ({pair.destination})')

def link_files(file_type: str, pairs: typing.Tuple[FilePair]):
    print(f'Verifying {file_type} file symlinks...')
    verify_symlinks(pairs)
    print(f'Finished verifying {file_type} file symlinks.', end='\n\n')

    print(f'Creating {file_type} file symlinks...')
    create_symlinks(pairs)
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
