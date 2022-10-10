#!/usr/bin/env python3
#
# ~/.sym_links.py
#

from pathlib import Path
import logging as logger
import typing
import sys
import os

class FilePair:
    def __init__(self, source, destination):
        self.source      = Path(source)
        self.destination = Path(destination)

    def verify(self):
        pass

    def __str__(self):
        return f'FilePair {{ Source: ({self.source}) Destination: ({self.destination}) }}'

class InvalidPairError(Exception):
    def __init__(self, reason, pair):
        super().__init__(reason)
        self.pair = pair

#
# Script Adjustments
#

# logging configuration
debug_flag = sys.argv[1]
if debug_flag.lower() == 'debug':
    logger.basicConfig(level=logger.DEBUG, format='[%(levelname)s] %(message)s')
else:
    logger.basicConfig(level=logger.INFO, format='%(message)s')

# safe mode
safe_mode = True

# indentation level
indent = '  '

# path variables
user_home  = Path.home()
duplicates = user_home / '.sym_links_duplicates'
repository = user_home / 'Repos/dotfiles'

config = FilePair(repository / '.config', user_home / '.config') 
bin    = FilePair(repository / '.bin',    user_home / '.bin')

rc_files = (
    FilePair(repository / '.bashrc',  user_home),
    FilePair(repository / '.zshrc',   user_home),
    FilePair(repository / '.vimrc',   user_home),
    FilePair(repository / '.inputrc', user_home),
)

config_files = (
    FilePair(config.source / 'kitty/kitty.conf', config.destination / 'kitty'),
    FilePair(repository / '.sh_aliases',         user_home),
)

bin_files = (
    FilePair(bin.source / 'trash', bin.destination),
)

#
#
#

def create_destination_parent(pair: FilePair):
    logger.debug(f'{indent}Ensuring ({pair.destination}) has a valid symlink destination...')
    destination = pair.destination.resolve()
    if not destination.exists():
        os.makedirs(destination, exist_ok=True)

def replace_destination_file(file_path: Path):
    logger.debug('{2}({0}) already exists, {1}moving file...'.format(file_path, '' if safe_mode else 're', indent))

    if safe_mode:
        os.rename(file_path, duplicates / file_path.name)
    else:
        os.remove(file_path)

def create_symlinks(pairs: typing.List[FilePair]):
    for pair in pairs:
        create_destination_parent(pair)

        destination_file = pair.destination / pair.source.name
        if destination_file.exists():
            replace_destination_file(destination_file)    

        os.symlink(pair.source, destination_file)
        logger.info(f'{indent}Created symlink ({pair.source}) -> ({destination_file})')

def verify_symlinks(pairs: typing.List[FilePair]):
    for pair in pairs:
        pair.verify()
        logger.info(f'{indent}Verified ({pair.source}) -> ({pair.destination})')

def link_files(file_type: str, pairs: typing.Tuple[FilePair]):
    logger.info(f'\nVerifying {file_type} file symlinks...')
    verify_symlinks(pairs)

    logger.info(f'\nCreating {file_type} file symlinks...')
    create_symlinks(pairs)

def verify_repository():
    if not repository.exists():
        logger.error(f'Repository ({repository}) does not exist')
        exit(1)

def main():
    if safe_mode:
        os.makedirs(duplicates, exist_ok=True)

    try:
        verify_repository()
        link_files('rc',     rc_files)
        link_files('config', config_files)
        link_files('bin',    bin_files)
        logger.info('\nSymlink creation complete.')
    except InvalidPairError as err:
        logger.error(f'{indent}Failed to verify pair, {err}: {err.pair}')
        exit(1)

if __name__ == '__main__':
    main()
