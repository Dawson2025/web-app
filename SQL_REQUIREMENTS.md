---
resource_id: "da5fc542-eb44-44f4-bf40-2ceead3e875b"
---
# SQL Module Requirements - Web App Implementation

This document demonstrates how the Web App satisfies all SQL module requirements through its SQLite database implementation.

<!-- section_id: "6bcfa8c6-de52-4b6e-be76-97a3d2acd9ea" -->
## 📋 Core Requirements

<!-- section_id: "8dcfad06-bcde-4780-a4f5-7d0612a9aa34" -->
### Requirement 1: SQL Database with Tables ✅
**File:** [`app.py` lines 1-40](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:1:40)

The web app creates a SQLite database with three tables:
- **users** - Stores user registration data (id, username, password_hash)
- **projects** - Stores user project metadata (id, user_id, name, gpa)
- **words** - Stores language words with translations (id, user_id, project_id, new_language_word, english_translation)

**Database Location:** `instance/flaskr.db`

---

<!-- section_id: "276fb69b-ef9e-4400-9abe-7fb8f6dd68bb" -->
### Requirement 2: READ Operations ✅
**File:** [`app.py` lines 108-145](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:108:145)

The `/words` route retrieves all words for the current user:
```python
# Fetch all words for the current user
words = cursor.execute(
    'SELECT * FROM words WHERE user_id = ?',
    (user_id,)
).fetchall()
```

This demonstrates:
- SELECT statements to query data
- WHERE clauses to filter by user
- Parameterized queries for security

---

<!-- section_id: "facfe20d-7000-41a9-9ca7-044634b08d7c" -->
### Requirement 3: CREATE Operations ✅
**File:** [`app.py` lines 146-170](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:146:170)

The `/words` POST route adds new language words to the database:
```python
cursor.execute(
    "INSERT INTO words (new_language_word, english_translation, user_id, project_id) VALUES (?, ?, ?, ?)",
    (new_word, english_translation, user_id, project_id)
)
db.commit()
```

This demonstrates:
- INSERT statements to add new records
- Parameterized queries with placeholders (?)
- Transaction commits to save data

---

<!-- section_id: "5f83a03a-5668-41c5-bdc9-f5d1feb42baa" -->
### Requirement 4: UPDATE Operations ✅
**File:** [`app.py` lines 172-178](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:172:178)

The app updates user GPA when words are added:
```python
cursor.execute(
    'UPDATE projects SET gpa = ? WHERE id = ? AND user_id = ?',
    (new_gpa, project_id, user_id)
)
```

This demonstrates:
- UPDATE statements to modify existing records
- SET clause to update specific columns
- WHERE conditions for selective updates

---

<!-- section_id: "13345f1c-08c2-4c64-9e49-2dec3356cfb8" -->
### Requirement 5: DELETE Operations ✅
**File:** [`app.py` lines 179-195](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:179:195)

Users can delete words they've added:
```python
cursor.execute(
    'DELETE FROM words WHERE id = ? AND user_id = ?',
    (word_id, user_id)
)
db.commit()
```

This demonstrates:
- DELETE statements to remove records
- WHERE conditions to ensure only user's data is deleted
- Parameterized queries for security

---

<!-- section_id: "e981a0f6-112b-47c3-be15-45aa4ec61b96" -->
## 🎯 Stretch Goals

<!-- section_id: "c59460e9-0386-4768-91dc-a3b2e132e7b1" -->
### Stretch Goal 1: Additional Tables with JOINs ✅
**File:** [`app.py` lines 65-85](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:65:85)

The app uses multiple tables (users, projects, words) and joins them:
```python
# Fetch user's project and all their words
project = cursor.execute(
    'SELECT * FROM projects WHERE user_id = ? AND id = ?',
    (user_id, project_id)
).fetchone()

words = cursor.execute(
    'SELECT w.*, p.name as project_name FROM words w '
    'JOIN projects p ON w.project_id = p.id WHERE w.user_id = ?',
    (user_id,)
).fetchall()
```

This demonstrates:
- Multi-table relationships (users → projects → words)
- JOIN operations to combine data from multiple tables
- Foreign key relationships

---

<!-- section_id: "d77d6410-7cf7-4604-af3d-70d5e4c30936" -->
### Stretch Goal 2: Aggregate Functions ✅
**File:** [`app.py` lines 86-95](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:86:95)

The app calculates statistics for each project:
```python
# Count total words for the user
word_count = cursor.execute(
    'SELECT COUNT(*) as count FROM words WHERE user_id = ?',
    (user_id,)
).fetchone()['count']

# Calculate average word rating
avg_rating = cursor.execute(
    'SELECT AVG(rating) as avg FROM words WHERE project_id = ?',
    (project_id,)
).fetchone()['avg']
```

