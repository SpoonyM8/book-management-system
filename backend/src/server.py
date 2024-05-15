from flask import Flask, request
from json import dumps
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity
from json import dumps
from werkzeug.exceptions import HTTPException
from .clear import clear
from .users import register, login
from .search import search
from .helper import check_jwt
from .review import add_review, delete_review, get_reviews
from .sharedCollections import create_shared_collection, delete_shared_collection,\
join_shared_collection, leave_shared_collection, add_book_shared_collection,\
remove_book_shared_collection, shared_collection_details, shared_collection,\
shared_collection_username, shared_collection_is_member, shared_collection_all
from .books import details
from .follow import follow, unfollow, followers, following
from .collections import add_book_to_collection, remove_book_from_collection,\
create_collection, get_collections, get_collection_details, delete_collection
from .goals import create_goal, remove_goal, update_goal, get_user_goals
from .recommend import recommend

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "notasecret"
jwt = JWTManager(app)

@app.errorhandler(HTTPException)
def handle_exception(e):
    resp = e.get_response()
    print("\033[93m"+ "Error:", e.description + "\033[0m")
    resp.data = dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    resp.content_type = "application/json"
    return resp

app.config["TRAP_HTTP_EXCEPTIONS"] = True

################################################################################

@app.route("/")
def index_http():
    return "<p>Root!</p>"

@app.route("/clear", methods=["DELETE"])
def clear_http():
    clear()
    return ""

@app.route("/register", methods=["POST"])
def register_http():
    return dumps(register(request.get_json()))

@app.route("/login", methods=["POST"])
def login_http():
    return dumps(login(request.get_json()))

@app.route("/search", methods=["POST"])
@check_jwt()
def search_http():
    return dumps(search(request.get_json()))

@app.route("/books/<bookID>/review/add", methods=["POST"])
@check_jwt()
def add_review_http(bookID):
    return dumps(add_review(get_jwt_identity(), bookID, request.get_json()))

@app.route("/books/<bookID>/review/delete", methods=["DELETE"])
@check_jwt()
def delete_review_http(bookID):
    return dumps(delete_review(get_jwt_identity(), bookID))

@app.route("/books/<bookID>/review/get", methods=["GET"])
@check_jwt()
def get_reviews_http(bookID):
    return dumps(get_reviews(bookID))

@app.route("/collections/user/<username>", methods=["GET"])
@check_jwt()
def get_collections_http(username):
    return dumps(get_collections(username))

@app.route("/collections", methods=["GET"])
@check_jwt()
def get_collections_username_http():
    return dumps(get_collections(get_jwt_identity()))

@app.route("/collections/<collectionID>", methods=["GET"])
@check_jwt()
def get_collection_details_http(collectionID):
    return dumps(get_collection_details(collectionID))

@app.route("/collections/create/<collectionName>", methods=["POST"])
@check_jwt()
def create_collection_http(collectionName):
    return dumps(create_collection(get_jwt_identity(), collectionName)) 

@app.route("/collections/delete/<collectionID>", methods=["DELETE"])
@check_jwt()
def delete_collection_http(collectionID):
    return dumps(delete_collection(get_jwt_identity(), collectionID))

@app.route("/collections/<collectionID>/add/<bookID>", methods=["POST"])
@check_jwt()
def add_book_collection_http(collectionID, bookID):
    return dumps(add_book_to_collection(bookID, collectionID))

@app.route("/collections/<collectionID>/remove/<bookID>", methods=["DELETE"])
@check_jwt()
def remove_book_collection_http(collectionID, bookID):
    return dumps(remove_book_from_collection(bookID, collectionID))

@app.route("/sharedCollection/create/<collectionName>", methods=["POST"])
@check_jwt()
def create_shared_collection_http(collectionName):
    return dumps(create_shared_collection(get_jwt_identity(), collectionName))

@app.route("/sharedCollection/delete/<collectionID>", methods=["DELETE"])
@check_jwt()
def delete_shared_collection_http(collectionID):
    return dumps(delete_shared_collection(get_jwt_identity(), collectionID))

@app.route("/sharedCollection/join/<collectionID>", methods=["POST"])
@check_jwt()
def join_shared_collection_http(collectionID):
    return dumps(join_shared_collection(get_jwt_identity(), collectionID))

@app.route("/sharedCollection/leave/<collectionID>", methods=["DELETE"])
@check_jwt()
def leave_shared_collection_http(collectionID):
    return dumps(leave_shared_collection(get_jwt_identity(), collectionID))

@app.route("/sharedCollection/<collectionID>/add/<bookID>", methods=["POST"])
@check_jwt()
def add_book_shared_collection_http(collectionID, bookID):
    return dumps(add_book_shared_collection(get_jwt_identity(), collectionID, bookID))

@app.route("/sharedCollection/<collectionID>/remove/<bookID>", methods=["DELETE"])
@check_jwt()
def remove_book_shared_collection_http(collectionID, bookID):
    return dumps(remove_book_shared_collection(get_jwt_identity(), collectionID, bookID))

@app.route("/sharedCollection/<collectionID>/details", methods=["GET"])
@check_jwt()
def shared_collection_details_http(collectionID):
    return dumps(shared_collection_details(get_jwt_identity(), collectionID))

@app.route("/sharedCollection", methods=["GET"])
@check_jwt()
def shared_collection_http():
    return dumps(shared_collection(get_jwt_identity()))

@app.route("/sharedCollection/user/<username>", methods=["GET"])
@check_jwt()
def shared_collection_username_http(username):
    return dumps(shared_collection_username(username))

@app.route("/sharedCollection/all", methods=["GET"])
@check_jwt()
def shared_collection_all_http():
    return dumps(shared_collection_all(get_jwt_identity()))

@app.route("/sharedCollection/<collectionID>/is_member/<username>", methods=["GET"])
@check_jwt()
def shared_collection_is_member_http(collectionID, username):
    return dumps(shared_collection_is_member(collectionID, username))

@app.route("/books/<bookID>", methods=["GET"])
@check_jwt()
def get_details_http(bookID):
    return dumps(details(bookID))
    
@app.route("/users/follow/<username>", methods=["POST"])
@check_jwt()
def follow_http(username):
    return dumps(follow(get_jwt_identity(), username))

@app.route("/users/unfollow/<username>", methods=["DELETE"])
@check_jwt()
def unfollow_http(username):
    return dumps(unfollow(get_jwt_identity(), username))

@app.route("/users/followers/<username>", methods=["GET"])
@check_jwt()
def followers_http(username):
    return dumps(followers(username))

@app.route("/users/following/<username>", methods=["GET"])
@check_jwt()
def following_http(username):
    return dumps(following(username))

@app.route("/goals/create", methods=["POST"])
@check_jwt()
def create_goal_http():
    return dumps(create_goal(get_jwt_identity(), request.get_json()))

@app.route("/goals/update/<goalID>", methods=["POST"])
@check_jwt()
def update_goal_http(goalID):
    return dumps(update_goal(goalID, request.get_json()))

@app.route("/goals/remove/<goalID>", methods=["DELETE"])
@check_jwt()
def remove_goal_http(goalID):
    return dumps(remove_goal(goalID))

@app.route("/goals", methods=["GET"])
@check_jwt()
def get_user_goals_http():
    return dumps(get_user_goals(get_jwt_identity()))

@app.route("/recommend/<bookID>", methods=["POST"])
@check_jwt()
def recommend_http(bookID):
    return dumps(recommend(get_jwt_identity(), request.get_json(), bookID))
