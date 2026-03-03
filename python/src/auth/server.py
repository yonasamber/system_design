import jwt
import datetime
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# Config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))


def createJWT(username, secret, authz=False):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "admin": authz,
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@server.route("/", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return "Missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401

        token = createJWT(auth.username, os.environ.get("JWT_SECRET"), authz=False)
        return jsonify({"token": token})

    return "Invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers.get("Authorization")
    if not encoded_jwt:
        return "Missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return "Token expired", 403
    except jwt.InvalidTokenError:
        return "Not authorized", 403

    return jsonify(decoded), 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)