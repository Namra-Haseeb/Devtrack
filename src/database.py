import os
import sqlite3
import hashlib
from datetime import datetime


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "devtrack.db"
)


# =========================================================
# CONNECTION
# =========================================================

def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# PASSWORD HELPERS
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# SAFE COLUMN MIGRATION
# =========================================================

def ensure_column(
    cursor,
    table_name,
    column_name,
    column_definition
):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if column_name not in columns:

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name}
            {column_definition}
            """
        )


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            github_username TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # CAREER PROFILE
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS career_profile (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            github_username TEXT,

            target_role TEXT,

            experience_level TEXT,

            target_company TEXT,

            target_technologies TEXT,

            bio TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # SAVED JOB DESCRIPTIONS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_job_descriptions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            company TEXT,

            job_description TEXT,

            extracted_skills TEXT,

            match_percentage REAL DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # ROADMAP PROGRESS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roadmap_progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            role TEXT,

            completed_tasks TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # SKILLS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            skill_name TEXT,

            skill_level TEXT DEFAULT 'Beginner',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # DSA PROBLEMS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dsa_problems (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            problem_name TEXT,

            topic TEXT,

            difficulty TEXT,

            status TEXT DEFAULT 'Not Started',

            solution_url TEXT,

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # PROJECTS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            name TEXT,

            description TEXT,

            status TEXT DEFAULT 'Planning',

            progress INTEGER DEFAULT 0,

            technologies TEXT,

            github_url TEXT,

            live_url TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # JOBS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            company TEXT,

            role TEXT,

            location TEXT,

            status TEXT DEFAULT 'Saved',

            job_url TEXT,

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # GOALS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            description TEXT,

            category TEXT,

            target_date TEXT,

            progress INTEGER DEFAULT 0,

            status TEXT DEFAULT 'Active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # ACHIEVEMENTS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS achievements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            category TEXT,

            achievement_date TEXT,

            description TEXT,

            proof_url TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # RESUME
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resume_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE,

            full_name TEXT,

            email TEXT,

            phone TEXT,

            location TEXT,

            linkedin TEXT,

            github TEXT,

            summary TEXT,

            education TEXT,

            skills TEXT,

            experience TEXT,

            projects TEXT,

            achievements TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # ACTIVITY LOG
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_log (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            activity_type TEXT,

            activity_text TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # =====================================================
    # GITHUB CACHE
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS github_cache (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            username TEXT UNIQUE,

            profile_data TEXT,

            repos_data TEXT,

            events_data TEXT,

            analysis_data TEXT,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    conn.commit()

    # =====================================================
    # SAFE MIGRATIONS
    # =====================================================

    ensure_column(
        cursor,
        "users",
        "github_username",
        "TEXT"
    )

    ensure_column(
        cursor,
        "career_profile",
        "user_id",
        "INTEGER"
    )

    ensure_column(
        cursor,
        "career_profile",
        "github_username",
        "TEXT"
    )

    ensure_column(
        cursor,
        "career_profile",
        "bio",
        "TEXT"
    )

    ensure_column(
        cursor,
        "career_profile",
        "target_company",
        "TEXT"
    )

    ensure_column(
        cursor,
        "career_profile",
        "updated_at",
        "TIMESTAMP"
    )

    ensure_column(
        cursor,
        "saved_job_descriptions",
        "match_percentage",
        "REAL DEFAULT 0"
    )

    ensure_column(
        cursor,
        "roadmap_progress",
        "user_id",
        "INTEGER"
    )

    ensure_column(
        cursor,
        "roadmap_progress",
        "updated_at",
        "TIMESTAMP"
    )

    conn.commit()
    conn.close()


# =========================================================
# USER AUTHENTICATION
# =========================================================

def create_user(
    name,
    email,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        password_hash = hash_password(
            password
        )

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        user_id = cursor.lastrowid

        conn.commit()

        return user_id

    except sqlite3.IntegrityError:

        return None

    finally:

        conn.close()


# =========================================================
# AUTHENTICATE USER
# =========================================================

def authenticate_user(
    email,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(
        password
    )

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        AND password_hash = ?
        """,
        (
            email,
            password_hash
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


# =========================================================
# GET USER
# =========================================================

def get_user_by_id(
    user_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


def get_user_by_email(
    email
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


# =========================================================
# UPDATE GITHUB USERNAME
# =========================================================

def update_user_github_username(
    user_id,
    github_username
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE users
        SET github_username = ?
        WHERE id = ?
        """,
        (
            github_username,
            user_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# CAREER PROFILE
# =========================================================

def save_career_profile(
    username=None,
    target_role="",
    experience_level="",
    target_technologies=None,
    user_id=None,
    bio="",
    target_company="",
    github_username=None
):

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # Support both:
    # username=
    # github_username=
    # -----------------------------------------------------

    if github_username is not None:

        username = github_username

    if username is None:

        username = ""

    if target_technologies is None:

        target_technologies = []

    technologies = (
        ", ".join(target_technologies)
        if isinstance(
            target_technologies,
            list
        )
        else str(target_technologies)
    )

    existing = None

    # -----------------------------------------------------
    # Find profile by logged-in user
    # -----------------------------------------------------

    if user_id is not None:

        cursor.execute(
            """
            SELECT id
            FROM career_profile
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        existing = cursor.fetchone()

    # -----------------------------------------------------
    # If no profile is linked to user yet,
    # try to find an old profile by GitHub username.
    # This prevents old saved data from being lost.
    # -----------------------------------------------------

    if existing is None and username:

        cursor.execute(
            """
            SELECT id
            FROM career_profile
            WHERE github_username = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (username,)
        )

        existing = cursor.fetchone()

    # -----------------------------------------------------
    # UPDATE EXISTING PROFILE
    # -----------------------------------------------------

    if existing:

        cursor.execute(
            """
            UPDATE career_profile
            SET
                user_id = ?,
                github_username = ?,
                target_role = ?,
                experience_level = ?,
                target_technologies = ?,
                bio = ?,
                target_company = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                user_id,
                username,
                target_role,
                experience_level,
                technologies,
                bio,
                target_company,
                existing["id"]
            )
        )

    # -----------------------------------------------------
    # CREATE NEW PROFILE
    # -----------------------------------------------------

    else:

        cursor.execute(
            """
            INSERT INTO career_profile
            (
                user_id,
                github_username,
                target_role,
                experience_level,
                target_technologies,
                bio,
                target_company
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                target_role,
                experience_level,
                technologies,
                bio,
                target_company
            )
        )

    conn.commit()
    conn.close()


# =========================================================
# GET CAREER PROFILE
# =========================================================

def get_career_profile(
    username=None,
    user_id=None
):

    conn = get_connection()
    cursor = conn.cursor()

    profile = None

    # -----------------------------------------------------
    # FIRST: Find using logged-in user ID
    # -----------------------------------------------------

    if user_id is not None:

        cursor.execute(
            """
            SELECT *
            FROM career_profile
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

    # -----------------------------------------------------
    # SECOND: If not found, find using GitHub username
    # -----------------------------------------------------

    if profile is None and username:

        cursor.execute(
            """
            SELECT *
            FROM career_profile
            WHERE github_username = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (username,)
        )

        profile = cursor.fetchone()

    conn.close()

    if profile:

        return dict(profile)

    return None


# =========================================================
# SAVED JOB DESCRIPTIONS
# =========================================================

def save_job_description(
    title,
    company,
    job_description,
    extracted_skills,
    match_percentage=0,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO saved_job_descriptions
        (
            user_id,
            title,
            company,
            job_description,
            extracted_skills,
            match_percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            company,
            job_description,
            extracted_skills,
            match_percentage
        )
    )

    conn.commit()
    conn.close()


def get_saved_jobs(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM saved_job_descriptions
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM saved_job_descriptions
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# ROADMAP
# =========================================================

def save_roadmap_progress(
    role,
    completed_tasks,
    user_id=None
):

    conn = get_connection()

    existing = None

    if user_id is not None:

        existing = conn.execute(
            """
            SELECT id
            FROM roadmap_progress
            WHERE user_id = ?
            AND role = ?
            """,
            (
                user_id,
                role
            )
        ).fetchone()

    if existing:

        conn.execute(
            """
            UPDATE roadmap_progress
            SET
                completed_tasks = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                completed_tasks,
                existing["id"]
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO roadmap_progress
            (
                user_id,
                role,
                completed_tasks
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                role,
                completed_tasks
            )
        )

    conn.commit()
    conn.close()


def get_roadmap_progress(
    username=None,
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM roadmap_progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM roadmap_progress
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# SKILLS
# =========================================================

def save_skill(
    skill_name,
    skill_level="Beginner",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO skills
        (
            user_id,
            skill_name,
            skill_level
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            skill_name,
            skill_level
        )
    )

    conn.commit()
    conn.close()


def get_skills(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM skills
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM skills
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def delete_skill(
    skill_id,
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        conn.execute(
            """
            DELETE FROM skills
            WHERE id = ?
            AND user_id = ?
            """,
            (
                skill_id,
                user_id
            )
        )

    else:

        conn.execute(
            """
            DELETE FROM skills
            WHERE id = ?
            """,
            (skill_id,)
        )

    conn.commit()
    conn.close()


# =========================================================
# DSA
# =========================================================

def add_dsa_problem(
    problem_name,
    topic,
    difficulty,
    status="Not Started",
    solution_url="",
    notes="",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO dsa_problems
        (
            user_id,
            problem_name,
            topic,
            difficulty,
            status,
            solution_url,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            problem_name,
            topic,
            difficulty,
            status,
            solution_url,
            notes
        )
    )

    conn.commit()
    conn.close()


def get_dsa_problems(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM dsa_problems
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM dsa_problems
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def update_dsa_problem(
    problem_id,
    status,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE dsa_problems
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            problem_id
        )
    )

    conn.commit()
    conn.close()


def delete_dsa_problem(
    problem_id,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM dsa_problems
        WHERE id = ?
        """,
        (problem_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# PROJECTS
# =========================================================

def add_project(
    name,
    description="",
    status="Planning",
    progress=0,
    technologies="",
    github_url="",
    live_url="",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO projects
        (
            user_id,
            name,
            description,
            status,
            progress,
            technologies,
            github_url,
            live_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            name,
            description,
            status,
            progress,
            technologies,
            github_url,
            live_url
        )
    )

    conn.commit()
    conn.close()


def get_projects(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM projects
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM projects
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def update_project(
    project_id,
    name,
    description,
    status,
    progress,
    technologies,
    github_url,
    live_url,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE projects
        SET
            name = ?,
            description = ?,
            status = ?,
            progress = ?,
            technologies = ?,
            github_url = ?,
            live_url = ?
        WHERE id = ?
        """,
        (
            name,
            description,
            status,
            progress,
            technologies,
            github_url,
            live_url,
            project_id
        )
    )

    conn.commit()
    conn.close()


def delete_project(
    project_id,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM projects
        WHERE id = ?
        """,
        (project_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# JOB TRACKER
# =========================================================

def add_job(
    company,
    role,
    location="",
    status="Saved",
    job_url="",
    notes="",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO jobs
        (
            user_id,
            company,
            role,
            location,
            status,
            job_url,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            company,
            role,
            location,
            status,
            job_url,
            notes
        )
    )

    conn.commit()
    conn.close()


def get_jobs(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM jobs
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM jobs
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def update_job_status(
    job_id,
    status,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE jobs
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            job_id
        )
    )

    conn.commit()
    conn.close()


def delete_job(
    job_id,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# GOALS
# =========================================================

def add_goal(
    title,
    description="",
    category="Career",
    target_date="",
    progress=0,
    status="Active",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO goals
        (
            user_id,
            title,
            description,
            category,
            target_date,
            progress,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            description,
            category,
            target_date,
            progress,
            status
        )
    )

    conn.commit()
    conn.close()


def get_goals(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM goals
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def update_goal(
    goal_id,
    title,
    description,
    category,
    target_date,
    progress,
    status,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE goals
        SET
            title = ?,
            description = ?,
            category = ?,
            target_date = ?,
            progress = ?,
            status = ?
        WHERE id = ?
        """,
        (
            title,
            description,
            category,
            target_date,
            progress,
            status,
            goal_id
        )
    )

    conn.commit()
    conn.close()


def delete_goal(
    goal_id,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM goals
        WHERE id = ?
        """,
        (goal_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# ACHIEVEMENTS
# =========================================================

def add_achievement(
    title,
    category,
    achievement_date="",
    description="",
    proof_url="",
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO achievements
        (
            user_id,
            title,
            category,
            achievement_date,
            description,
            proof_url
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            category,
            achievement_date,
            description,
            proof_url
        )
    )

    conn.commit()
    conn.close()


def get_achievements(
    user_id=None
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM achievements
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM achievements
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def delete_achievement(
    achievement_id,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM achievements
        WHERE id = ?
        """,
        (achievement_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# RESUME
# =========================================================

def save_resume_data(
    data,
    user_id=None
):

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        """
        SELECT id
        FROM resume_data
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    values = (
        data.get("full_name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", ""),
        data.get("linkedin", ""),
        data.get("github", ""),
        data.get("summary", ""),
        data.get("education", ""),
        data.get("skills", ""),
        data.get("experience", ""),
        data.get("projects", ""),
        data.get("achievements", "")
    )

    if existing:

        cursor.execute(
            """
            UPDATE resume_data
            SET
                full_name = ?,
                email = ?,
                phone = ?,
                location = ?,
                linkedin = ?,
                github = ?,
                summary = ?,
                education = ?,
                skills = ?,
                experience = ?,
                projects = ?,
                achievements = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            values + (user_id,)
        )

    else:

        cursor.execute(
            """
            INSERT INTO resume_data
            (
                user_id,
                full_name,
                email,
                phone,
                location,
                linkedin,
                github,
                summary,
                education,
                skills,
                experience,
                projects,
                achievements
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id,) + values
        )

    conn.commit()
    conn.close()


def get_resume_data(
    user_id=None
):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM resume_data
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    conn.close()

    if row:

        return dict(row)

    return {}


# =========================================================
# ACTIVITY
# =========================================================

def log_activity(
    activity_type,
    activity_text,
    user_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO activity_log
        (
            user_id,
            activity_type,
            activity_text
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            activity_type,
            activity_text
        )
    )

    conn.commit()
    conn.close()


def get_activity(
    user_id=None,
    limit=20
):

    conn = get_connection()

    if user_id is not None:

        rows = conn.execute(
            """
            SELECT *
            FROM activity_log
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT *
            FROM activity_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# GITHUB CACHE
# =========================================================

def save_github_cache(
    username,
    profile_data,
    repos_data,
    events_data,
    analysis_data,
    user_id=None
):

    import json

    conn = get_connection()

    profile_json = json.dumps(
        profile_data
    )

    repos_json = json.dumps(
        repos_data
    )

    events_json = json.dumps(
        events_data
    )

    analysis_json = json.dumps(
        analysis_data
    )

    existing = conn.execute(
        """
        SELECT id
        FROM github_cache
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    if existing:

        conn.execute(
            """
            UPDATE github_cache
            SET
                user_id = ?,
                profile_data = ?,
                repos_data = ?,
                events_data = ?,
                analysis_data = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE username = ?
            """,
            (
                user_id,
                profile_json,
                repos_json,
                events_json,
                analysis_json,
                username
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO github_cache
            (
                user_id,
                username,
                profile_data,
                repos_data,
                events_data,
                analysis_data
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                profile_json,
                repos_json,
                events_json,
                analysis_json
            )
        )

    conn.commit()
    conn.close()


def get_github_cache(
    username
):

    import json

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM github_cache
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    conn.close()

    if not row:

        return None

    data = dict(row)

    try:

        data["profile_data"] = json.loads(
            data["profile_data"]
        )

    except Exception:
        pass

    try:

        data["repos_data"] = json.loads(
            data["repos_data"]
        )

    except Exception:
        pass

    try:

        data["events_data"] = json.loads(
            data["events_data"]
        )

    except Exception:
        pass

    try:

        data["analysis_data"] = json.loads(
            data["analysis_data"]
        )

    except Exception:
        pass

    return data


# =========================================================
# DASHBOARD STATS
# =========================================================

def get_dashboard_stats(
    user_id=None
):

    stats = {
        "projects": 0,
        "completed_projects": 0,
        "jobs": 0,
        "applications": 0,
        "interviews": 0,
        "offers": 0,
        "goals": 0,
        "completed_goals": 0,
        "achievements": 0,
        "skills": 0
    }

    conn = get_connection()

    if user_id is not None:

        stats["projects"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM projects
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

        stats["completed_projects"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM projects
            WHERE user_id = ?
            AND status = 'Completed'
            """,
            (user_id,)
        ).fetchone()[0]

        stats["jobs"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

        stats["applications"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE user_id = ?
            AND status = 'Applied'
            """,
            (user_id,)
        ).fetchone()[0]

        stats["interviews"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE user_id = ?
            AND status = 'Interview'
            """,
            (user_id,)
        ).fetchone()[0]

        stats["offers"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE user_id = ?
            AND status = 'Offer'
            """,
            (user_id,)
        ).fetchone()[0]

        stats["goals"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

        stats["completed_goals"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
            AND status = 'Completed'
            """,
            (user_id,)
        ).fetchone()[0]

        stats["achievements"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM achievements
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

        stats["skills"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM skills
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

    conn.close()

    return stats


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()