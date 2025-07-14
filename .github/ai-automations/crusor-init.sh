#!/bin/bash
PROMPT="@welcome-agent"

# Open Cursor
cursor . &
sleep 4

# Send prompt to Cursor
osascript << EOF
tell application "Cursor"
    activate
    delay 2
end tell

tell application "System Events"
    tell process "Cursor"
        # Open chat with Cmd+L
        keystroke "l" using {command down}
        delay 1
        
        # Type the prompt
        keystroke "$PROMPT"
        delay 0.5
        
        # Submit with Enter
        keystroke return
    end tell
end tell
EOF