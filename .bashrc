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
    echo "$red[Warning]$reset $1" >&2
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
# Prompt & Less
#

PS1="\[$green\]\u\[$reset\]@\[$green\]\h\[$reset\] \[$bold\]\[$cyan\]\w\[$reset\] \n\$ "
PS2='> '

# coloured less and man pages
# begin bold
export LESS_TERMCAP_mb="$bold"
# begin blink
export LESS_TERMCAP_md="$bold$yellow"
# begin reverse video
export LESS_TERMCAP_so="$bold$magenta"
# begin underline
export LESS_TERMCAP_us="$bold"
# reset bold & blink
export LESS_TERMCAP_me="$reset"
# reset reverse video
export LESS_TERMCAP_se="$(tput rmso)$reset"
# reset underline
export LESS_TERMCAP_ue="$(tput rmul)$reset"
# for some terminal applications
export GROFF_NO_SGR=1

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

# include dot files in globs
shopt -s dotglob

# convert a glob that evaluated to nothing to an empty string
shopt -s nullglob

# check for terminal resize after every command
shopt -s checkwinsize

# prepends cd to a file path
shopt -s autocd

