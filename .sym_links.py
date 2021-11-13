#
# ~/.sym_links.py
#

from pathlib import Path
import os

# safe mode
# any duplicate files will be moved to a special .sym_links_duplicates directory instead of being deleted
safe_mode = True

indent = '  '

# path variables
user_home   = Path.home()
dup_dest    = user_home / '.sym_links_duplicates'
source      = user_home / 'Repos/dotfiles'
config_dest = user_home / '.config'
config_src  = source    / '.config'

# rc files
# (source, destination)
rc_files = (
    (f'{source}/.bashrc',  user_home),
    (f'{source}/.zshr',   user_home),
    (f'{source}/.vimrc',   user_home),
    (f'{source}/.inputrc', user_home),
)

# config files
# (source, destination)
config_files = (
    (f'{config_src}/kitty/kitty.conf', f'{config_dest}/kitty'),
    (f'{source}/.sh_aliases',          user_home),
)

class InvalidPairError(Exception):
    def __init__(self, reason, pair):
        super().__init__(reason)
        self.pair = pair

def make_symlinks(files):
    for pair in files:
        src_path  = Path(pair[0])
        dest_path = Path(pair[1])
        file_name = src_path.name

        # ensure destination directories exist
        if pair[1] != user_home:
            print(indent, 'Ensuring ({0}) has a valid symlink destination...'.format(pair[1]))
            path = dest_path.parent.resolve()
            os.makedirs(path, exist_ok=True)

        # replace existing file with symlink
        new_dest_path = dest_path / file_name
        if new_dest_path.exists():
            if safe_mode:
                print(indent, '({0}) already exists, moving file...'.format(new_dest_path))
                os.rename(new_dest_path, dup_dest / file_name)
            else:
                print(indent, '({0}) already exists, removing file...'.format(new_dest_path))
                os.remove(new_dest_path)

        os.symlink(src_path, new_dest_path)
        print(indent, 'Created symlink ({0}) -> ({1})'.format(src_path, new_dest_path))

def verify_symlinks(files):
    for pair in files:
        if len(pair) != 2:
            raise InvalidPairError('not enough or too many items', pair)
        elif not all(map(lambda f: Path(f).exists(), pair)):
            raise InvalidPairError('not all locations exist', pair)

        print(indent, f'Verified ({pair[0]}) -> ({pair[1]})')

def make_files(file_type, files):
    print(f'Verifying {file_type} file symlinks...')
    verify_symlinks(files)
    print(f'Finished verifying {file_type} file symlinks.', end='\n\n')

    print(f'Creating {file_type} file symlinks...')
    make_symlinks(files)
    print(f'Finished creating {file_type} file symlinks.', end='\n\n')

def main():
    if safe_mode:
        os.makedirs(dup_dest, exist_ok=True)

    try:
        make_files('rc',     rc_files)
        make_files('config', config_files)
    except InvalidPairError as err:
        print(indent, f'Failed to verify pair, {err}: {err.pair}') 

if __name__ == '__main__':
    main()
