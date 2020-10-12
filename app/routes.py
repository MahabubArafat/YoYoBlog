from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
    g,
    request,
    jsonify,
)
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import app, db, email
from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    PostForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from app.models import User, Post
from app.email import send_password_reset_email
from app.translate import translate


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
# this is how we can add multiple routes or links or paths for an function or page
# and serial of decoratores in flask specially app.routes are very important to be in first in order
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == "UNKNOWN" or len(language) > 5:
            language = ""
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash("You Just Shouted in YoYoBlog")
        return redirect(url_for("index"))

    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    # for pagination of blog posts, tail .all() na die eivabe dite hoise
    # paginate sequence (page number, num of items perpage,will it show an error when page not found?->False disi mane error dibe na,empty page dibe)
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None
    # mane next and previous page number uprer oi posts ja paisi paginate query theke nibe, ar jodi paginate empty list return kore then amra next page value None dilam, jeno jeita nai oita show na kore.
    return render_template(
        "index.html",
        title="Home",
        posts=posts.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url,
    )
    # posts er pore .items lagate hoise karon paginate query items akare dey result, list akare dey na ager moto


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


@app.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    # request.args.get(what is term looking for,default,type of the argument)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    # eivabe query korar reason upore
    next_url = url_for("explore", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("explore", page=posts.prev_num) if posts.has_prev else None
    # print(type(posts.items))--> becomes list
    # print(len(posts.items)) per page item je koyta oitay dey
    # print(posts.next_num, posts.prev_num)
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
            # that .data is important cause without oita form theke ja pabe pura ta dekhabe, just username ta grab korbe na
        login_user(user, remember=form.remember_me.data)
        flash(f"welcome {form.username.data} to your home")
        next_page = request.args.get("next")
        # request.args die amra query string access korte pari, oi je search/address bar e ? er por ja ase oitaai query string, eita ekta dictionary format e ase, so 'next' is like a key to the value of the query string
        # this is for dhoro ekta page e jete dhorlam, login kora dorkar tar jonno, so login korle direct jeno je page e jaite chaisilam oi page e direct kore eita sei kaj kortese
        if not next_page or not next_page.startswith("/"):
            # oi eki kahini,eita better tobe
            # url_parse(next_page).netloc check kortese je , je url ta pass kora hoise oitar domain name empty kina, empty na hoile nicher ta set kore dicche, \
            # ar empty hoile ja ache tai, eita kortese karon kono attacker url er query string e ?er por or website er domain name add kore okhane redirect krte pare, \
            # ei dhoroner attack deflect korar jonno eita kora,mane domain empty paile toh amar site e, karon ami ei folder er relatively url pass kori, \
            # ar domain paile amar site na, remote site, so tokhon next_page eer value niche  set kore dicchi 'index' jeno amar site theke redirect kore or site e nite na pare
            next_page = url_for("index")
            # jodi kono query string na thake tobe index default kore dilam
        return redirect(next_page)
    return render_template(
        "login.html", title="Sign In", form=form, body="rgb(127, 255, 212)"
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Congratulations {form.username.data} , You have Registered Successfully,Now Login to continue"
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user.html", user=user, posts=posts, title=username)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # current_user.username dilam eitay original_username
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes Have been saved")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", form=form, title="edit profile")


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User : {username} not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You Can't Follow Yourself ")
        return redirect(url_for("user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are Folllowing {username}")
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User :{username} not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You Can't Unfollow Yourself ")
        return redirect(url_for("user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You unfollowed  {username}")
    return redirect(url_for("user", username=username))


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check Your Email for further instructions to reset password")
        return redirect(url_for("login"))

    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form, title="Reset password")


@app.route("/translate", methods=["POST"])
@login_required
def trnaslate_text():
    return jsonify(
        {
            "text": translate(
                request.form["text"],
                request.form["source_language"],
                request.form["dest_language"],
            )
        }
    )

