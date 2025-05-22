#!/usr/bin/env bash

# Script: monitor.sh
# Description: Start a tmux session named "monitor",
# split into 3 panes: left top (htop), left bottom (nvtop), right (btop),
# then attach in a new terminal.

SESSION=monitor

# Create session if it doesn't exist
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  # Start a new detached tmux session
  tmux new-session -d -s "$SESSION"

  # Split into left and right panes (vertical split)
  tmux split-window -h -t "$SESSION"

  # Split the left pane (pane 0) into top and bottom (horizontal split)
  tmux split-window -v -t "$SESSION:0.0"

  # Pane layout:
  #  - "$SESSION:0.0" => left top
  #  - "$SESSION:0.1" => left bottom
  #  - "$SESSION:0.2" => right full height

  # Launch htop in left top pane
  tmux send-keys -t "$SESSION:0.0" 'htop' C-m

  # Launch nvtop in left bottom pane
  tmux send-keys -t "$SESSION:0.1" 'nvtop' C-m

  # Launch btop in right pane
  tmux send-keys -t "$SESSION:0.2" 'btop' C-m
fi

# Attach to the session in a new terminal or fallback
if command -v gnome-terminal >/dev/null 2>&1; then
  gnome-terminal -- tmux attach -t "$SESSION"
else
  # Fallback: attach in current terminal
  tmux attach -t "$SESSION"
fi
