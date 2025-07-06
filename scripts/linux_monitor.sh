#!/usr/bin/env bash

# Script: monitor.sh
# Description: Start a tmux session named "monitor",
# split into 3 panes: left top (htop), left bottom (nvtop), right (btop),
# then attach in a new terminal.

SESSION=monitor

# Get tmux base indices to handle different configurations
get_base_indices() {
  BASE_INDEX=$(tmux show-options -gv base-index 2>/dev/null || echo 0)
  PANE_BASE_INDEX=$(tmux show-options -gv pane-base-index 2>/dev/null || echo 0)
}

# Create session if it doesn't exist
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Creating new tmux session: $SESSION"
  
  # Get base indices
  get_base_indices
  echo "Using base-index: $BASE_INDEX, pane-base-index: $PANE_BASE_INDEX"
  
  # Start a new detached tmux session
  tmux new-session -d -s "$SESSION"
  
  # Wait for session to be fully created
  sleep 0.2
  
  # Split into left and right panes (vertical split)
  tmux split-window -h -t "$SESSION:$BASE_INDEX"
  sleep 0.1
  
  # Split the left pane into top and bottom (horizontal split)
  # Target the first pane of the first window
  tmux split-window -v -t "$SESSION:$BASE_INDEX.$PANE_BASE_INDEX"
  sleep 0.1
  
  # Calculate pane indices based on base index
  PANE1=$PANE_BASE_INDEX
  PANE2=$((PANE_BASE_INDEX + 1))
  PANE3=$((PANE_BASE_INDEX + 2))
  
  echo "Pane layout:"
  echo "  - Pane $PANE1: left top (htop)"
  echo "  - Pane $PANE2: left bottom (nvtop)"
  echo "  - Pane $PANE3: right (btop)"
  
  # Launch htop in left top pane
  tmux send-keys -t "$SESSION:$BASE_INDEX.$PANE1" 'htop' C-m
  
  # Launch nvtop in left bottom pane
  tmux send-keys -t "$SESSION:$BASE_INDEX.$PANE2" 'nvtop' C-m
  
  # Launch btop in right pane
  tmux send-keys -t "$SESSION:$BASE_INDEX.$PANE3" 'btop' C-m
  
  echo "All monitoring tools launched successfully"
else
  echo "Session $SESSION already exists"
fi

# Attach to the session in a new terminal or fallback
if command -v gnome-terminal >/dev/null 2>&1; then
  gnome-terminal -- tmux attach -t "$SESSION"
elif command -v xterm >/dev/null 2>&1; then
  xterm -e tmux attach -t "$SESSION" &
elif command -v konsole >/dev/null 2>&1; then
  konsole -e tmux attach -t "$SESSION" &
else
  # Fallback: attach in current terminal
  echo "Attaching to session in current terminal..."
  tmux attach -t "$SESSION"
fi
