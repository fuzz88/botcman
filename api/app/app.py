from fastapi import FastAPI

import logging

import db
import auth
import routes

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    app = FastAPI()

    db.init(app)
    auth.init(app)
    routes.init(app)

    return app


if __name__ == "__main__":
    main()
