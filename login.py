import json
import os
from datetime import datetime
import gradio as gr

# File to store user data and activity logs
USER_DB = "user_activity.json"

# Initialize user database if it doesn't exist
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({"users": {}, "sessions": []}, f)

def log_activity(username, email, activity):
    """Log user activity to the JSON file"""
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "username": username,
        "email": email,
        "activity": activity
    }
    
    with open(USER_DB, "r+") as f:
        data = json.load(f)
        data["sessions"].append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

def authenticate(username, email):
    """Simple authentication and user registration"""
    if not username or not email:
        return False, "Username and email are required"
    
    with open(USER_DB, "r") as f:
        data = json.load(f)
    
    # Store basic user info if new user
    if email not in data["users"]:
        data["users"][email] = {
            "username": username,
            "email": email,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat()
        }
        with open(USER_DB, "w") as f:
            json.dump(data, f, indent=2)
    
    log_activity(username, email, "User logged in")
    return True, "Login successful"

def login_page():
    """Create the Gradio login interface"""
    with gr.Blocks() as login_interface:
        gr.Markdown("## Welcome to Honestly.ai - Please Login")
        
        with gr.Row():
            username = gr.Textbox(label="Username", placeholder="Enter your username")
            email = gr.Textbox(label="Email", placeholder="Enter your email address")
        
        login_button = gr.Button("Login")
        status = gr.Textbox(label="Status", interactive=False)
        
        login_button.click(
            authenticate,
            inputs=[username, email],
            outputs=[status]
        )
    
    return login_interface

if __name__ == "__main__":
    login_interface = login_page()
    login_interface.launch()