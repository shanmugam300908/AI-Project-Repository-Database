from flask import Flask, request, redirect, url_for
import sqlite3
from html import escape

app = Flask(__name__)

DATABASE = "ai_project_repository.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def create_database():

    db = get_db()
    cursor = db.cursor()

    # -------------------------
    # Project
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            description TEXT,
            domain TEXT,
            status TEXT,
            created_date TEXT
        )
    """)

    # -------------------------
    # Dataset
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dataset (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            source TEXT,
            dataset_type TEXT,
            project_id INTEGER,
            FOREIGN KEY (project_id)
                REFERENCES Project(project_id)
                ON DELETE CASCADE
        )
    """)

    # -------------------------
    # AI Model
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AI_Model (
            model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            model_type TEXT,
            accuracy REAL,
            project_id INTEGER,
            FOREIGN KEY (project_id)
                REFERENCES Project(project_id)
                ON DELETE CASCADE
        )
    """)

    # -------------------------
    # Member
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT NOT NULL,
            role TEXT,
            email TEXT
        )
    """)

    # -------------------------
    # Repository
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Repository (
            repository_id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository_name TEXT NOT NULL,
            repository_url TEXT,
            platform TEXT,
            project_id INTEGER,
            FOREIGN KEY (project_id)
                REFERENCES Project(project_id)
                ON DELETE CASCADE
        )
    """)

    db.commit()
    db.close()


# =========================================================
# COMMON HTML
# =========================================================

def page_start(title):

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <title>{escape(title)}</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                color: #222;
            }}

            .header {{
                background: #172554;
                color: white;
                padding: 25px;
                text-align: center;
            }}

            .header h1 {{
                margin: 0;
            }}

            .nav {{
                background: white;
                padding: 15px;
                text-align: center;
                box-shadow: 0 2px 5px #ccc;
            }}

            .nav a {{
                text-decoration: none;
                color: #172554;
                font-weight: bold;
                margin: 0 10px;
            }}

            .container {{
                width: 90%;
                max-width: 1200px;
                margin: 30px auto;
            }}

            .dashboard {{
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin: 25px 0;
            }}

            .stat {{
                background: white;
                padding: 25px;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0 3px 10px #ddd;
            }}

            .stat .icon {{
                font-size: 32px;
            }}

            .stat h2 {{
                font-size: 32px;
                margin: 10px;
                color: #172554;
            }}

            .stat p {{
                margin: 0;
                font-weight: bold;
                color: #555;
            }}

            .cards {{
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }}

            .card {{
                background: white;
                padding: 22px;
                border-radius: 12px;
                box-shadow: 0 3px 10px #ddd;
            }}

            .card h2 {{
                color: #172554;
            }}

            .button {{
                display: inline-block;
                padding: 10px 16px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 7px;
                border: none;
                cursor: pointer;
                font-size: 15px;
            }}

            .delete {{
                background: #dc2626;
            }}

            .green {{
                background: #16a34a;
            }}

            .orange {{
                background: #f59e0b;
            }}

            .form-box {{
                background: white;
                max-width: 650px;
                margin: 30px auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 10px #ddd;
            }}

            input,
            textarea,
            select {{
                width: 100%;
                padding: 11px;
                margin: 8px 0 18px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 15px;
            }}

            textarea {{
                height: 100px;
                resize: vertical;
            }}

            label {{
                font-weight: bold;
            }}

            .search {{
                display: flex;
                gap: 10px;
                margin: 20px 0;
            }}

            .search input {{
                margin: 0;
            }}

            .footer {{
                margin-top: 50px;
                padding: 20px;
                text-align: center;
                background: #172554;
                color: white;
            }}

            .badge {{
                display: inline-block;
                padding: 6px 10px;
                background: #dcfce7;
                color: #166534;
                border-radius: 15px;
                font-weight: bold;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🤖 AI PROJECT REPOSITORY</h1>

            <p>
                Centralized Database Management System
            </p>

        </div>

        <div class="nav">

            <a href="/">
                🏠 Dashboard
            </a>

            <a href="/projects">
                📁 Projects
            </a>

            <a href="/datasets">
                💾 Datasets
            </a>

            <a href="/models">
                🤖 AI Models
            </a>

            <a href="/members">
                👥 Members
            </a>

            <a href="/repositories">
                🔗 Repositories
            </a>

        </div>
    """


