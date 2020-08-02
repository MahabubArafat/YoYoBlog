from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
# this is how we can add multiple routes or links or paths for an function or page
def index():
    user = {"username": "jack"}
    posts = [
        {"author": {"username": "John"}, "body": "Good Morning"},
        {"author": {"username": "Wick"}, "body": "I am gonna kill you"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


# adding onek boro string in return
# return f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#       <meta charset="UTF-8">
#       <meta name="viewport" content="width=device-width, initial-scale=1.0">
#       <title>Document</title>
# </head>
# <body>
#       bal {us} ei je variable disi
# </body>
# </html>
# """

# mane ''' ei 3ta die onek boro string o return kora jay''' jantam e na bal


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f" Log in Complete {form.username.data} and remeber you={form.remember_me.data}"
        )  # that .data is important cause without oita form theke ja pabe pura ta dekhabe, just username ta grab korbe na
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)

