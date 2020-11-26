from fastapi import FastAPI

import db
import auth
import routes


app = FastAPI()

db.init(app)
auth.init(app)
routes.init(app)