def page_end():

    return """
        <div class="footer">

            AI Project Repository |
            Python + Flask + SQLite

        </div>

    </body>

    </html>
    """


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM Project")
    projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Dataset")
    datasets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM AI_Model")
    models = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Member")
    members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Repository")
    repositories = cursor.fetchone()[0]

    cursor.execute("""
        SELECT project_id,
               project_name,
               domain,
               status,
               created_date
        FROM Project
        ORDER BY project_id DESC
    """)

    project_list = cursor.fetchall()

    db.close()

    html = page_start("Dashboard")

    html += f"""

    <div class="container">

        <h1 style="text-align:center;">
            📊 Dashboard
        </h1>

        <div class="dashboard">

            <div class="stat">
                <div class="icon">📁</div>
                <h2>{projects}</h2>
                <p>Total Projects</p>
            </div>

            <div class="stat">
                <div class="icon">💾</div>
                <h2>{datasets}</h2>
                <p>Total Datasets</p>
            </div>

            <div class="stat">
                <div class="icon">🤖</div>
                <h2>{models}</h2>
                <p>AI Models</p>
            </div>

            <div class="stat">
                <div class="icon">👥</div>
                <h2>{members}</h2>
                <p>Team Members</p>
            </div>

            <div class="stat">
                <div class="icon">🔗</div>
                <h2>{repositories}</h2>
                <p>Repositories</p>
            </div>

        </div>


        <div style="text-align:center; margin:25px;">

            <a class="button" href="/project/add">
                ➕ Add Project
            </a>

        </div>


        <h2>
            📁 Recent Projects
        </h2>

        <div class="cards">
    """

    if not project_list:

        html += """
            <div class="card">
                <h2>No Projects Yet</h2>
                <p>
                    Add your first AI project using
                    the Add Project button.
                </p>
            </div>
        """

    for project in project_list:

        project_id = project[0]
        name = escape(str(project[1]))
        domain = escape(str(project[2] or ""))
        status = escape(str(project[3] or ""))
        date = escape(str(project[4] or ""))

        html += f"""

            <div class="card">

                <h2>
                    {name}
                </h2>

                <p>
                    <b>Domain:</b> {domain}
                </p>

                <p>
                    <b>Status:</b>
                    <span class="badge">
                        {status}
                    </span>
                </p>

                <p>
                    <b>Date:</b> {date}
                </p>

                <a
                    class="button delete"
                    href="/project/delete/{project_id}"
                    onclick="return confirm('Delete this project?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """

        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# PROJECTS
# =========================================================

@app.route("/projects")
def projects_page():

    search = request.args.get("search", "")

    db = get_db()
    cursor = db.cursor()

    if search:

        cursor.execute("""
            SELECT *
            FROM Project
            WHERE project_name LIKE ?
               OR domain LIKE ?
               OR description LIKE ?
            ORDER BY project_id DESC
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM Project
            ORDER BY project_id DESC
        """)

    projects = cursor.fetchall()

    db.close()

    html = page_start("Projects")

    html += """

    <div class="container">

        <h1>📁 Projects</h1>

        <form class="search" method="GET">

            <input
                type="text"
                name="search"
                placeholder="Search project..."
                value="
    """ + escape(search) + """
            ">

            <button class="button" type="submit">
                🔍 Search
            </button>

        </form>

        <p>
            <a class="button" href="/project/add">
                ➕ Add Project
            </a>
        </p>

        <div class="cards">

    """

    for project in projects:

        project_id = project[0]

        name = escape(str(project[1]))
        description = escape(str(project[2] or ""))
        domain = escape(str(project[3] or ""))
        status = escape(str(project[4] or ""))
        date = escape(str(project[5] or ""))

        html += f"""

            <div class="card">

                <h2>
                    {name}
                </h2>

                <p>
                    <b>Description:</b><br>
                    {description}
                </p>

                <p>
                    <b>Domain:</b>
                    {domain}
                </p>

                <p>
                    <b>Status:</b>
                    {status}
                </p>

                <p>
                    <b>Created:</b>
                    {date}
                </p>

                <a
                    class="button delete"
                    href="/project/delete/{project_id}"
                    onclick="return confirm('Delete this project?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """
        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# ADD PROJECT
# =========================================================

