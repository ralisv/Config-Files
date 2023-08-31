export PATH="$HOME/Executables:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"

COMMON_TEXT_COLOR="\e[38;2;255;255;255m"
ERROR_TEXT_COLOR="\e[38;2;255;0;0m"

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

alias python="python3.10"
alias pip="python -m pip"
alias R="R --no-save -q"
alias c="clear"
alias uncomment='egrep -v "^[[:space:]]*[/ *][*/]|^$"'
alias sl="sl -e"
alias s="ls"
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
alias la="ls -a"
alias du="du -h"
# Wrappers for convenience

function wiki() {
	wikit --line "$(($COLUMNS - 15))" "$@"	
}

function okular() {
	setsid okular "$@" &
}

function element() {
	setsid gelemental "$@" 2>/dev/null 
}

alias trans="~/Executables/trans -j -d -t czech"
alias překladač="trans"
alias překlad="trans"

alias maisa='sshfs "xralis@aisa.fi.muni.cz:/home/xralis" /home/ralis/aisa'
alias aisa='ssh "xralis@aisa.fi.muni.cz"'
alias drive='setsid rclone mount Google-Drive:Drive ~/Drive'


alias valgrind='colour-valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --track-origins=yes --show-reachable=yes --track-fds=yes -s'
alias stackusage='colour-valgrind --tool=drd --show-stack-usage=yes'

alias bashrc="micro ~/.bashrc; source ~/.bashrc"

alias is='setsid firefox -new-tab "https://is.muni.cz/auth/student/" 2>/dev/null'

function lion() {
	setsid clion $@ 2>/dev/null
}
function yt() {
	if [ -z $1 ]; then
		setsid brave-browser "https://www.youtube.com/" 2>/dev/null 1>/dev/null
	else
		to_search=`echo "$@" | awk 'BEGIN {FS=" ";OFS="+"} {$1=$1; print $0}'`
		setsid brawe-browser "https://www.youtube.com/results?search_query=$to_search" 2>/dev/null 1>/dev/null
	fi
}


function idos() {
	setsid brave-browser "https://idos.idnes.cz/vlakyautobusymhdvse/spojeni/vysledky/?f=$1&fc=1&t=$2&tc=1"
}

function -() {
	to_search=`echo "$@" | awk 'BEGIN {FS=" ";OFS="+"} {$1=$1; print $0}'`
	setsid brave-browser "https://www.google.com/search?channel=fs&client=ubuntu&q=$to_search" 2>/dev/null 1>/dev/null
}

function okular() {
	for f; do
		if [ -f $f ]; then
		 	setsid /bin/okular $f 2>/dev/null &
		else
		 	echo -e "${ERROR_TEXT_COLOR}Failed to open: $f${COMMON_TEXT_COLOR}" >&2
		fi
	done
}

function libreoffice() {
	setsid /bin/libreoffice $@ 2>/dev/null
}
function topdf() {
	gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=out.pdf -dBATCH $@
}

function play() {
	setsid vlc $@ 2>/dev/null
}


PS1="\[\e[38;2;255;180;50m\]\u.[\w] λ \[$COMMON_TEXT_COLOR\]"
PS1="$PS1"

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth
# append to the history file, don't overwrite it
shopt -s histappend
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=10000
HISTFILESIZE=20000
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi


# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# math functions

function calc() {
	exp="$(echo "$@" | sed 's/\^/**/g')"
	echo "print($exp)" | python3
}

function sqrt() {
	if  ! test -z "$2"; then
		power=`echo "1/$2" | bc -l`
		echo "print($1**$power)" | python3
	else
		echo "print($1**0.5)" | python3
	fi
}


function bin() {
	echo "ibase=10; obase=2; $1" | bc -l
}

function hex() {
	echo "ibase=10; obase=16; $1" | bc -l
}

function oct() {
	echo "ibase=10; obase=16; $1" | bc -l
}

function pi() {
	echo "scale=10; 4*a(1)" | bc -l
	}


# random functions

function timer() {
	start=`date +%s.%N`
	$1 > /dev/null
	end=`date +%s.%N`
	echo "$end-$start" | bc -l
}

# Colored man pages

export LESS_TERMCAP_mb=$'\e[1;32m'
export LESS_TERMCAP_md=$'\e[38;2;255;180;50m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[38;2;255;255;50m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[38;2;255;100;50m'

# Colored ls

LS_COLORS='rs=0:di=38;2;0;200;255:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*.pdf=38;2;255;0;200:';
export LS_COLORS


# colored GCC warnings and errors

export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

alias diablo='wine ~/games/Diablo-II/game.exe'
