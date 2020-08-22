from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    password = PasswordField("Password : ", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password : ", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password :", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # adding custom validation syntax-> validate_fieldname(self,fieldname):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # when we need to query a field, and we have an attribute but not the unique id(primary key), we don't use get, we use filter_by(attribute=attribute name)
        if user is not None:
            raise ValidationError("Username Taken, Please use another username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "Email is used by another user, Please use a different email"
            )


class EditProfileForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    about_me = TextAreaField(
        "About Me :", validators=[DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField("Update")

