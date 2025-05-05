#!/usr/bin/env python3

from flask import Flask, abort, request, render_template_string, render_template
import jinja2, re, hashlib

app = Flask(__name__, template_folder=".")

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/dimensions', methods=['GET'])
def dimension():
    dim = request.args.get("dimension", None) 
    if dim is None:
        return '<center><body style="background:url(\'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/rick-and-morty-season-four-trailer-1585738290.png\');background-size:cover;"><h2 style="color:white;"><i>bughhh, so morty tell me, ugh, what dimension shall we go to??<br>use \"dimension\" as parameter </i></h2></body></center>'
    else:
        template = '''
         <!DOCTYPE html>
         <html>
            <head>
            <title>Dimensions</title>
            </head>
            <body style="background: url('https://c4.wallpaperflare.com/wallpaper/410/59/609/rick-and-morty-tv-rick-sanchez-morty-smith-wallpaper-preview.jpg'); background-size:cover;">
            <center>
            <p style="color:white;">we can't just go from C-107 to "''' + dim + '''" without the flag morty! BUGH!</p>
            <p style="color:yellow; background-color:green;">wuwu </p>
            </center>
            </body>
            </html>'''

        return render_template_string(template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
