import csv
import os
from flask import Flask, redirect, request, render_template

app = Flask(__name__)
FILE_NAME = "expenses.csv"

@app.route("/add", methods=["POST"])
def add():
    category = request.form.get("category", "")
    amount = request.form.get("amount", "")
    date = request.form.get("date", "")
    note = request.form.get("note", "")

    if not amount.isdigit():
        return "Invalid amount"

    rows = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as f:
            rows = list(csv.reader(f))

    id = len(rows) if rows else 1

    if not rows:
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category", "amount", "date", "note"])
            writer.writerow([id, category, amount, date, note])
    else:
        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([id, category, amount, date, note])

    return redirect("/")

@app.route("/edit/<id>", methods=["POST"])
def edit(id):
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    note = request.form["note"]

    with open(FILE_NAME, "r", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return redirect("/")

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] == str(id):
            new_rows.append([id, category, amount, date, note])
        else:
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/")

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expense Tracker</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: #333;
            }
            .container {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                padding: 50px;
                max-width: 700px;
                text-align: center;
                backdrop-filter: blur(5px);
            }
            h1 {
                color: #ff6b6b;
                margin-bottom: 40px;
                font-size: 3em;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .description {
                font-size: 1.2em;
                margin-bottom: 30px;
                color: #666;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .feature {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .feature:hover {
                transform: translateY(-5px);
            }
            .feature h3 {
                margin: 0 0 10px 0;
                color: #ff6b6b;
            }
            .feature p {
                margin: 0;
                color: #666;
            }
            .links {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }
            .link {
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                font-weight: bold;
                font-size: 1.1em;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .link:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }
            .footer {
                margin-top: 40px;
                color: #999;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💸 Expense Tracker</h1>
            <p class="description">Manage your expenses efficiently with our intuitive tracker.</p>
            <div class="features">
                <div class="feature">
                    <h3>📊 Insights</h3>
                    <p>View detailed analytics of your spending habits.</p>
                </div>
                <div class="feature">
                    <h3>➕ Add Expenses</h3>
                    <p>Easily add new expenses with categories and notes.</p>
                </div>
                <div class="feature">
                    <h3>✏️ Edit</h3>
                    <p>Edit existing expenses to keep records accurate.</p>
                </div>
                <div class="feature">
                    <h3>🗑️ Delete</h3>
                    <p>Remove expenses you no longer need.</p>
                </div>
            </div>
            <div class="links">
                <a href="/insights" class="link">View Insights</a>
                <a href="/add" class="link">Add Expense</a>
                <a href="/edit/1" class="link">Edit Expense</a>
            </div>
            <p class="footer">Use the API endpoints for programmatic access.</p>
        </div>
    </body>
    </html>
    """

@app.route("/insights")
def insights():
    
    categories = ["Food", "Travel", "Shopping"]
    amounts = [500, 300, 200]

    try:
        with open(FILE_NAME, 'r') as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        rows = []

    expenses = rows[1:] if rows else []

    total = 0
    category_totals = {}

    for row in expenses:
        category = row[1]
        amount = int(row[2])
        total += amount
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += amount

    highest_category = max(category_totals, key=category_totals.get) if category_totals else "N/A"

    if total < 2000:
        message = "Excellent spending habits 🌟"
    elif total < 5000:
        message = "Good budgeting 👍"
    else:
        message = "High spending detected 💸"

    # Prepare data for charts
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    return render_template(
    "insights.html",
    categories=categories,
    amounts=amounts,
    total=total,
    count=count,
    highest=highest,
    message=message
   )

@app.route("/delete/<id>")
def delete(id):
    with open(FILE_NAME, "r", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return redirect("/")

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] != str(id):
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/insights")

if __name__ == "__main__":
    app.run(debug=True)
