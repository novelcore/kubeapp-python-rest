#!/bin/bash

# Check if this is a recognized project structure
if [ -f "app/pyproject.toml" ] && [ -f "app/app/main.py" ]; then
    PROMPT="Hello! I'm your Kubecore DevOps Assistant. Welcome to your Python REST API repository!

🎯 **You're in your Python REST API repository**
This is your FastAPI-powered microservice, ready for development and deployment.

📊 **Current Project Status:**
  • Framework: FastAPI with Poetry dependency management
  • Architecture: RESTful API with comprehensive system
  • Testing: Unit testing infrastructure ready
  • Deployment: GitOps workflow with automated CI/CD
  • Branch Strategy: GitFlow for organized development

🚀 **What would you like to work on today?**

**🔧 New Feature Development:**
  • \"I want to create a new API endpoint\"
  • \"I need to add a new feature\"
  • \"Let's build a new service\"

**🧪 Testing & Quality:**
  • \"I need to add unit tests\"
  • \"Test my current changes\"
  • \"Validate my implementation\"

**🚀 Release Management:**
  • \"I'm ready to create a release\"
  • \"I need to deploy a hotfix\"
  • \"Help me with the release process\"

**📋 Planning & Documentation:**
  • \"I want to create a PRD\"
  • \"Help me plan a new feature\"
  • \"Track my development progress\"

**❓ General Help:**
  • \"Show me the project structure\"
  • \"What can I do here?\"
  • \"How does the workflow work?\"

Just tell me what you'd like to work on, and I'll connect you with the right specialist! 🎉

The specialized agents are available through the .cursor/rules system and will automatically activate based on your requests."
else
    PROMPT="Hello! Please analyze this codebase and suggest what I should work on first. @Kubecore DevOps Assistant"
fi

# Open Cursor
cursor . &
sleep 4

# Copy the prompt to clipboard using pbcopy
echo "$PROMPT" | pbcopy

# Send prompt to Cursor using AppleScript
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
        
        # Paste the prompt from clipboard
        keystroke "v" using {command down}
        delay 0.5
        
        # Submit with Enter
        keystroke return
    end tell
end tell
EOF