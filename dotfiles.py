#!/usr/bin/env python3
#
# ~/.sym_links.py
#

from pathlib import Path
import argparse
import typing
import sys
import os

class Config:
    def __init__(self, arguments: argparse.Namespace):
        self.generate_man_pages: bool = arguments.generate_man_pages
        self.create_symlinks: bool    = arguments.create_symlinks
        self.safe_mode: bool          = not arguments.disable_safe_mode
        self.colour: bool             = not arguments.plain
        self.debug: bool              = arguments.debug

        self.indent          = '    '
        self.repository_path = Path(arguments.repository_path)

        home_path   = Path.home()
        config_path = FilePair(self.repository_path / '.config',    home_path / '.config')
        bin_path    = FilePair(self.repository_path / '.local/bin', home_path / '.local/bin')

        self.rc_files = (
            FilePair(self.repository_path / '.bashrc',   home_path / '.bashrc'),
            FilePair(self.repository_path / '.zshrc',    home_path / '.zshrc'),
            FilePair(self.repository_path / '.vimrc',    home_path / '.vimrc'),
            FilePair(self.repository_path / '.inputrc',  home_path / '.inputrc'),
            FilePair(self.repository_path / '.screenrc', home_path / '.screenrc'),
        )

        self.config_files = (
            FilePair(config_path.source / 'kitty/kitty.conf', config_path.destination / 'kitty/kitty.conf'),
            FilePair(self.repository_path / '.sh_aliases',    home_path / '.sh_aliases'),
            FilePair(self.repository_path / '.sh_env',        home_path / '.bashenv'),
            FilePair(self.repository_path / '.sh_env',        home_path / '.zshenv'),
        )

        self.bin_files = (
            FilePair(bin_path.source / 'screen-kill.sh', bin_path.destination / 'screen-kill.sh'),
        )
        self.safe_mode_path = home_path / '.found_dotfiles'

class Colour:
    Red     = '\u001b[31m'
    Green   = '\u001b[32m'
    Blue    = '\u001b[34m'
    Yellow  = '\u001b[33m'
    Magenta = '\u001b[35m'
    Cyan    = '\u001b[36m'
    White   = '\u001b[37m'
    Reset   = '\u001b[0m'

class Logger:
    def __init__(self, config: Config):
        self.__debug  = config.debug
        self.__indent = config.indent
        self.__colour = config.colour

    def colour(self, colour: Colour, text: str):
        if self.__colour:
            return f'{colour}{text}{Colour.Reset}'
        else:
            return text

    def debug(self, message: str, indent=False):
        if self.__debug:
            space = self.__indent if indent else ''
            tag = self.colour(Colour.Cyan, '(debug)')
            print(f'{space}{tag} {message}')

    def info(self, message: str, indent=False):
        space = self.__indent if indent else ''
        print(f'{space}{message}')

    def error(self, message: str, indent=False):
        space = self.__indent if indent else ''
        tag = self.colour(Colour.Red, '(error)')
        print(f'{space}{tag} {message}')
        exit(1)

class FilePair:
    def __init__(self, source: str | Path, destination: str | Path):
        self.destination = Path(destination)
        self.source = Path(source)

    def __str__(self) -> str:
        return f'"{self.source}" -> "{self.destination}"'
    
    def __repr__(self) -> str:
        return f'FilePair {{ Source: {self.source} Destination: {self.destination} }}'

def generate_man_pages(config: Config, logger: Logger):
    pass

def create_symlinks(name: str, file_pairs: tuple[FilePair], config: Config, logger: Logger):
    def exists(path):
        return path.exists() or path.is_symlink()
    
    logger.info(f'\nCreating symlinks for {name} files')

    for pair in file_pairs:
        try:
            logger.info(f'Linking {pair}', indent=True)
            if not exists(pair.source):
                raise FileNotFoundError()
            
            # broken symlinks show up as non-existant
            if exists(pair.destination):
                if config.safe_mode:
                    safe_space = config.safe_mode_path / pair.destination.name
                    tag = logger.colour(Colour.Yellow, '(Safe Mode)')
                    logger.info(f'{tag} Moving "{pair.destination}" -> "{safe_space}"', indent=True)
                    os.rename(pair.destination, safe_space)
                else:
                    os.remove(pair.destination)

            os.symlink(pair.source.absolute(), pair.destination)
        except FileNotFoundError:
            tag = logger.colour(Colour.Red, '(Fail)')
            logger.info(f'{tag} Cannot link file "{pair.source}" does it exist?', indent=True)

def create_dotfile_symlinks(config: Config, logger: Logger):
    if config.safe_mode:
        os.makedirs(config.safe_mode_path, exist_ok=True)

    args = {'config': config, 'logger': logger}
    create_symlinks('rc', config.rc_files, **args)
    create_symlinks('config', config.config_files, **args)
    create_symlinks('bin', config.bin_files, **args)

def parse_arguments() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(
        prog='dotfiles.py',
        description='Script for managing dotfiles',
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='enable extra debug messages',
    )
    parser.add_argument(
        '-p', '--plain', action='store_true',
        help='disable coloured messages',
    )
    parser.add_argument(
        '-m', '--generate-man-pages', action='store_true',
        help='(task) generate man pages containing notes and move them to the appropriate directory',
    )
    parser.add_argument(
        '-s', '--create-symlinks', action='store_true',
        help='(task) create symlinks for the dotfiles',
    )
    parser.add_argument(
        '-f', '--disable-safe-mode', action='store_true',
        help=f'disable safe mode, this means that existing dotfiles will be deleted instead of being moved to "{Path.home() / ".found_dotfiles"}" (only applies to --create-symlinks)',
    )
    parser.add_argument(
        'repository_path', type=str,
        help='path to the repository with the dotfiles and manpages',
    )
    return parser, parser.parse_args()

def main():
    tasks_ran = 0
    def run_task(condition: bool, task):
        nonlocal tasks_ran
        if condition:
            task()
            tasks_ran += 1

    parser, args = parse_arguments()
    config = Config(args)
    logger = Logger(config)
    logger.debug(f'Arguments: {args}')

    if not config.repository_path.exists():
        logger.error(f'Repository path "{config.repository_path}" does not exist')

    run_task(
        config.generate_man_pages,
        lambda: generate_man_pages(config, logger),
    )

    run_task(
        config.create_symlinks,
        lambda: create_dotfile_symlinks(config, logger),
    )

    logger.info(logger.colour(Colour.Green, f'Finished running {tasks_ran} tasks'))

if __name__ == '__main__':
    main()