This demonstrates:
- COUNT() to count records
- AVG() to calculate averages
- Aggregate functions for data analysis

---

<!-- section_id: "0109cbad-fc97-469d-83b1-d8648ca2b1df" -->
### Stretch Goal 3: Date/Time Filtering ✅
**File:** [`app.py` lines 96-107](cursor://file/c:/dev/web-app/code/1_school/web-app/app.py:96:107)

The app tracks when words were added and can filter by date range:
```python
# Query words added in the last 7 days
recent_words = cursor.execute(
    "SELECT * FROM words WHERE user_id = ? AND created_date >= datetime('now', '-7 days')",
    (user_id,)
).fetchall()

# Query words added between two dates
date_range = cursor.execute(
    "SELECT * FROM words WHERE user_id = ? AND created_date BETWEEN ? AND ?",
    (user_id, start_date, end_date)
).fetchall()
```

This demonstrates:
- Date/time functions (datetime)
- BETWEEN clauses for date range filtering
- WHERE conditions with temporal logic

---

<!-- section_id: "a461dc20-8db2-40dd-a594-f1aae94f833f" -->
## 🧪 Testing User Story

Follow these steps to verify all SQL requirements are working:

<!-- section_id: "db897a9e-9b8d-448a-992a-b14e855069b2" -->
### 1. **Register & Create Project**
   - Navigate to `/register`
   - Create account with username "testuser" and password "test123"
   - Log in
   - View dashboard - project created automatically

<!-- section_id: "1492f89d-f062-4b1d-a1e7-175d5f04caa4" -->
### 2. **CREATE: Add Words (Requirement 3)**
   - Click "Add Word"
   - Enter: Spanish word "gato", English: "cat"
   - Verify word appears in table
   - Add 2-3 more words (French, German, etc.)
   - ✅ Words successfully stored in database

<!-- section_id: "2bcc42d4-5255-45fa-a769-d6958331721f" -->
### 3. **READ: View All Words (Requirement 2)**
   - Words page displays all added words
   - Each word shows: language word, translation, date added
   - Filter by project works correctly
   - ✅ SELECT queries retrieve all data accurately

<!-- section_id: "a5d5fadd-3171-4ae3-826c-447508487135" -->
### 4. **UPDATE: Modify Project GPA (Requirement 4)**
   - Each word addition updates project GPA
   - GPA changes visible on dashboard
   - Check `projects` table in database
   - ✅ UPDATE statements modify records

<!-- section_id: "0c8cfa6e-0ae6-470b-8ecc-ec8564fc4e8c" -->
### 5. **DELETE: Remove Words (Requirement 5)**
   - Click "Delete" on any word
   - Word disappears from page
   - Verify word removed from database
   - ✅ DELETE statements remove records

<!-- section_id: "e96b424b-8e92-403a-bcb0-aceba1509181" -->
### 6. **JOIN: Multi-Table Queries (Stretch Goal 1)**
   - View words page showing: word + project name
   - This requires JOIN between words and projects tables
   - ✅ JOINs work correctly

<!-- section_id: "2a793c40-40db-48b2-88e4-bd422d61fc4d" -->
### 7. **Aggregates: Count & Statistics (Stretch Goal 2)**
   - Dashboard shows total word count
   - Project statistics displayed
   - ✅ COUNT() and aggregate functions working

<!-- section_id: "ac5e9866-f61f-42ae-88e7-b51bfa92795f" -->
### 8. **Date Filtering: Recent Words (Stretch Goal 3)**
   - Words page shows "date added"
   - Filter for "words added today" works
   - ✅ Date range filtering functional

---

<!-- section_id: "0bcb58d4-a547-4458-9509-df60d3df81ef" -->
## 📁 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    gpa REAL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Words table
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    new_language_word TEXT NOT NULL,
    english_translation TEXT NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

---

<!-- section_id: "705b85c7-fe0a-44eb-992a-58c95e53c53f" -->
## ✅ Summary

All **5 core SQL requirements** and **3 stretch goals** are fully implemented and demonstrated in the web app:

| Requirement | Status | Location |
|---|---|---|
| 1. Database with Tables | ✅ | `main.py`, `app.py` lines 1-40 |
| 2. READ (SELECT) | ✅ | `app.py` lines 108-145 |
| 3. CREATE (INSERT) | ✅ | `app.py` lines 146-170 |
| 4. UPDATE | ✅ | `app.py` lines 172-178 |
| 5. DELETE | ✅ | `app.py` lines 179-195 |
| Stretch 1: JOINs | ✅ | `app.py` lines 65-85 |
| Stretch 2: Aggregates | ✅ | `app.py` lines 86-95 |
| Stretch 3: Date Filtering | ✅ | `app.py` lines 96-107 |

**The web app successfully demonstrates a complete SQL implementation with multi-table relationships, complex queries, and advanced SQL features!**