@app.route("/project/add", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        name = request.form["project_name"]
        description = request.form["description"]
        domain = request.form["domain"]
        status = request.form["status"]
        date = request.form["created_date"]

        db = get_db()

        db.execute("""
            INSERT INTO Project
            (
                project_name,
                description,
                domain,
                status,
                created_date
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            description,
            domain,
            status,
            date
        ))

        db.commit()
        db.close()

        return redirect(url_for("projects_page"))


    html = page_start("Add Project")

    html += """

    <div class="form-box">

        <h1>➕ Add Project</h1>

        <form method="POST">

            <label>Project Name</label>

            <input
                type="text"
                name="project_name"
                placeholder="Example: AI Treasure Hunt"
                required
            >

            <label>Description</label>

            <textarea
                name="description"
                placeholder="Enter project description"
                required
            ></textarea>

            <label>Domain</label>

            <input
                type="text"
                name="domain"
                placeholder="Example: Artificial Intelligence"
                required
            >

            <label>Status</label>

            <select name="status">

                <option>Planned</option>

                <option>In Progress</option>

                <option>Completed</option>

            </select>

            <label>Created Date</label>

            <input
                type="date"
                name="created_date"
                required
            >

            <button class="button" type="submit">
                💾 Save Project
            </button>

        </form>

    </div>

    """

    html += page_end()

    return html


# =========================================================
# DELETE PROJECT
# =========================================================

@app.route("/project/delete/<int:project_id>")
def delete_project(project_id):

    db = get_db()

    db.execute("""
        DELETE FROM Project
        WHERE project_id = ?
    """, (project_id,))

    db.commit()
    db.close()

    return redirect(url_for("projects_page"))


# =========================================================
# DATASETS
# =========================================================

@app.route("/datasets")
def datasets_page():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            Dataset.dataset_id,
            Dataset.dataset_name,
            Dataset.source,
            Dataset.dataset_type,
            Project.project_name
        FROM Dataset
        LEFT JOIN Project
        ON Dataset.project_id = Project.project_id
        ORDER BY Dataset.dataset_id DESC
    """)

    datasets = cursor.fetchall()

    db.close()

    html = page_start("Datasets")

    html += """

    <div class="container">

        <h1>💾 Datasets</h1>

        <p>
            <a class="button green" href="/dataset/add">
                ➕ Add Dataset
            </a>
        </p>

        <div class="cards">

    """

    for dataset in datasets:

        dataset_id = dataset[0]
        name = escape(str(dataset[1]))
        source = escape(str(dataset[2] or ""))
        dtype = escape(str(dataset[3] or ""))
        project = escape(
            str(dataset[4] or "Not Assigned")
        )

        html += f"""

            <div class="card">

                <h2>
                    📊 {name}
                </h2>

                <p>
                    <b>Source:</b> {source}
                </p>

                <p>
                    <b>Type:</b> {dtype}
                </p>

                <p>
                    <b>Project:</b> {project}
                </p>

                <a
                    class="button delete"
                    href="/dataset/delete/{dataset_id}"
                    onclick="return confirm('Delete this dataset?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """

        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# ADD DATASET
# =========================================================

@app.route("/dataset/add", methods=["GET", "POST"])
def add_dataset():

    db = get_db()

    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["dataset_name"]
        source = request.form["source"]
        dtype = request.form["dataset_type"]
        project_id = request.form["project_id"]

        cursor.execute("""
            INSERT INTO Dataset
            (
                dataset_name,
                source,
                dataset_type,
                project_id
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            source,
            dtype,
            project_id
        ))

        db.commit()
        db.close()

        return redirect(url_for("datasets_page"))


    cursor.execute("""
        SELECT project_id, project_name
        FROM Project
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    db.close()


    options = ""

    for project in projects:

        options += f"""
        <option value="{project[0]}">
            {escape(str(project[1]))}
        </option>
        """


    html = page_start("Add Dataset")

    html += f"""

    <div class="form-box">

        <h1>➕ Add Dataset</h1>

        <form method="POST">

            <label>Dataset Name</label>

            <input
                type="text"
                name="dataset_name"
                placeholder="Example: Student Dataset"
                required
            >

            <label>Source</label>

            <input
                type="text"
                name="source"
                placeholder="Example: Kaggle"
                required
            >

            <label>Dataset Type</label>

            <input
                type="text"
                name="dataset_type"
                placeholder="Example: CSV"
                required
            >

            <label>Related Project</label>

            <select
                name="project_id"
                required
            >

                <option value="">
                    Select Project
                </option>

                {options}

            </select>

            <button class="button green" type="submit">
                💾 Save Dataset
            </button>

        </form>

    </div>

    """

    html += page_end()

    return html


# =========================================================
# DELETE DATASET
# =========================================================

@app.route("/dataset/delete/<int:dataset_id>")
def delete_dataset(dataset_id):

    db = get_db()

    db.execute("""
        DELETE FROM Dataset
        WHERE dataset_id = ?
    """, (dataset_id,))

    db.commit()
    db.close()

    return redirect(url_for("datasets_page"))


# =========================================================
# AI MODELS
# =========================================================

@app.route("/models")
def models_page():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            AI_Model.model_id,
            AI_Model.model_name,
            AI_Model.model_type,
            AI_Model.accuracy,
            Project.project_name
        FROM AI_Model
        LEFT JOIN Project
        ON AI_Model.project_id = Project.project_id
        ORDER BY AI_Model.model_id DESC
    """)

    models = cursor.fetchall()

    db.close()

    html = page_start("AI Models")

    html += """

    <div class="container">

        <h1>🤖 AI Models</h1>

        <p>
            <a class="button orange" href="/model/add">
                ➕ Add AI Model
            </a>
        </p>

        <div class="cards">

    """

    for model in models:

        model_id = model[0]
        name = escape(str(model[1]))
        mtype = escape(str(model[2] or ""))
        accuracy = model[3]
        project = escape(
            str(model[4] or "Not Assigned")
        )

        html += f"""

            <div class="card">

                <h2>
                    🤖 {name}
                </h2>

                <p>
                    <b>Model Type:</b>
                    {mtype}
                </p>

                <p>
                    <b>Accuracy:</b>
                    {accuracy if accuracy is not None else "Not provided"}
                </p>

                <p>
                    <b>Project:</b>
                    {project}
                </p>

                <a
                    class="button delete"
                    href="/model/delete/{model_id}"
                    onclick="return confirm('Delete this model?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """

        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# ADD AI MODEL
# =========================================================

@app.route("/model/add", methods=["GET", "POST"])
def add_model():

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["model_name"]
        mtype = request.form["model_type"]
        accuracy = request.form["accuracy"]
        project_id = request.form["project_id"]

        if accuracy == "":
            accuracy = None

        cursor.execute("""
            INSERT INTO AI_Model
            (
                model_name,
                model_type,
                accuracy,
                project_id
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            mtype,
            accuracy,
            project_id
        ))

        db.commit()
        db.close()

        return redirect(url_for("models_page"))


    cursor.execute("""
        SELECT project_id, project_name
        FROM Project
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    db.close()


    options = ""

    for project in projects:

        options += f"""
        <option value="{project[0]}">
            {escape(str(project[1]))}
        </option>
        """


    html = page_start("Add AI Model")

    html += f"""

    <div class="form-box">

        <h1>➕ Add AI Model</h1>

        <form method="POST">

            <label>Model Name</label>

            <input
                type="text"
                name="model_name"
                placeholder="Example: Random Forest"
                required
            >

            <label>Model Type</label>

            <input
                type="text"
                name="model_type"
                placeholder="Example: Classification"
                required
            >

            <label>Accuracy</label>

            <input
                type="number"
                step="0.01"
                name="accuracy"
                placeholder="Example: 92.5"
            >

            <label>Related Project</label>

            <select
                name="project_id"
                required
            >

                <option value="">
                    Select Project
                </option>

                {options}

            </select>

            <button class="button orange" type="submit">
                💾 Save AI Model
            </button>

        </form>

    </div>

    """

    html += page_end()

    return html


# =========================================================
# DELETE AI MODEL
# =========================================================

@app.route("/model/delete/<int:model_id>")
def delete_model(model_id):

    db = get_db()

    db.execute("""
        DELETE FROM AI_Model
        WHERE model_id = ?
    """, (model_id,))

    db.commit()
    db.close()

    return redirect(url_for("models_page"))


# =========================================================
# MEMBERS
# =========================================================

@app.route("/members")
def members_page():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            member_id,
            member_name,
            role,
            email
        FROM Member
        ORDER BY member_id DESC
    """)

    members = cursor.fetchall()

    db.close()

    html = page_start("Members")

    html += """

    <div class="container">

        <h1>👥 Team Members</h1>

        <p>
            <a class="button" href="/member/add">
                ➕ Add Member
            </a>
        </p>

        <div class="cards">

    """

    for member in members:

        member_id = member[0]

        name = escape(str(member[1]))

        role = escape(str(member[2] or ""))

        email = escape(str(member[3] or ""))


        html += f"""

            <div class="card">

                <h2>
                    👤 {name}
                </h2>

                <p>
                    <b>Role:</b>
                    {role}
                </p>

                <p>
                    <b>Email:</b>
                    {email}
                </p>

                <a
                    class="button delete"
                    href="/member/delete/{member_id}"
                    onclick="return confirm('Delete this member?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """

        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# ADD MEMBER
# =========================================================

@app.route("/member/add", methods=["GET", "POST"])
def add_member():

    if request.method == "POST":

        name = request.form["member_name"]

        role = request.form["role"]

        email = request.form["email"]


        db = get_db()

        db.execute("""
            INSERT INTO Member
            (
                member_name,
                role,
                email
            )
            VALUES (?, ?, ?)
        """, (
            name,
            role,
            email
        ))

        db.commit()
        db.close()

        return redirect(url_for("members_page"))


    html = page_start("Add Member")

    html += """

    <div class="form-box">

        <h1>➕ Add Team Member</h1>

        <form method="POST">

            <label>Name</label>

            <input
                type="text"
                name="member_name"
                placeholder="Example: Subashree"
                required
            >

            <label>Role</label>

            <input
                type="text"
                name="role"
                placeholder="Example: Developer"
                required
            >

            <label>Email</label>

            <input
                type="email"
                name="email"
                placeholder="Example: student@email.com"
                required
            >

            <button class="button" type="submit">
                💾 Save Member
            </button>

        </form>

    </div>

    """

    html += page_end()

    return html


# =========================================================
# DELETE MEMBER
# =========================================================

@app.route("/member/delete/<int:member_id>")
def delete_member(member_id):

    db = get_db()

    db.execute("""
        DELETE FROM Member
        WHERE member_id = ?
    """, (member_id,))

    db.commit()
    db.close()

    return redirect(url_for("members_page"))


# =========================================================
# REPOSITORIES
# =========================================================

@app.route("/repositories")
def repositories_page():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            Repository.repository_id,
            Repository.repository_name,
            Repository.repository_url,
            Repository.platform,
            Project.project_name
        FROM Repository
        LEFT JOIN Project
        ON Repository.project_id = Project.project_id
        ORDER BY Repository.repository_id DESC
    """)

    repositories = cursor.fetchall()

    db.close()

    html = page_start("Repositories")

    html += """

    <div class="container">

        <h1>🔗 Repositories</h1>

        <p>
            <a class="button" href="/repository/add">
                ➕ Add Repository
            </a>
        </p>

        <div class="cards">

    """

    for repo in repositories:

        repo_id = repo[0]

        name = escape(str(repo[1]))

        url = escape(str(repo[2] or ""))

        platform = escape(str(repo[3] or ""))

        project = escape(
            str(repo[4] or "Not Assigned")
        )


        html += f"""

            <div class="card">

                <h2>
                    🔗 {name}
                </h2>

                <p>
                    <b>Platform:</b>
                    {platform}
                </p>

                <p>
                    <b>Project:</b>
                    {project}
                </p>

                <p>
                    <b>URL:</b>
                    {url}
                </p>

                <a
                    class="button delete"
                    href="/repository/delete/{repo_id}"
                    onclick="return confirm('Delete this repository?');"
                >
                    🗑️ Delete
                </a>

            </div>

        """

    html += """

        </div>

    </div>
    """

    html += page_end()

    return html


# =========================================================
# ADD REPOSITORY
# =========================================================

@app.route("/repository/add", methods=["GET", "POST"])
def add_repository():

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["repository_name"]

        url = request.form["repository_url"]

        platform = request.form["platform"]

        project_id = request.form["project_id"]


        cursor.execute("""
            INSERT INTO Repository
            (
                repository_name,
                repository_url,
                platform,
                project_id
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            url,
            platform,
            project_id
        ))


        db.commit()
        db.close()

        return redirect(url_for("repositories_page"))


    cursor.execute("""
        SELECT project_id, project_name
        FROM Project
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    db.close()


    options = ""

    for project in projects:

        options += f"""
        <option value="{project[0]}">
            {escape(str(project[1]))}
        </option>
        """


    html = page_start("Add Repository")

    html += f"""

    <div class="form-box">

        <h1>➕ Add Repository</h1>

        <form method="POST">

            <label>Repository Name</label>

            <input
                type="text"
                name="repository_name"
                placeholder="Example: AI Treasure Hunt"
                required
            >

            <label>Repository URL</label>

            <input
                type="text"
                name="repository_url"
                placeholder="Example: GitHub repository URL"
                required
            >

            <label>Platform</label>

            <select name="platform">

                <option>GitHub</option>

                <option>GitLab</option>

                <option>Bitbucket</option>

                <option>Other</option>

            </select>

            <label>Related Project</label>

            <select
                name="project_id"
                required
            >

                <option value="">
                    Select Project
                </option>

                {options}

            </select>

            <button class="button" type="submit">
                💾 Save Repository
            </button>

        </form>

    </div>

    """

    html += page_end()

    return html


# =========================================================
# DELETE REPOSITORY
# =========================================================

@app.route("/repository/delete/<int:repo_id>")
def delete_repository(repo_id):

    db = get_db()

    db.execute("""
        DELETE FROM Repository
        WHERE repository_id = ?
    """, (repo_id,))

    db.commit()
    db.close()

    return redirect(url_for("repositories_page"))


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    create_database()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )