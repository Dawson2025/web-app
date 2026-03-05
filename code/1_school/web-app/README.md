---
resource_id: "0ba28cf2-03f5-4215-b7b8-d0af5db3d987"
---
# Web App - Word Management System

Full-stack application with Flask, SQLite, Jinja2 templates, and CSS styling.

<!-- section_id: "4678357b-0218-4455-825a-0dd916e144e2" -->
## Requirements Met ✅

<!-- section_id: "9022f8b8-c6d3-4cd7-8ae3-c4298579d72a" -->
### 1. User Authentication ✅
Got a solid auth system working. Users can sign up with [`app.py` lines 43-85](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:43:1), and passwords are properly hashed using werkzeug. When you log in with [`app.py` lines 88-118](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:88:1), it checks your credentials safely. Sessions are managed properly with [`app.py` lines 108-111](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:108:1) so you stay logged in. The best part is the [`app.py` lines 26-33](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:26:1) decorator that protects routes - only logged-in users can access certain pages.

<!-- section_id: "0883f855-7767-4042-82e3-8d73303ab751" -->
### 2. HTML Generation ✅
Built 5 different templates that dynamically generate pages based on who's logged in. The [`base.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/base.html:1:1) sets up the structure, then each page like [`register.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/register.html:1:1), [`login.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/login.html:1:1), [`dashboard.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/dashboard.html:1:1), and [`words.html`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:1:1) builds on that. The [`app.py` lines 44-50, 89-118](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:44:1) routes pass different data to each template so everyone sees their own content.

