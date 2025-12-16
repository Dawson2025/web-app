from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import functools
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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password))
                )
                db.commit()

                # Create a default project for the new user
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        error = None
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
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
        new_word = request.form['new_language_word'].strip()
        english_translation = request.form['english_translation'].strip()
        error = None

        if not new_word:
            error = 'New language word is required.'
        elif not english_translation:
            error = 'English translation is required.'
        
        # --- Requirement: Perform error checking on the input from the user ---
        if error is None:
            try:
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

    # --- Requirement: Generate at least 1 HTML page from the app ---
    # --- Requirement: Modify content of HTML generated by the app based on user input ---
    # This route serves words.html which lists words (modified by user input)
    cursor.execute(
        "SELECT id, new_language_word, english_translation FROM words WHERE user_id = ? AND project_id = ? ORDER BY created_at DESC",
        (user_id, project_id)
    )
    words_list = cursor.fetchall()
    return render_template('words.html', words=words_list, current_project_name=session.get('current_project_name'))

@app.route('/words/delete/<int:word_id>', methods=('POST',))
@login_required
def delete_word(word_id):
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Ensure user owns the word
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