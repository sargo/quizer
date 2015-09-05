# -*- coding: utf-8 -*-
"""
Quizer - a quiz application created with Flask.
"""

import os
from flask import Flask, session, request, render_template, redirect, url_for


# create app and initialize config
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('QUIZER_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    """
    Welcome page - quiz info and username form.
    """
    username = session.get('username')

    if request.method == 'POST':
        if not username:
            username = session['username'] = request.form['username']
        if username:
            return redirect(url_for('question_page'))

    return render_template('welcome.html', username=username)


@app.route('/pytanie', methods=['GET', 'POST'])
def question_page():
    """
    Quiz question page - show question, handle answer.
    """
    # ToDo


@app.route('/wynik')
def result_page():
    """
    Last page - show results.
    """
    # ToDo


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
