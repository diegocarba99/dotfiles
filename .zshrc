# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Dependencies for this file
#########################################
#  - zoxiode (brew install zoxide)
#  - fzf (brew install fzf)
#  - NerdFonts (brew install --cask font-jetbrains-mon-nerd-font)
#  - zsh (brew install zsh)


# MacOS specific config - make brew installed apps avaiable in path
#########################################
eval "$(/opt/homebrew/bin/brew shellenv)"


# Directories in path
#########################################
# Example: PATH="$HOME/example/path:$PATHq"


# Aliases
#########################################
alias q="exit"
alias l="ls"
alias ll="ls -l"
alias la="ls -al"
alias c="clear"
alias pip="pip3"
alias ..="cd ./.."
alias dev="cd $HOME/dev"
alias restart-homepage="docker stop homepage; docker rm homepage; docker rmi homepage; docker build -t homepage ~/dev/homepage/; docker run --name homepage --restart=unless-stopped -p 8081:3000 -d homepage"
alias t='tmux'
alias st='subl'
alias kali='docker attach kalimotxo'
alias gche='git checkout'
alias gadd='git add .'
alias gcom='git commit -a -m'
alias gpush='git push origin $(git symbolic-ref --short HEAD)'
alias gpull='git pull origin $(git symbolic-ref --short HEAD)'
alias gdel='git branch -d'
alias gdiff-comm=' git log --branches --not --remotes'
alias tmuxcheat='bat $HOME/.tmux.cheatsheet'
alias talos-run-preprod='f() {
  pyenv activate talos
  export AWS_PROFILE="heritage_talos-engine"
  python $HOME/dev/talos-batch/run.py -r eu-west-1 -e preprod -p $1
  pyenv deactivate
};f'

# Set the directory we want to store zinit and plugins
#########################################
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
   mkdir -p "$(dirname $ZINIT_HOME)"
   git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
#########################################
source "${ZINIT_HOME}/zinit.zsh"


# Add in Powerlevel10k
#########################################
zinit ice depth=1; zinit light romkatv/powerlevel10k


# Add in zsh plugins
#########################################
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab


# Add in snippets using snipped loading
#########################################
# https://github.com/zdharma-continuum/zinit#loading-and-unloading
# Plugins for OhMyZSH are available in 
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins
zinit snippet OMZL::git.zsh
zinit snippet OMZP::git
zinit snippet OMZP::sudo
zinit snippet OMZP::archlinux
zinit snippet OMZP::aws
zinit snippet OMZP::kubectl
zinit snippet OMZP::kubectx
zinit snippet OMZP::command-not-found

# Load completions
#########################################
autoload bashcompinit; bashcompinit
autoload -Uz compinit; compinit

# Replay all cached completions
#########################################
zinit cdreplay -q


# Shell integrations
#########################################
eval "$(fzf --zsh)"
eval "$(zoxide init --cmd cd zsh)"

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh


# History
#########################################
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups


# Completion styling
#########################################
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'

## Custom functions
#########################################

new-blog-entry() {
  if [ $# -eq 0 ]; then
    echo "Please provide the name of the new article"
    exit
  fi

  title="$1"
  blog_dir="$HOME/diejdev/blog/content"

  cd
  title_lower=$(echo $title | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
  new_dir="$blog_dir/$(date "+%Y%m%d")-$title_lower"

  if [ -d "$new_dir" ]; then
    echo "Directory '$new_dir' already exists."
  else
    mkdir -p "$new_dir"
    touch "$new_dir/$title_lower.md"
    cd $new_dir
    echo "New directory created in $(pwd)"
  fi

}
