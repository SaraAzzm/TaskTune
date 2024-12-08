from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required, deadline, date_comparison, calculate_percentages, get_eps_level, get_completion_value, get_correlation_indicator

# Configure application
app = Flask(__name__)

# Custom filters
app.jinja_env.filters["deadline"] = deadline
app.jinja_env.filters["date_comparison"] = date_comparison

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasktune.db")

# Emotions and their corresponding values
emotions = {
    "Indifferent": 0,
    "I’m okay with it.": 1,
    "Excited": 1,
    "Not thrilled about it": -1,
    "Stressed": -1,
    "Anxious": -1
}


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Display tasks"""

    # Get overdue tasks if any, to display first and the rest of the tesks after
    message = "You have no tasks at the moment."
    tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND (datetime('now', '+3 hours') < deadline OR deadline IS NULL)", session["user_id"])
    overdue_tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') > deadline", session["user_id"])

    # Update the overdue status for overdue tasks
    for overdue_task in overdue_tasks:
        db.execute("UPDATE tasks SET overdue = 1 WHERE task_id = ?", overdue_task["task_id"])

    return render_template("index.html", overdue_tasks=overdue_tasks, tasks=tasks, message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        if not username or not username.strip():
            apology = "Missing username."
            return render_template("login.html", apology=apology)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apology = "Missing password."
            return render_template("login.html", apology=apology)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            apology = "Invalid username and/or password."
            return render_template("login.html", apology=apology)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Verify username
        if not username or not username.strip():
            apology = "Missing username."
            return render_template("signup.html", apology=apology)

        # Verify password
        if not password:
            apology = "Missing password."
            return render_template("signup.html", apology=apology)

        # Check if the passowrd entered and its confirmation are similar
        if password != confirmation:
            apology = "Passwords don't match."
            return render_template("signup.html", apology=apology)

        # Ensure username is unique
        try:
            key = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        except ValueError:
            apology = "Username taken."
            return render_template("signup.html", apology=apology)

        session["user_id"] = key

        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a task"""

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        emotion = request.form.get("emotion")
        date = request.form.get("date")
        time = request.form.get("time")

        # Check for any missing field
        if not title or not title.strip():
            apology = "Missing title."
            return render_template("add.html", apology=apology, emotions=emotions)

        if not description or not description.strip():
            apology = "Missing description."
            return render_template("add.html", apology=apology, emotions=emotions)

        if not emotion:
            apology = "Missing emotion."
            return render_template("add.html", apology=apology, emotions=emotions)

        # If a deadline (date) is provided, time must also be provided and vice versa
        if date and not time:
            apology = "Missing time."
            return render_template("add.html", apology=apology, emotions=emotions)

        if time and not date:
            apology = "Missing date."
            return render_template("add.html", apology=apology, emotions=emotions)

        # Record task if it has a valid deadline
        if date and time:
            # fix the formatting of the deadline to insert into the db
            deadline_str = f"{date} {time}:00"

            # Let deadline be read as a date to compare it to datetime.now()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")

            # Check for invalid dates
            if deadline < datetime.now():
                apology = "Invalid date."
                return render_template("add.html", apology=apology, emotions=emotions)

            overdue = 0
            db.execute("INSERT INTO tasks (user_id, title, description, deadline, overdue, emotion) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], title.title(), description, deadline, overdue, emotions[emotion])
            return redirect("/")

        # Record task if it has no deadline 
        db.execute("INSERT INTO tasks (user_id, title, description, emotion) VALUES (?, ?, ?, ?)", session["user_id"], title.title(), description, emotions[emotion])
        return redirect("/")
    else:
        return render_template("add.html", emotions=emotions)


@app.route("/search", methods=["POST"])
@login_required
def search():
    """Search for a task"""

    q = request.form.get("q")

    # Empty search
    if not q or not q.strip():
        return redirect("/")

    q.title()
    overdue_tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') > deadline AND title LIKE ?", session["user_id"], ('%' + q + '%'))
    tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND (datetime('now', '+3 hours') < deadline OR deadline IS NULL) AND title LIKE ?", session["user_id"], ('%' + q + '%'))

    # No results found
    if not overdue_tasks and not tasks:
        message = "No tasks found with that title."
        return render_template("index.html", message=message)

    return render_template("index.html", overdue_tasks=overdue_tasks, tasks=tasks)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete a task"""

    task = request.form.get("delete")
    db.execute("DELETE FROM tasks WHERE task_id = ?", task)
    return redirect("/")


@app.route("/complete", methods=["POST"])
@login_required
def complete():
    """Complete a task"""

    # Update complete status
    task = request.form.get("complete")
    db.execute("UPDATE tasks SET is_completed = 1, completed_at = datetime('now', '+3 hours') WHERE task_id = ?", task)

    return redirect("/")


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    """Edit a task"""

    task_id = request.form.get("task_id")
    title = request.form.get("title")
    description = request.form.get("description")
    due_date = request.form.get("deadline")

    # If a deadline is provided update values accordingly 
    if due_date:
        deadline = due_date.replace('T', ' ') + ":00"
        db.execute("UPDATE tasks SET title = ?, description = ?, deadline = ?, overdue = 0 WHERE task_id = ?", title, description, deadline, task_id)
        return redirect("/")

    # If no deadline is present, check if the task previously had a deadline
    task_details = db.execute("SELECT deadline FROM tasks WHERE task_id = ?", task_id)

    # If the task also did not previously have a deadline, update title and description fields only
    if not task_details[0]["deadline"]:
        db.execute("UPDATE tasks SET title = ?, description = ? WHERE task_id = ?", title, description, task_id)
        return redirect("/")

    # If the task previously had a deadline but now updated without it, set deadline and overdue to NULL
    db.execute("UPDATE tasks SET title = ?, description = ?, deadline = NULL, overdue = NULL WHERE task_id = ?", title, description, task_id)
    return redirect("/")


@app.route("/statistics")
@login_required
def statistics():
    """Display statistics"""

    # List of queries
    queries = [
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 1",
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 1 AND overdue = 0",
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 1 AND overdue = 1",
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL",
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NULL",
        "SELECT COUNT(*) AS value FROM tasks WHERE user_id = ? AND is_completed = 0 AND overdue = 1",
    ]

    # List of statistics
    statistic_list = [
        "Total Tasks Completed",
        "Tasks Completed On Time",
        "Tasks Completed Past Due",
        "Current Tasks with Deadlines",
        "Current Tasks without Deadlines",
        "Current Overdue Tasks",
    ]

    # EPS indicator statements
    EPS_indicators = [
        "You’re experiencing mostly positive emotions during your tasks.",
        "Your emotions are balanced as you work.",
        "You’re experiencing mostly negative emotions during your tasks."
    ]

    # EPS indicator statements
    correlation_indicators = [
        "You’re in a positive emotional state, with strong or solid task completion. Keep up the great work!",
        "You’re feeling positive, but task completion is low. Channel that positive energy into accomplishing more tasks!",
        "Your emotions are balanced, and your task completion is effective. A stable and productive approach!",
        "Your emotions are steady, but task completion is low. Try to boost your task output to match your balanced state.",
        "You’re completing tasks effectively despite negative emotions, which may lead to burnout. Consider ways to address your feelings to maintain your well-being.",
        "Low task completion and negative emotions suggest a need for a change. Consider revising your approach to improve both your emotional state and productivity."
    ]

    # Totals needed for percentages
    total = db.execute("SELECT COUNT(*) AS total FROM tasks WHERE user_id = ?", session["user_id"])
    due_total = db.execute("SELECT COUNT(*) AS due_total FROM tasks WHERE user_id = ? AND is_completed = 1 AND deadline IS NOT NULL", session["user_id"])
    current_total = db.execute("SELECT COUNT(*) AS current_total FROM tasks WHERE user_id = ? AND is_completed = 0", session["user_id"])

    # Check for new users
    if total[0]["total"] == 0:
        return render_template("statistics.html", statistic_list=statistic_list)

    # Execute all queries and fill the values in statistics
    statistics = [db.execute(query, session["user_id"])[0] for query in queries]

    # First value only to be divides by total
    statistics[0]["percentage"] = round((statistics[0]["value"] / total[0]["total"]) * 100, 1)
    statistics[0]["statistic"] = statistic_list[0]

    # Calculate the percentages
    calculate_percentages(due_total[0]["due_total"], 1, 3, statistics, statistic_list)
    calculate_percentages(current_total[0]["current_total"], 3, 6, statistics, statistic_list)

    # EPS and task completion stats
    eps_table = {}

    # Get the sum of emotion values for all completed tasks
    emotions_sum = db.execute("SELECT SUM(emotion) as sum FROM tasks WHERE user_id = ? AND is_completed = 1", session["user_id"])

    # Check if the user doesn't have any completed tasks
    if not emotions_sum[0]["sum"] and not statistics[0]["value"]:
        return render_template("statistics.html", statistics=statistics)

    # Compute EPS 
    eps_table["eps"] = round(emotions_sum[0]["sum"] / statistics[0]["value"], 1)

    # Get EPS value (High, Low, Medium) and EPS indicator
    eps_table["eps_value"], eps_table["indicator1"] = get_eps_level(eps_table["eps"], EPS_indicators)

    # Get task completion value (High, Low, Medium)
    eps_table["completion_value"] = get_completion_value(statistics[0]["percentage"])

    # Get EPS and task completion percentage correlation indicator
    eps_table["indicator2"] = get_correlation_indicator(eps_table["eps_value"], eps_table["completion_value"], correlation_indicators)

    return render_template("statistics.html", statistics=statistics, eps_table=eps_table)


@app.route("/filter", methods=["POST"])
@login_required
def filter():
    """Filter tasks"""

    option = request.form.get("filter")

    # All tasks
    if option == "option0":
        return redirect("/")

    # Tasks due today
    if option == "option1":
        overdue_tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') > deadline AND DATE(deadline) = DATE('now')", session["user_id"])
        tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') < deadline AND DATE(deadline) = DATE('now')", session["user_id"])

        # If no tasks due today, return a message to display
        if not overdue_tasks and not tasks:
            message="You don't have any tasks due today."
            return render_template("index.html", message=message)
        return render_template("index.html", overdue_tasks=overdue_tasks, tasks=tasks)

    # Tasks with a deadline
    if option == "option2":
        overdue_tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') > deadline", session["user_id"])
        tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NOT NULL AND datetime('now', '+3 hours') < deadline", session["user_id"])

        # If no tasks with a deadline, return a message to display
        if not overdue_tasks and not tasks:
            message="You have no tasks with a deadline."
            return render_template("index.html", message=message)
        return render_template("index.html", overdue_tasks=overdue_tasks, tasks=tasks)

    # Tasks without a deadline
    if option == "option3":
        tasks = db.execute("SELECT task_id, title, description, deadline FROM tasks WHERE user_id = ? AND is_completed = 0 AND deadline IS NULL", session["user_id"])

        # If no tasks without a deadline, return a message to display
        if not tasks:
            message="You have no tasks without a deadline."
            return render_template("index.html", message=message)
        return render_template("index.html", tasks=tasks)

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Display all completed tasks"""
    
    completed_tasks = db.execute("SELECT title, description, deadline, completed_at FROM tasks WHERE user_id = ? AND is_completed = 1 ORDER BY completed_at DESC", session["user_id"])
    if completed_tasks:
        return render_template("history.html", completed_tasks=completed_tasks)

    return render_template("history.html")





