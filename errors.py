from flask import Flask, render_template
from app import app, db


app = Flask (__name__)

@app.route("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404
    


@app.errorhandler(500)
def page_not_found(e):
    db.session.rollback()
    return render_template('error505.html'), 500
        