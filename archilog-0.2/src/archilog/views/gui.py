from flask import Blueprint, render_template, request, redirect, url_for
import uuid
import archilog.models as models

web_ui = Blueprint('web_ui', __name__)

@web_ui.route("/")
def index():
    entries = models.get_all_entries()
    return render_template("interface.html", entries=entries)

@web_ui.route("/create", methods=["GET", "POST"])
def create_entry():
    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"])
        category = request.form.get("category", None)
        models.create_entry(name, amount, category)
        return redirect(url_for("web_ui.index"))
    return render_template("create.html")

@web_ui.route("/delete/<uuid:id>")
def delete_entry(id):
    models.delete_entry(id)
    return redirect(url_for("web_ui.index"))

@web_ui.route("/update/<uuid:id>", methods=["GET", "POST"])
def update_entry(id):
    entry = models.get_entry(id)
    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"])
        category = request.form.get("category", None)
        models.update_entry(id, name, amount, category)
        return redirect(url_for("web_ui.index"))
    return render_template("update.html", entry=entry)
