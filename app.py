import csv
import os
from flask import Flask, redirect, request, render_template

app = Flask(__name__)
FILE_NAME = "expenses.csv"


# ✅ HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# ✅ ADD EXPENSE (GET + POST FIXED)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
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

        id = len(rows)

        # create file with header if not exists
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

    # 👇 THIS FIXES YOUR ERROR
    return render_template("index.html")


# ✅ INSIGHTS PAGE (FULLY FIXED)
@app.route("/insights")
def insights():
    try:
        with open(FILE_NAME, "r") as f:
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

    # ✅ FIXED VARIABLES
    count = len(expenses)
    highest = max(category_totals, key=category_totals.get) if category_totals else "N/A"

    # messages
    if total < 2000:
        message = "Excellent spending habits 🌟"
    elif total < 5000:
        message = "Good budgeting 👍"
    else:
        message = "High spending detected 💸"

    # chart data
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


# ✅ DELETE EXPENSE
@app.route("/delete/<id>")
def delete(id):
    if not os.path.exists(FILE_NAME):
        return redirect("/")

    with open(FILE_NAME, "r", newline="") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] != str(id):
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/insights")


# ✅ EDIT (basic working version)
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]
        note = request.form["note"]

        with open(FILE_NAME, "r", newline="") as f:
            rows = list(csv.reader(f))

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

    return render_template("index.html")  # simple fallback


if __name__ == "__main__":
    app.run(debug=True)