#
# Custom ~/.zshrc
#

# if not interactive
[ -z "PS1" ] && return

#
# Zsh History
#

# ignore duplicate history entries
HISTCONTROL=ignoredups

# history size
HISTFILESIZE=2000
HISTSIZE=2000

#
# Command Aliases
#

[ -f ~/.sh_aliases ] && source ~/.sh_aliases

#
# Prompt
#

PS1='%F{green}%n%f@%F{green}%M %B%F{cyan}%~%f%b
%# '
PS2='> '

#
# Misc
#

setopt extendedglob

