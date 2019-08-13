# -*- coding: utf-8 -*-
"""
Quizer - a quiz application created with Flask.
"""

import csv
import os
import random
import time
from flask import Flask, session, request, render_template, redirect, url_for


# create app and initialize config
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    DATA_FILE='data/quiz.csv',
    TIME_TRESHOLDS=[10, 30],
))
app.config.from_envvar('QUIZER_SETTINGS', silent=True)


ANSWER_IDS = ['A', 'B', 'C', 'D', 'E']


@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    """
    Welcome page - quiz info and username form.
    """
    questions = get_questions()
    session['points'] = 0
    session['to_ask'] = random.sample(questions, 5)

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
    if request.method == 'POST':
        if request.form.get('answer') == session['correct_answer']:
            diff_time = time.time() - session['start_time']
            time_thresholds = app.config['TIME_TRESHOLDS']
            if diff_time < time_thresholds[0]:
                session['points'] += 3
            elif diff_time < time_thresholds[1]:
                session['points'] += 2
            else:
                session['points'] += 1
        if not session['to_ask']:
            return redirect(url_for('result_page'))
        else:
            return redirect(url_for('question_page'))
    else:
        if not session['to_ask']:
            return redirect(url_for('result_page'))
        question = session['to_ask'].pop()
        session['correct_answer'] = question[-1]
        session['start_time'] = time.time()
        return render_template(
            'question.html',
            question=question[0],
            answers=zip(ANSWER_IDS, question[1:-1])
        )


@app.route('/wynik')
def result_page():
    """
    Last page - show results.
    """
    return render_template(
        'result.html',
        points=session['points'],
        points_procent=int((session['points'] / 15.0) * 100)
    )


def get_questions():
    """
    Parse CSV file with questions.
    """
    with open(app.config['DATA_FILE'], 'rb') as csvfile:
        line = csv.reader(csvfile, delimiter=';')
        return [[unicode(cell, 'utf-8') for cell in row] for row in line]


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
