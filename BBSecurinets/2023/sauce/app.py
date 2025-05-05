from flask import Flask, request, render_template

app = Flask(__name__)

flag = "Securinets{4lg0r1thm5_4nd_l0g1c_4r3_3qu4lly_imp0rT4nt}"  

@app.route('/source')
def source():
    with open('source.txt', 'r') as file:
        contents = file.read()
    return contents

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        if 'p' in request.json:
            p = request.json['p']
            if isinstance(p, list) and all(isinstance(x, int) for x in p) and len(p) == 6:
                y = 1
                for x in p:
                    y *= x
                if y == 1337:
                    return flag
    return "Invalid request"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
