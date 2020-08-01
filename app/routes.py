from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
# this is how we can add multiple routes or links or paths for an function or page
def index():
    user = {"username": "jack"}
    return render_template("index.html", title="First", user=user)


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

