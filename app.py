from flask import Flask, abort, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import shopping

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route('/identify', methods=["POST"])
@cross_origin()
def identify():
    user_id = request.get_json().get('userId', '')
    print(user_id)
    path = f"data/{user_id}"
    if not os.path.isdir(path):
        abort(404)
    return "OK"

@app.route('/user/<int:user_id>/shop/list', methods=["GET"])
@cross_origin()
def shop_list(user_id):
    path = f"data/{user_id}/shopping.json"
    with open(path, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/user/<int:user_id>/shop/clear', methods=["POST"])
@cross_origin()
def shop_clear(user_id):
    try:
        shopping.clear(user_id)
        return "OK"
    except:
        abort(404)

@app.route('/user/<int:user_id>/shop/<str:item>/delete', methods=["POST"])
@cross_origin()
def shop_clear(user_id, item):
    try:
        shopping.remove(user_id, {item})
        return "OK"
    except:
        abort(404)

@app.route('/user/<int:user_id>/shop/<str:item>/increase/<int:amt>', methods=["POST"])
@cross_origin()
def shop_clear(user_id, item, amt):
    try:
        shopping.add(user_id, {item: amt})
        return "OK"
    except:
        abort(404)

if __name__ == "__main__":
    app.run()