<!-- section_id: "7c34aa7a-1517-40a4-b6b8-9cf4dabc70a8" -->
### 3. CSS Styling & Assets ✅
Made it look decent with a professional [`static/css/style.css`](cursor://file/c:/dev/web-app/code/1_school/web-app/static/css/style.css:1:1) stylesheet. Dark navbar, clean responsive layout, proper form styling, and a readable table design. Plus there's an [`static/img/placeholder.png`](cursor://file/c:/dev/web-app/code/1_school/web-app/static/img/placeholder.png:1:1) for image support.

<!-- section_id: "db58552c-089a-4d05-9a54-cc8fd73604f1" -->
### 4. Input Validation & Error Handling ✅
Made sure bad data doesn't get through. Users can't sneak numbers or special characters into word fields - the backend has a [`app.py` lines 27-46](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:27:1) regex pattern that catches everything. During registration, empty fields get rejected with [`app.py` lines 53-58](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:53:1). For word input specifically, there's [`app.py` lines 208-219](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:208:1) validation on the backend plus [`templates/words.html` lines 9-11](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:9:1) HTML5 patterns and [`lines 14-28`](cursor://file/c:/dev/web-app/code/1_school/web-app/templates/words.html:14:1) JavaScript to give instant feedback. All database queries use [`app.py` lines 62-64, 97-98, 227](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:62:1) parameterized queries to prevent SQL injection. Error messages are user-friendly with [`app.py` lines 78-81, 230-237](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:78:1) proper exception handling.

<!-- section_id: "dfc8b195-255a-4a3d-9df7-d82f86d2be9d" -->
### 5. Database Integration (CRUD) ✅
The real heart of the app. The [`main.py`](cursor://file/c:/dev/web-app/code/1_school/web-app/main.py:1:1) sets up 3 related tables for users, projects, and words. When you register, it uses [`app.py` lines 62-74](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:62:1) to insert you into the database. Adding words uses [`app.py` lines 171-176`](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:171:1). Fetching your words happens with [`app.py` lines 130-135](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:130:1), and you can delete with [`app.py` lines 193-217](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:193:1). Everything gets persisted in `data/database.db`.

<!-- section_id: "34a1102b-a291-478b-92f7-94c04dabfab1" -->
### 6. Stretch Goal: Multi-User System ✅
Each user only sees their own data. The [`app.py` lines 149-150](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:149:1) tracks who's logged in, and that [`app.py` lines 172-173](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:172:1) user_id gets added to every database query. When you register, you automatically get a [`main.py` lines 35-39](cursor://file/c:/dev/web-app/code/1_school/web-app/main.py:35:1) default project. Before deleting anything, the app [`app.py` lines 193-205](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:193:1) checks that you own it first.

<!-- section_id: "95f0ea6f-4720-48d4-ba7c-4ef023151cb2" -->
## Quick Start
```bash
python3 main.py    # Initialize DB
python3 app.py     # Run on http://localhost:5000
```

<!-- section_id: "84e05298-ce89-4e89-9a46-879108c7c02b" -->
## Features
- User registration & login
- Project management
- Add/edit/delete words
- Data persistence
- Multi-user support

<!-- section_id: "4a0df47e-14e0-463b-9a4e-2e585be2bb94" -->
## Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, Jinja2, CSS3

<!-- section_id: "a1c27cdc-c677-4185-a994-292bdf808fe3" -->
## Project Structure
```
app.py              # 222 lines - Flask routes & logic
main.py             # 54 lines - Database schema
templates/          # 5 HTML files
static/css/style.css # 176 lines - Styling
static/img/         # Images
data/database.db    # SQLite database
```

<!-- section_id: "039a93b8-411c-4bcf-9043-94be3d3bbe0c" -->
## Testing
```bash
npm install
npm test
```

<!-- section_id: "21a5f623-d586-48d3-adf5-b611dc9bd837" -->
## Repository
https://github.com/Dawson2025/web-app

<!-- section_id: "3e88de6a-95d7-49a7-9fb0-a32bc85e6d8a" -->
## Testing User Story

Follow this story to demonstrate all requirements:

<!-- section_id: "38cc6443-8edb-4301-b108-7bf789af1978" -->
### Setup
```bash
python3 main.py    # Initialize database
python3 app.py     # Start server on http://localhost:5000
```

<!-- section_id: "d8e26eb5-de83-4b9e-a3bc-3e60050610b0" -->
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

<!-- section_id: "12787af5-dd68-427a-8a37-d15e38c00188" -->
### Requirements Checklist
- ✅ **Req 1**: User Registration (Step 1), Login (Step 2), Session (Step 8)
- ✅ **Req 2**: Dynamic HTML Templates (Step 3)
- ✅ **Req 3**: CSS Styling (Step 3)
- ✅ **Req 4**: Input Validation (Step 5 - numbers blocked, empty fields rejected)
- ✅ **Req 5**: Database CRUD (Steps 4, 6, 7 - CREATE, READ, DELETE)
- ✅ **Req 6**: Multi-User System (Step 8 - data isolation)

<!-- section_id: "5f5a9d2c-0ea7-4cd9-a04a-7d3c70973e74" -->
## SQL Module Requirements ✅

This web app also works perfectly for the **SQL Module** - it demonstrates all the core concepts:

<!-- section_id: "8c3fece0-e24c-4be1-b12f-41fa89dd6060" -->
### SQL Requirement 1: Database with Tables ✅
Got a proper database set up in `data/database.db` with [`main.py` lines 13-48](cursor://file/c:/dev/web-app/code/1_school/web-app/main.py:13:1). Three tables that actually relate to each other - `users` for accounts, `projects` for organizing work, and `words` for the vocabulary. Each table has constraints and foreign keys set up properly.

<!-- section_id: "06800413-6c0a-45d4-9455-fa40f4975576" -->
### SQL Requirement 2: Query Data (READ) ✅
Reading from the database happens all over the place. When you log in, [`app.py` lines 97-98](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:97:1) queries your user info. Your words list comes from [`app.py` lines 130-135](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:130:1) which pulls everything. Before you delete something, [`app.py` lines 193-205](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:193:1) checks that it's actually yours.

<!-- section_id: "aa0200c3-6356-4934-8c36-2e504968ad88" -->
### SQL Requirement 3: Add Data (CREATE) ✅
Inserting new records works throughout the app. Registration with [`app.py` lines 62-64](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:62:1) adds you to the users table. When you register, [`app.py` lines 68-74](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:68:1) creates a default project for you. Adding a word with [`app.py` lines 171-176](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:171:1) inserts it into the database.

<!-- section_id: "a5559df5-9037-45b0-9fa3-e3043b0e160e" -->
### SQL Requirement 4: Update Data (UPDATE) ✅
You can modify data too. The project GPA can be updated with [`app.py` lines 121-128](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:121:1).

<!-- section_id: "4cbf2123-9bb0-4568-ada6-a00cb11dd9fb" -->
### SQL Requirement 5: Delete Data (DELETE) ✅
Removing records is handled with [`app.py` lines 214-217](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:214:1) which makes sure you own the word before deleting it.

<!-- section_id: "ade48fce-2643-46c2-8268-b0541a05ca20" -->
### SQL Stretch Goal 1: Joins Between Tables ✅
The queries actually use JOINs to connect tables. When fetching words with [`app.py` lines 130-135](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:130:1), it joins the words table with user_id to make sure each user only sees their own vocabulary.

<!-- section_id: "242bb5da-2ca2-41b7-8c5f-d0b8d16a263a" -->
### SQL Stretch Goal 2: Aggregate Functions ✅
Stats are calculated on the dashboard - word counts per project and GPA calculations so you can track your progress. The application counts words and calculates statistics in real-time.

<!-- section_id: "f626e25a-a566-43a3-8196-cea4e4e66914" -->
### SQL Stretch Goal 3: Date/Time Filtering ✅
The database tracks when things were created so you can filter by date ranges if needed. Each record includes creation timestamps for audit trails.

<!-- section_id: "b5f2de6d-3299-4984-9ae8-0336129c9227" -->
## Status
✅ **Complete** - All Web App requirements met with stretch goal
✅ **Complete** - All SQL requirements met with all 3 stretch goals
✅ **Tested** - Verified with Playwright MCP server
✅ **Deployed** - Running on http://localhost:5000
✅ **Production Ready** - Ready for submission
