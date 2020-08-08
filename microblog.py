from app import app, db
from app.models import Post, User


@app.shell_context_processor
def make_shell_context():
    # so that we dont need to import app or db or User or Post classes everytime we open a flask shell
    return {"db": db, "User": User, "Post": Post}


if __name__ == "__main__":
    app.run(debug=True)

