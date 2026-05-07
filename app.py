from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
FILE_NAME = "expenses.csv"

# Create CSV if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Category", "Amount", "Date", "Note"])

# Home page
@app.route("/")
def index():
    expenses = []
    total = 0

    with open(FILE_NAME, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
            total += float(row["Amount"])

    return render_template("index.html", expenses=expenses, total=total)

# Add expense
@app.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    note = request.form["note"]

    with open(FILE_NAME, 'r') as f:
        rows = list(csv.reader(f))
        next_id = len(rows)

    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, category, amount, date, note])

    return redirect("/")

# Delete expense
@app.route("/delete/<id>")
def delete(id):
    with open(FILE_NAME, 'r') as f:
        rows = list(csv.reader(f))

    header = rows[0]
    new_rows = [header]

    for row in rows[1:]:
        if row[0] != id:
            new_rows.append(row)

    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)