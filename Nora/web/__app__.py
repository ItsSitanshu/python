import json
import os

import asyncpg
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import *

app = Flask("__main__")

load_dotenv()
PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
async def create_db_pool():
    app.db = await asyncpg.create_pool(database="Nora", user="postgres", password=PSQL_PASSWORD)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/invite/')
def invite():
    return render_template("invite.html")

@app.route(f'/en/docs/')
def docs_main_en():
    return render_template(f"./docs/en/main_docs.html")

@app.route(f'/jp/docs/')
def docs_main_jp():
    return render_template(f"./docs/jp/main_docs.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template(f"./errors/404.html")

if __name__ == "__main__":
    app.run(debug=True)