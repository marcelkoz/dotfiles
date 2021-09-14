#
# ~/.sym_links.py
#

from pathlib import Path
import os

# path variables
user_home   = str(Path.home())
source      = str(Path.home()  / 'Repos/dotfiles')
config_dest = str(Path.home()  / '.config')
config_src  = str(Path(source) / '.config')

# rc files
# [source, destination]
rc_files = [
    (f'{source}/.bashrc',  user_home),
    (f'{source}/.zshrc',   user_home),
    (f'{source}/.vimrc',   user_home),
    (f'{source}/.inputrc', user_home),
]

# config files
# [source, destination]
config_files = [
    (f'{config_src}/kitty/kitty.conf', f'{config_dest}/kitty'),
    (f'{source}/.sh_aliases',          user_home),
]

def make_symlinks(files):
    for pair in files:
        src_path  = Path(pair[0])
        dest_path = Path(pair[1])
        file_name = src_path.name

        # ensure destination directories exist
        if pair[1] != user_home:
            print('  Ensuring ({0}) has a valid symlink destination...'.format(pair[1]))
            path = dest_path.parent.resolve()
            os.makedirs(path, exist_ok=True)

        # replace existing file with symlink
        new_dest_path = dest_path / file_name
        if new_dest_path.exists():
            print('  ({0}) already exists, removing file...'.format(new_dest_path))
            os.remove(new_dest_path)

        os.symlink(src_path, new_dest_path)
        print('  Created symlink ({0}) -> ({1})'.format(src_path, new_dest_path))

def main():
    print('Creating rc file symlinks...')
    make_symlinks(rc_files)
    print('Finished creating rc file symlinks.', end='\n\n')

    print('Creating config file symlinks...')
    make_symlinks(config_files)
    print('Finished creating config file symlinks.')

if __name__ == '__main__':
    main()
