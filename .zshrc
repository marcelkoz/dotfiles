#
# Custom ~/.zshrc
#

# if not interactive
[ -z "PS1" ] && return

# zsh

# if run from a terminal
DISPLAY_FORMATTING=$TERM
if [[ $DISPLAY_FORMATTING ]]
then
    autoload -U colors && colors
fi

#
# Helper Functions
#

# $1: warning message to the user
warn_user()
{
    if [[ $DISPLAY_FORMATTING ]]
    then
        print -P -- "%F{red}[Warning]%f $1" >&2
    else
        echo "[Warning] $1" >&2
    fi
}

# $1: path to file
# returns success of sourcing file
source_file()
{
    if [ -f "$1" ]
    then
        source $1
        return 0
    fi
    
    warn_user "Could not find file ($1)"
    return 1
}

#
# Prompt
#

PS1='%F{green}%n%f@%F{green}%M %B%F{cyan}%~%f%b
%# '
PS2='> '

#
# Zsh History
#

# ignore duplicate history entries
HISTCONTROL=ignoredups

# history size
HISTFILESIZE=2000
HISTSIZE=2000

#
# Misc
#

# crtl + r to search history
bindkey '^R' history-incremental-search-backward

# load command aliases
source_file "$HOME/.sh_aliases"

# enable extended globs
setopt extendedglob

# prepend cd to a file path
setopt autocd

# case insensitive completion
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
