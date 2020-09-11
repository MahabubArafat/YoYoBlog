from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found(error):
    # the error object , that is automatically provided by flask to show the exact error messages and codes in the webpage
    return render_template("404.html", title="User Not Found"), 404
    # ar oi je last e 404 disi, eita status of this page,mane jekuno error er jonno ami amar mon moto code dite pari, actually ei error code 404 dekhano uchit server e, kintu jehetu eita ekta webpage return e krtese so eita 404 na dekhaiye, 200 ok dekhabe in the server karon amra error ta handle kortesi, so asol error code ta pacchi na , so amra error code manually set kore nilam, ami chaile 420 ba jekuno error dekhiate parbo amar mon moto and seita define o korte parbo, jeuno error set korte parbo,onk developer ra nijer mon moto error set kore, for security purpose, 404, 200 egula just standard


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # ei session er data er jonnoi toh error asche, so ei session er data remove korlam, rollback hoilo db,commit er opposite
    return render_template("500.html", title="Internal Error"), 500

