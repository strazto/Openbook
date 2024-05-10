#!/bin/bash

activate () {
  . .venv/bin/activate
  echo Virtual Environment Activated Successfully
}

activate

# flask --app openbook run --debug



## remote start attempt

# https://stackoverflow.com/questions/31902929/how-to-write-a-shell-script-that-starts-tmux-session-and-then-runs-a-ruby-scrip

# also write a git automation script

# ssh web
# tmux new-session -d -s my_session 'make waitress'
