from flask import Flask, request
from json import dumps
from typing import Dict
from definitions import ErrorResponse, SuccessResponse, PostColor, GetColor

# python -m flask --app server run

SUCCESS = 200
BAD_REQ = 400
INTERNAL_ERR = 500


app = Flask(__name__)

color_db: Dict[str, str] = {}


def req_err(msg: str):
    res: ErrorResponse = {"code": BAD_REQ, "message": msg}
    return dumps(res)


def server_err():
    res: ErrorResponse = {"code": INTERNAL_ERR, "message": "Internal server error."}
    return dumps(res)


@app.route("/")
def version():
    try:
        res: SuccessResponse = {"code": SUCCESS, "data": {"version": "0.0.1"}}
        return dumps(res)
    except TypeError:
        return server_err()


@app.post("/set_color")
def set_color():
    try:
        req: PostColor = request.json
        user: str = req["user_uuid"]
        color: str = req["color"]
        color_db[user] = color
        res: SuccessResponse = {"code": SUCCESS, "data": None}
        return dumps(res)
    except (KeyError, TypeError):
        example: PostColor = {"user_uuid": "example", "color": "blue"}
        return req_err(
            f"Malformed request. Expected something resembling this: {dumps(example)}"
        )


@app.get("/get_color")
def get_color():
    try:
        user: str = request.args.get("user_uuid")
        if user not in color_db:
            return req_err("The requested user was not found.")
        res: SuccessResponse = {"code": SUCCESS, "data": color_db[user]}
        return dumps(res)

    except KeyError:
        example: GetColor = {"user_uuid": "example"}
        return req_err(
            f"Malformed request. Expected something resembling this: {dumps(example)}"
        )
