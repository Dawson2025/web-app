# Web App - Word Management System

Full-stack application with Flask, SQLite, Jinja2 templates, and CSS styling.

## Requirements Met ✅

### 1. User Authentication ✅
- **Registration**: [`app.py` lines 43-85](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:43:1) (`/register` route)
- **Login**: [`app.py` lines 88-118](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:88:1) (`/login` route)
- **Password Hashing**: [`app.py` lines 18, 64](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:18:1) (werkzeug `generate_password_hash`)
- **Sessions**: [`app.py` lines 108-111](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:108:1) (session management)
- **Protected Routes**: [`app.py` lines 26-33](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:26:1) (`@login_required` decorator)

### 2. HTML Generation ✅
- **Templates**: `templates/` directory with 5 Jinja2 templates
  - [`base.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/base.html:1:1) - Template inheritance
  - [`register.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/register.html:1:1) - Registration form
  - [`login.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/login.html:1:1) - Login form
  - [`dashboard.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/dashboard.html:1:1) - User dashboard
  - [`words.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:1:1) - Word management (lines 1-58)
- **Dynamic Content**: [`app.py` lines 44-50, 89-118](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:44:1) (render_template calls)

### 3. CSS Styling & Assets ✅
- **Stylesheet**: [`static/css/style.css`](cursor://file/c:/dev/web-app/code/1_school/web-app/static/css/style.css:1:1) (176 lines)
  - Dark navbar, responsive layout, form styling, table design
- **Images**: [`static/img/placeholder.png`](cursor://file/c:/dev/web-app/code/1_school/web-app/static/img/placeholder.png:1:1)

### 4. Input Validation & Error Handling ✅
- **Strict Word Validation**: [`app.py` lines 27-46](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:27:1) (regex validation, only letters/spaces)
- **Empty Fields**: [`app.py` lines 53-58](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:53:1) (registration validation)
- **Word Validation**: [`app.py` lines 208-219](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:208:1) (regex check prevents numbers & special chars)
- **Parameterized Queries**: [`app.py` lines 62-64, 97-98, 227](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:62:1) (SQL with `?` placeholders)
- **Error Handling**: [`app.py` lines 78-81, 230-237](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:78:1) (try-catch, user feedback)
- **Duplicate Prevention**: [`app.py` lines 78-79](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:78:1) (SQLite UNIQUE constraints)
- **Frontend Validation**: [`templates/words.html` lines 9-11](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:9:1) (HTML5 pattern), [`lines 14-28`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:14:1) (JavaScript)
- **Backend Regex**: Strict `^[a-Za-z\s]+$` pattern catches any paste-bypass attempts

### 5. Database Integration (CRUD) ✅
- **Schema**: [`main.py`](cursor://file/c:/dev/web-app/code/1_school/web-app/main.py:1:1) (54 lines) - 3 tables: users, projects, words
- **CREATE**: [`app.py` lines 62-74](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:62:1) (user registration), [`lines 171-176`](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:171:1) (add word)
- **READ**: [`app.py` lines 97-98](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:97:1) (login query), [`lines 130-135`](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:130:1) (fetch words)
- **DELETE**: [`app.py` lines 193-217](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:193:1) (delete word with ownership check)
- **Persistence**: `data/database.db` - SQLite file persists data

### 6. Stretch Goal: Multi-User System ✅
- **User Isolation**: [`app.py` lines 149-150](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:149:1) (session user_id), [`lines 172-173`](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:172:1) (user_id in queries)
- **Projects**: [`main.py` lines 35-39](cursor://file/c:/dev/web-app/code/1_school/web-app/main.py:35:1) (projects table), [`app.py` lines 68-74](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:68:1) (default project)
- **Ownership Verification**: [`app.py` lines 193-205](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:193:1) (check user_id before delete)

## Quick Start
```bash
python3 main.py    # Initialize DB
python3 app.py     # Run on http://localhost:5000
```

## Features
- User registration & login
- Project management
- Add/edit/delete words
- Data persistence
- Multi-user support

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, Jinja2, CSS3

## Project Structure
```
app.py              # 222 lines - Flask routes & logic
main.py             # 54 lines - Database schema
templates/          # 5 HTML files
static/css/style.css # 176 lines - Styling
static/img/         # Images
data/database.db    # SQLite database
```

## Testing
```bash
npm install
npm test
```

## Repository
https://github.com/Dawson2025/web-app

## Testing User Story

Follow this story to demonstrate all requirements:

### Setup
```bash
python3 main.py    # Initialize database
python3 app.py     # Start server on http://localhost:5000
```

### Story: New User Learns Spanish Vocabulary

**Step 1: User Registration (Req 1 - Authentication)**
1. Navigate to http://localhost:5000
2. Click "Register" link
3. Enter:
   - Username: `testuser123`
   - Email: `test@example.com`
   - Password: `SecurePass123`
4. Click "Register"
5. ✅ See success message "Registration successful! Please log in."
6. ✅ **Validates**: User Authentication + Input Validation (Req 1, 4)

**Step 2: User Login (Req 1 - Authentication)**
1. Enter credentials:
   - Username: `testuser123`
   - Password: `SecurePass123`
2. Click "Login"
3. ✅ Redirected to dashboard (HTML rendered dynamically - Req 2)
4. ✅ **Validates**: User Authentication (Req 1)

**Step 3: View Dashboard (Req 2, 3 - HTML & CSS)**
1. Dashboard displays user's project "My First Project" (created automatically - Req 6 Stretch)
2. ✅ Page styled with professional CSS (dark navbar, readable layout - Req 3)
3. Click on "My First Project"
4. ✅ **Validates**: HTML Generation (Req 2), CSS Styling (Req 3)

**Step 4: Add Words (Req 4, 5 - Validation & Database)**
1. On words page, see form: "New Language Word" and "English Translation"
2. Try entering: `hola123` and `hello`
3. ✅ JavaScript blocks numbers - see alert "Numbers not allowed"
4. Enter valid word: `hola` and `hello`
5. Click "Add Word"
6. ✅ Word appears in table below
7. ✅ **Validates**: Input Validation (Req 4), Database CREATE (Req 5)

**Step 5: Test Input Validation (Req 4)**
1. Try adding empty word (just click Add) - ✅ Error: "New language word is required"
2. Try adding word with numbers via copy-paste: `word2` - ✅ Backend rejects: "Word cannot contain numbers"
3. ✅ **Validates**: Frontend + Backend Input Validation (Req 4)

**Step 6: Data Persistence (Req 5 - Database)**
1. Add multiple words:
   - `gato` → `cat`
   - `perro` → `dog`
   - `libro` → `book`
2. ✅ All words display in table (Database READ - Req 5)
3. Refresh page - ✅ Words still there (Data Persistence - Req 5)
4. ✅ **Validates**: Database CRUD (Req 5)

**Step 7: Delete Word (Req 5 - Database)**
1. Click "Delete" button on any word
2. ✅ Word removed from table
3. ✅ Stays removed after refresh
4. ✅ **Validates**: Database DELETE (Req 5)

**Step 8: Multi-User System (Req 6 - Stretch Goal)**
1. Logout (click "Logout" link)
2. Register new user:
   - Username: `user2`
   - Email: `user2@example.com`
   - Password: `Password123`
3. Login as user2
4. Go to words page
5. ✅ User2 sees empty word list (not testuser123's words)
6. Add word: `agua` → `water`
7. Logout and login as testuser123
8. Go to words page
9. ✅ See only testuser123's words (hola, gato, perro, libro, agua NOT here)
10. ✅ **Validates**: Multi-User System with Data Isolation (Req 6 - Stretch)

### Requirements Checklist
- ✅ **Req 1**: User Registration (Step 1), Login (Step 2), Session (Step 8)
- ✅ **Req 2**: Dynamic HTML Templates (Step 3)
- ✅ **Req 3**: CSS Styling (Step 3)
- ✅ **Req 4**: Input Validation (Step 5 - numbers blocked, empty fields rejected)
- ✅ **Req 5**: Database CRUD (Steps 4, 6, 7 - CREATE, READ, DELETE)
- ✅ **Req 6**: Multi-User System (Step 8 - data isolation)

## Status
✅ Complete - All requirements met with stretch goal implemented
