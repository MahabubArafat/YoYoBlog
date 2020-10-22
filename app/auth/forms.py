from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    password = PasswordField("Password : ", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password : ", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password :", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username Taken, Please use another username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "Email is used by another user, Please use a different email"
            )


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Enter Your Email:", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password : ", validators=[DataRequired()])
    password2 = PasswordField(
        "Retype Your Password :", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Reset")
