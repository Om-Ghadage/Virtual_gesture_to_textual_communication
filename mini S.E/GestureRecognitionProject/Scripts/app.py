



# from flask import Flask, render_template
# import subprocess
# import os

# # Go up one level from current script directory
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# # Create Flask app, pointing to template and static folders
# app = Flask(__name__,
#             template_folder=os.path.join(base_dir, 'templates'),
#             static_folder=os.path.join(base_dir, 'static'))

# @app.route('/')
# def home():
#     return render_template("homepage.html")

# @app.route('/start-camera')
# def start_camera():
#     try:
#         subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "classify_gestures.py")])
#         return "Gesture Recognition Started Successfully!"
#     except Exception as e:
#         return f"Failed to start gesture recognition: {str(e)}"

# if __name__ == '__main__':
#     app.run(debug=True)



# #updated with linking
# from flask import Flask, render_template
# import subprocess
# import os

# # Go up one level from current script directory
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# # Create Flask app, pointing to template and static folders
# app = Flask(__name__,
#             template_folder=os.path.join(base_dir, 'templates'),
#             static_folder=os.path.join(base_dir, 'static'))


# @app.route('/')
# def home():
#     return render_template("homepage.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

# @app.route('/privacy')
# def privacy():
#     return render_template("privacy.html")

# @app.route('/start-camera')
# def start_camera():
#     try:
#         subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "classify_gestures.py")])
#         return "Gesture Recognition Started Successfully!"
#     except Exception as e:
#         return f"Failed to start gesture recognition: {str(e)}"

# if __name__ == '__main__':
#     app.run(debug=True)




# new code
from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import hashlib

# Go up one level from current script directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__,
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

# Secret key for session management
app.secret_key = 'your_secret_key'  # Replace with a real secret key

users_file = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    # Check if the user is logged in by looking for their email in the session
    if 'email' not in session:
        return redirect(url_for('signup'))  # Redirect to signup if not logged in
    return render_template("homepage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        
        # Check if the email exists and password matches
        if email in users and users[email] == hash_password(password):
            session['email'] = email  # Store the user's email in the session
            return redirect(url_for('home'))  # Redirect to homepage if login is successful
        else:
            return render_template("VGTC.html", error="Invalid email or password.")
    return render_template("VGTC.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        # Check if passwords match
        if password != confirm:
            return render_template("signup.html", error="Passwords do not match.")

        users = load_users()
        
        # Check if user already exists
        if email in users:
            return render_template("signup.html", error="User already exists.")

        # Save the new user to the users file
        users[email] = hash_password(password)
        save_users(users)
        
        session['email'] = email  # Store the user's email in the session
        return redirect(url_for('home'))  # Redirect to homepage after successful signup

    return render_template("signup.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/start-camera')
def start_camera():
    import subprocess
    try:
        subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "classify_gestures.py")])
        return "Gesture Recognition Started Successfully!"
    except Exception as e:
        return f"Failed to start gesture recognition: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
