from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
    g,
    current_app,
)
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm
from app.models import Notification, User, Post, Message
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("main.index"))

    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )
    next_url = url_for("main.index", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("main.index", page=posts.prev_num) if posts.has_prev else None
    return render_template(
        "index.html",
        title="Home",
        posts=posts.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    # request.args.get(what is term looking for,default,type of the argument)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )
    next_url = url_for("main.explore", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("main.explore", page=posts.prev_num) if posts.has_prev else None
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user.html", user=user, posts=posts, title=username)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes Have been saved")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", form=form, title="edit profile")


@bp.route("/user/<username>/popup")
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user_popup.html", user=user)


@bp.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User : {username} not found")
        return redirect(url_for("main.index"))
    if user == current_user:
        flash("You Can't Follow Yourself ")
        return redirect(url_for("main.user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are Folllowing {username}")
    return redirect(url_for("main.user", username=username))


@bp.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User :{username} not found")
        return redirect(url_for("main.index"))
    if user == current_user:
        flash("You Can't Unfollow Yourself ")
        return redirect(url_for("main.user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You just unfollowed  {username}")
    return redirect(url_for("main.user", username=username))


@bp.route("/translate", methods=["POST"])
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


@bp.route("/search")
@login_required
def search():
    if (
        not g.search_form.validate()
    ):  # why validate not validate on submit, cause validate on submit will imply its post request but actually its a get request, so we had to use only validate
        return redirect(url_for("main.explore"))
    try:
        page = request.args.get("page", 1, type=int)
        posts, total = Post.search(
            g.search_form.q.data, page, current_app.config["POSTS_PER_PAGE"]
        )
        next_url = (
            url_for("main.search", q=g.search_form.q.data, page=page + 1)
            if total["value"] > page * current_app.config["POSTS_PER_PAGE"]
            else None
        )

        prev_url = (
            url_for("main.search", q=g.search_form.q.data, page=page - 1)
            if page > 1
            else None
        )

        return render_template(
            "search.html",
            title="Search",
            posts=posts,
            next_url=next_url,
            prev_url=prev_url,
            total=total,
        )
    except:
        return render_template("not_found.html")


@bp.route("/send_message/<recipient>", methods=["GET", "POST"])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        user.add_notification("unread_message_count", user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash("Sent")
        return redirect(url_for("main.user", username=recipient))
    return render_template(
        "send_message.html", title="Send Message", form=form, recipient=recipient
    )


@bp.route("/messages")
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification("unread_message_count", 0)
    db.session.commit()
    page = request.args.get("page", 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()
    ).paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    next_url = (
        url_for("main.messages", page=messages.next_num) if messages.has_next else None
    )
    prev_url = (
        url_for("main.messages", page=messages.prev_num) if messages.has_prev else None
    )

    return render_template(
        "messages.html",
        messages=messages.items,
        title="Messages",
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/notifications")
@login_required
def notifications():
    since = request.args.get("since", 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since
    ).order_by(Notification.timestamp.asc())

    return jsonify(
        [
            {"name": n.name, "data": n.get_data(), "timestamp": n.timestamp}
            for n in notifications
        ]
    )


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash("Exporting your posts ....")
    else:
        current_user.launch_task('export_posts',"Exporting Posts...")
        db.session.commit()
    return redirect(url_for('main.user',username=current_user.username))