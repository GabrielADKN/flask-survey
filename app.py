from flask import Flask, render_template, request, redirect, url_for, flash, abort
from surveys import satisfaction_survey
import pdb 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

responses = []


@app.route('/')
def start():
    responses.clear()
    return render_template('start.html', survey_title='Customer Satisfaction Survey',
                           survey_instructions='Please answer the following questions to help us improve.')


@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def show_question(question_id):
    if question_id > len(satisfaction_survey.questions):
        flash('Invalid question access.', 'error')
        return redirect(url_for('show_question', question_id=len(responses)))

    if question_id != len(responses):
        flash('Please answer questions in order.', 'error')
        return redirect(url_for('show_question', question_id=len(responses)))
    
    # if request.method == 'POST':
    #     answer = request.form.get('answer')
    #     if answer == '':
    #         flash('Please select an answer before moving on.', 'error')
    #         return redirect(url_for('show_question', question_id=len(responses)))

    #     responses.append(answer)

    #     if len(responses) == len(satisfaction_survey.questions):
    #         return redirect(url_for('thank_you'))

    #     return redirect(url_for('show_question', question_id=len(responses)))

    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question=question, question_id=question_id)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form.get('answer')
    # pdb.set_trace()
    if  not answer:
        flash('Please select an answer before moving on.', 'error')
        return redirect(url_for('show_question', question_id=len(responses)))
    
    responses.append(answer)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))

    return redirect(url_for('show_question', question_id=len(responses)))

@app.route('/thank-you')
def thank_you():
    flash('Thank you for taking our survey!', 'success')
    return render_template('thankyou.html',responses=responses)


if __name__ == '__main__':
    app.run(debug=True)
