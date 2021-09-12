#
# ~/.sym_links.py
#

from pathlib import Path
import os

# path variables
source      = '~/Repos/dotfiles'
config_dest = '~/.config'
config_src  = f'{source}/.config'

# rc files
# [source, destination]
rc_files = [
    [f'{source}/.bashrc',  '~'],
    [f'{source}/.zshrc',   '~'],
    [f'{source}/.vimrc',   '~'],
    [f'{source}/.inputrc', '~'],
]

# config files
# [source, destination]
config_files = [
    [f'{config_src}/kitty/kitty.conf', f'{config_dest}/kitty/kitty.conf'],
    [f'{source}/.sh_aliases', '~'],
]

def make_symlinks(files):
    for pair in files:
        src_path  = Path(pair[0])
        dest_path = Path(pair[1])
        file_name = src_path.name

        # ensure destination directories exist
        if pair[1] != '~':
            print('Ensuring {0} has a valid symlink destination...'.format(pair[1]))
            path = str(dest_path.parent.resolve())
            os.makedirs(path, exist_ok=True)

        # replace existing file with symlink
        new_dest_path = dest_path / file_name
        if (new_dest_path).exists():
            print('Path {0} already exists, removing file...'.format(new_dest_path))
            os.remove(new_dest_path)

        os.symlink(src_path, new_dest_path)
        print('Created symlink ({0}) -> ({1})'.format(src_path, new_dest_path))

def main():
    print('Creating rc file symlinks...')
    make_symlinks(rc_files)
    print('Finished creating rc file symlinks.')

    print('Creating config file symlinks...')
    make_symlinks(config_files)
    print('Finished creating config file symlinks.')

if __name__ == '__main__':
    main()
