from flask import Flask, render_template, request, redirect, url_for, Response
from scraper import find_leads
from database import init_db, save_leads, get_leads

app = Flask(__name__)

# Create the database/table when the app starts.
init_db()


@app.route("/")
def home():
    leads = get_leads()
    return render_template("index.html", leads=leads)


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"].strip()
    location = request.form["location"].strip()

    if not keyword or not location:
        return redirect(url_for("home"))

    leads = find_leads(keyword, location)
    save_leads(leads)

    return render_template(
        "index.html",
        leads=get_leads(),
        searched=True,
        keyword=keyword,
        location=location,
        found=len(leads),
    )


@app.route("/export")
def export():
    leads = get_leads()

    lines = ["name,website,email,phone,source"]

    for lead in leads:
        row = [
            lead["name"],
            lead["website"],
            lead["email"],
            lead["phone"],
            lead["source"],
        ]

        # Simple CSV escaping.
        row = ['"' + str(value).replace('"', '""') + '"' for value in row]
        lines.append(",".join(row))

    csv_data = "\n".join(lines)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=leads.csv"
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
