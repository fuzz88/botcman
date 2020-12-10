from fastapi import FastAPI

import logging

import db
import auth
import routes

"""
TODO:
    - logging level environment variable
"""

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

db.init(app)
auth.init(app)
routes.init(app)
