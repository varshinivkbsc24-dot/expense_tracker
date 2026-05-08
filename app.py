import csv
import os
from flask import Flask, redirect, request, render_template

app = Flask(__name__)
FILE_NAME = "expenses.csv"


# ✅ HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# ✅ ADD EXPENSE (FIXED: GET + POST)
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

    # 👉 when clicking "Add Expense"
    return render_template("index.html")


# ✅ EDIT (FIXED: no 405 error)
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

    # 👉 prevents 405 error when clicking link
    return redirect("/")


# ✅ INSIGHTS
@app.route("/insights")
def insights():
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

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    return render_template(
        "insights.html",
        total=total,
        count=len(expenses),
        highest=highest_category,
        message=message,
        categories=categories,
        amounts=amounts
    )


# ✅ DELETE
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


# ✅ RUN
if __name__ == "__main__":
    app.run(debug=True)