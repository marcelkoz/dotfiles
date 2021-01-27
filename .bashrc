#
# Custom ~/.bashrc
#

# if not interactive
[ -z "PS1" ] && return

#
# Bash History
#

# ignore duplicate history entries
HISTCONTROL=ignoredups

# history size
HISTFILESIZE=2000
HISTSIZE=2000

# appends entries to history instead of overwriting
shopt -s histappend

#
# Command Aliases
#

[ -f ~/.sh_aliases ] && source ~/.sh_aliases

#
# Prompt
#

# colours
magenta=$(tput setaf 5)
yellow=$(tput setaf 3)
black=$(tput setaf 0)
green=$(tput setaf 2)
white=$(tput setaf 7)
blue=$(tput setaf 4)
cyan=$(tput setaf 6)
red=$(tput setaf 1)

# modifiers
reset=$(tput sgr0)
bold=$(tput bold)

PS1="\[$green\]\u\[$reset\]@\[$green\]\h\[$reset\] \[$bold\]\[$cyan\]\w\[$reset\] \n\$ "
PS2='> '

#
# Misc
#

# enable extended globs
shopt -s extglob

# check for terminal resize after every command
shopt -s checkwinsize

# prepends cd to a file path
shopt -s autocd

