from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    about_me = TextAreaField(
        "About Me :", validators=[DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField("Update")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username Taken, Please Use Another Username")


class PostForm(FlaskForm):
    post = TextAreaField(
        "What's on your mind?", validators=[DataRequired(), Length(min=1, max=300)]
    )
    submit = SubmitField("Shout")


class SearchForm(FlaskForm):
    q = StringField("Search", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "csrf_enabled" not in kwargs:
            kwargs["csrf_enabled"] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=0, max=200)]
    )
    submit = SubmitField("Send")

