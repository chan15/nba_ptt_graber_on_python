# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from app.graber import Graber
app = Flask(__name__)

@app.route("/")
def hello():
    ptt_id = request.args.get('id', '')
    contents = ''

    if ptt_id != '':
        graber = Graber(ptt_id)
        graber.run()
        contents = graber.result()

    return render_template('index.html', ptt_id=ptt_id, contents=contents)

if __name__ == '__main__':
    app.run()
