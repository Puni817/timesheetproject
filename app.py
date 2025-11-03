import base64
import io
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import matplotlib
matplotlib.use('Agg')  # Fix backend issue for servers

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["timesheet_db"]
collection = db["records"]

# ------------------ HOME PAGE ------------------


@app.route('/')
def index():
    records = list(collection.find())
    return render_template('index.html', records=records)

# ------------------ ADD NEW RECORD ------------------


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        project = request.form['project']
        hours = float(request.form['hours'])
        date = request.form['date']  # ✅ added date field

        collection.insert_one({
            'name': name,
            'project': project,
            'hours': hours,
            'date': date
        })
        return redirect(url_for('index'))
    return render_template('add.html')


# ------------------ EDIT RECORD ------------------


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    from bson import ObjectId
    record = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        name = request.form['name']
        project = request.form['project']
        hours = float(request.form['hours'])
        date = request.form['date']

        # ✅ Update existing record instead of inserting new one
        collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'name': name, 'project': project, 'hours': hours, 'date': date}}
        )
        return redirect(url_for('index'))

    return render_template('add.html', record=record)


# ------------------ DELETE RECORD ------------------


@app.route('/delete/<id>')
def delete(id):
    from bson import ObjectId
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

# ------------------ DASHBOARD PAGE ------------------


@app.route('/dashboard')
def dashboard():
    try:
        # Fetch data from MongoDB
        data = list(collection.find())

        # If no data is present, return empty lists
        if not data:
            return render_template(
                "dashboard.html",
                names=[],
                hours=[],
                projects=[],
                avg_hours=0,
                total_hours=0
            )

        # Extract fields safely
        names = [d.get("name", "Unknown") for d in data]
        hours = [float(d.get("hours", 0)) for d in data]
        projects = [d.get("project", "N/A") for d in data]

        # Calculate averages
        avg_hours = sum(hours) / len(hours) if hours else 0
        total_hours = sum(hours)

        # Send data to HTML
        return render_template(
            "dashboard.html",
            names=names,
            hours=hours,
            projects=projects,
            avg_hours=round(avg_hours, 2),
            total_hours=round(total_hours, 2)
        )

    except Exception as e:
        print("Dashboard Error:", e)
        return render_template(
            "dashboard.html",
            names=[],
            hours=[],
            projects=[],
            avg_hours=0,
            total_hours=0
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
