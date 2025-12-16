from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import functools
import re  # For regex validation
import main # Import main.py for DB_NAME and migrate_schema

# --- Configuration ---
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your_super_secret_key_here' # IMPORTANT: Change this in production!

# --- Helper Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(main.DB_NAME)
        db.row_factory = sqlite3.Row # Return rows as dict-like objects
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def is_valid_word(word):
    """
    Req 4: Input Validation - Strict validation for words
    Only allows letters (A-Z, a-z) and spaces.
    Returns: (is_valid: bool, error_message: str)
    """
    # Check for empty string
    if not word or not word.strip():
        return False, "Word cannot be empty"
    
    # Check length (reasonable bounds)
    if len(word) > 100:
        return False, "Word is too long (max 100 characters)"
    
    # Regex: only letters and spaces allowed
    # ^[a-zA-Z\s]+$ means: start, one or more letters/spaces, end
    if not re.match(r'^[a-zA-Z\s]+$', word):
        return False, "Word can only contain letters and spaces (no numbers or special characters)"
    
    return True, None


def login_required(view):
    """
    Req 1: User Authentication - Decorator for protected routes
    Checks if user_id is in session. If not, redirects to login page.
    Used to restrict access to dashboard and words pages for logged-in users only.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Req 1: Authentication - Check if user has active session
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    """
    REQ 1: User Authentication - Registration Route
    Handles both GET (show form) and POST (process registration)
    """
    if request.method == 'POST':
        # Req 4: Input Validation - Extract user input from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        error = None

        # Req 4: Input Validation - Check for empty/missing required fields
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                # Req 1: Authentication - Secure password hashing using werkzeug
                # Req 5: Database CREATE - Insert new user with hashed password
                # Req 4: Security - Use parameterized query (?, ?, ?) to prevent SQL injection
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password))
                )
                db.commit()

                # Req 6: Stretch Goal - Create default project for new user (multi-user system)
                user_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO projects (name, user_id) VALUES (?, ?)",
                    ("My First Project", user_id)
                )
                db.commit()
                
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                error = f"User {username} or email {email} is already registered."
            except Exception as e:
                error = f"An unexpected error occurred: {e}"
        
        flash(error, 'danger')

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    """
    Req 1: User Authentication - Login Route
    Handles both GET (show login form) and POST (process login credentials)
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        error = None
        
        # Req 5: Database READ - Query user by username
        # Req 4: Security - Use parameterized query (?) to prevent SQL injection
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        user = cursor.fetchone()

        # Req 1: Authentication - Validate username exists
        if user is None:
            error = 'Incorrect username.'
        # Req 1: Authentication - Validate password using secure hash comparison
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # Req 1: Authentication - Create user session after successful login
            session['user_id'] = user['id']
            session['username'] = user['username'] # Store username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash(error, 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()

    # Get user's projects
    cursor.execute("SELECT id, name FROM projects WHERE user_id = ?", (user_id,))
    projects = cursor.fetchall()
    
    # Select the first project or provide a placeholder
    current_project_id = projects[0]['id'] if projects else None
    current_project_name = projects[0]['name'] if projects else "No Project Selected"

    session['current_project_id'] = current_project_id # Store current project in session
    session['current_project_name'] = current_project_name

    return render_template('dashboard.html', projects=projects, current_project_name=current_project_name)


@app.route('/words', methods=('GET', 'POST'))
@login_required
def words():
    user_id = session['user_id']
    project_id = session.get('current_project_id')
    db = get_db()
    cursor = db.cursor()
    
    if project_id is None:
        flash('Please select a project from the dashboard to manage words.', 'warning')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Req 4: Input Validation - Get and clean user input
        new_word = request.form['new_language_word'].strip()
        english_translation = request.form['english_translation'].strip()
        error = None

        # Req 4: Input Validation - Use regex helper function for strict validation
        is_valid_new_word, word_error = is_valid_word(new_word)
        if not is_valid_new_word:
            error = word_error
        
        # Req 4: Input Validation - Validate translation using same rules
        is_valid_translation, translation_error = is_valid_word(english_translation)
        if not error and not is_valid_translation:
            error = f"Translation: {translation_error}"
        
        # Req 4: Input Validation - Only proceed if all validation passes
        if error is None:
            try:
                # Req 5: Database CREATE - Insert new word
                # Req 4: Security - Use parameterized query (?, ?, ?, ?) to prevent SQL injection
                # Req 6: Stretch Goal - Store user_id & project_id for multi-user data isolation
                cursor.execute(
                    "INSERT INTO words (new_language_word, english_translation, user_id, project_id) VALUES (?, ?, ?, ?)",
                    (new_word, english_translation, user_id, project_id)
                )
                db.commit()
                flash(f'Word "{new_word}" added successfully!', 'success')
            except Exception as e:
                error = f"Error adding word: {e}"
        
        if error:
            flash(error, 'danger')

    # Req 2: HTML Generation - Generate words.html template with dynamic content
    # Req 5: Database READ - Query words for the current user and project
    # Req 4: Security - Use parameterized query (?, ?) to prevent SQL injection
    # Req 6: Stretch Goal - Only return words for THIS user (user_id), ensuring data isolation
    cursor.execute(
        "SELECT id, new_language_word, english_translation FROM words WHERE user_id = ? AND project_id = ? ORDER BY created_at DESC",
        (user_id, project_id)
    )
    words_list = cursor.fetchall()
    return render_template('words.html', words=words_list, current_project_name=session.get('current_project_name'))

@app.route('/words/delete/<int:word_id>', methods=('POST',))
@login_required
def delete_word(word_id):
    """
    Req 5: Database DELETE - Delete a word by ID
    Req 6: Stretch Goal - Verify ownership before deletion (security/multi-user)
    """
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Req 6: Stretch Goal - Ownership verification (ensure user owns this word)
        # Req 4: Security - Use parameterized query (?, ?) to prevent SQL injection
        cursor.execute("SELECT 1 FROM words WHERE id = ? AND user_id = ?", (word_id, user_id))
        if cursor.fetchone() is None:
            flash("You do not have permission to delete this word.", "danger")
            return redirect(url_for('words'))

        cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
        db.commit()
        flash("Word deleted successfully!", 'success')
    except Exception as e:
        flash(f"Error deleting word: {e}", 'danger')
    
    return redirect(url_for('words'))


# --- Run App ---
if __name__ == '__main__':
    # Ensure database schema is migrated when app starts
    with app.app_context():
        os.makedirs(os.path.dirname(main.DB_NAME), exist_ok=True) # Ensure data directory exists
        main.migrate_schema()
    app.run(debug=True, port=5000)