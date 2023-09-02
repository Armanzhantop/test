from random import randint, shuffle
import os
from flask import Flask, session, redirect, url_for, request, render_template
from db_scripts import get_question_after, get_quises, check_answer
def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answer'] = 0
    session['total'] = 0
def end_quiz():
    session.clear()
def quiz_form():
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)
def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return redirect(url_for('test'))
def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answer'] += 1
def qeestion_form(question):
    answer_list = [question[2], question[3], question[4], question[5]]
    shuffle(answer_list)
    return render_template('test.html', question=question[1], quest_id=question[0],answer_list=answer_list)
def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return qeestion_form(next_question)
def result():
    html = render_template('result.html', right=session['answer'], total=session['total'])
    end_quiz()
    return html
folder = os.getcwd()
#Создаем обьект веб-приложения:
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['post', 'get']) #создает правило для URL '/'
app.add_url_rule('/test', 'test', test, methods=['post', 'get']) ##создает правило для URL '/test'
app.add_url_rule('/result', 'result', result) ##создает правило для URL '/result'
#устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'ThisIsSecret'

if __name__ == '__main__':
    #Запускаем веб-сервер:
    app.run()