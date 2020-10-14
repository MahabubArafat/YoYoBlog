from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField("Username :", validators=[DataRequired()])
    about_me = TextAreaField(
        "About Me :", validators=[DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField("Update")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(
            *args, **kwargs
        )  # eida die ekta class construct kre nilam original je username ta db te ache oi ta die, toh eita korar karon hoilo jodi keu username same raikha form ta submit kore then db te kintu username ta already exit korbe, mane amra direct age je unique korar jonno query chalaisi orom query chalate parbo na, ejonoo bedar username bortoman jeita ache oita re dhorte hobe, eita die oi current username rei dhorsi
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            # eikhane check korsi current username er sathe form submit er je username seitar difference ache kina, jodi na thake then eita skip, validate er dorkar nai, jodi submit er username er ssathe original jejita upore dhorsi oita na mile then nicher ei validation error run korbe and submitted username unique kina dekhmu
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username Taken, Please Use Another Username")


class PostForm(FlaskForm):
    post = TextAreaField(
        "What's on your mind?", validators=[DataRequired(), Length(min=1, max=300)]
    )
    submit = SubmitField("Shout")

