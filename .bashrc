#
# Custom ~/.bashrc
#

# if not interactive
[ -z "PS1" ] && return

#
# Colours
#

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

#
# Helper Functions
#

# $1 = warning message to the user
warn_user()
{
    echo "$red[Warning]$reset $1"
}

# $1 = path to file
# return value = success of sourcing file
source_file()
{
    if [ -f "$1" ]
    then
        source $1
        return 0
    fi
    
    warn_user "Could not find or source file '$1'"
    return 1
}

#
# Prompt
#

PS1="\[$green\]\u\[$reset\]@\[$green\]\h\[$reset\] \[$bold\]\[$cyan\]\w\[$reset\] \n\$ "
PS2='> '

#
# Bash History
#

# ignore duplicate history entries
HISTCONTROL=ignoreboth

# history size
HISTFILESIZE=2000
HISTSIZE=2000

# appends entries to history instead of overwriting
shopt -s histappend

#
# Misc
#

# load command aliases
source_file "$HOME/.sh_aliases"

# enable bash completion
source_file '/usr/share/bash-completion/bash_completion' 

# enable extended globs
shopt -s extglob

# check for terminal resize after every command
shopt -s checkwinsize

# prepends cd to a file path
shopt -s autocd

