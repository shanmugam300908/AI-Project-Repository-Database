import sqlite3

def connect_database():
    return sqlite3.connect("ai_project_repository.db")


# -----------------------------
# Add Project
# -----------------------------
def add_project():
    connection = connect_database()
    cursor = connection.cursor()

    name = input("Enter project name: ")
    description = input("Enter description: ")
    domain = input("Enter domain: ")
    status = input("Enter status: ")
    date = input("Enter created date (YYYY-MM-DD): ")

    cursor.execute("""
    INSERT INTO Project
    (project_name, description, domain, status, created_date)
    VALUES (?, ?, ?, ?, ?)
    """, (name, description, domain, status, date))

    connection.commit()
    connection.close()

    print("\nProject added successfully!")


# -----------------------------
# View Projects
# -----------------------------
def view_projects():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT project_id, project_name, domain, status, created_date
    FROM Project
    """)

    projects = cursor.fetchall()

    print("\n===== PROJECT LIST =====")

    if not projects:
        print("No projects found.")
    else:
        for project in projects:
            print("\nID:", project[0])
            print("Name:", project[1])
            print("Domain:", project[2])
            print("Status:", project[3])
            print("Created Date:", project[4])

    connection.close()


# -----------------------------
# Search Project
# -----------------------------
def search_project():
    connection = connect_database()
    cursor = connection.cursor()

    keyword = input("Enter project name to search: ")

    cursor.execute("""
    SELECT project_id, project_name, domain, status
    FROM Project
    WHERE project_name LIKE ?
    """, ('%' + keyword + '%',))

    projects = cursor.fetchall()

    print("\n===== SEARCH RESULTS =====")

    if not projects:
        print("No project found.")
    else:
        for project in projects:
            print("\nID:", project[0])
            print("Name:", project[1])
            print("Domain:", project[2])
            print("Status:", project[3])

    connection.close()


# -----------------------------
# Update Project
# -----------------------------
def update_project():
    connection = connect_database()
    cursor = connection.cursor()

    project_id = input("Enter project ID to update: ")

    new_status = input("Enter new status: ")

    cursor.execute("""
    UPDATE Project
    SET status = ?
    WHERE project_id = ?
    """, (new_status, project_id))

    connection.commit()

    if cursor.rowcount > 0:
        print("\nProject updated successfully!")
    else:
        print("\nProject ID not found.")

    connection.close()


# -----------------------------
# Delete Project
# -----------------------------
def delete_project():
    connection = connect_database()
    cursor = connection.cursor()

    project_id = input("Enter project ID to delete: ")

    cursor.execute("""
    DELETE FROM Project
    WHERE project_id = ?
    """, (project_id,))

    connection.commit()

    if cursor.rowcount > 0:
        print("\nProject deleted successfully!")
    else:
        print("\nProject ID not found.")

    connection.close()


# -----------------------------
# Main Menu
# -----------------------------
while True:

    print("\n==============================")
    print("   AI PROJECT REPOSITORY")
    print("==============================")
    print("1. Add Project")
    print("2. View Projects")
    print("3. Search Project")
    print("4. Update Project")
    print("5. Delete Project")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_project()

    elif choice == "2":
        view_projects()

    elif choice == "3":
        search_project()

    elif choice == "4":
        update_project()

    elif choice == "5":
        delete_project()

    elif choice == "6":
        print("Thank you for using AI Project Repository!")
        break

    else:
        print("Invalid choice. Please try again.")