from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension
import pdb 
# import ipdb

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'your_secret_key'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


responses = []

# responses = {}

@app.route('/', methods=['GET', 'POST'])
def start():
    session['responses'] = []
    # session['responses'] = []
    return render_template('start.html', survey_title=satisfaction_survey.title,
                           survey_instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def show_question(question_id):
    # if question_id == 0:
    #     session['responses'] = []
        
    responses = session.get('responses')
    
    print("Current question_id:", question_id)
    print("Current responses:", session["responses"])

       
    if question_id > len(satisfaction_survey.questions):
        flash('Invalid question access.', 'error')
        return redirect(url_for('show_question', question_id=len(responses)))

    if question_id != len(session['responses']):
        # pdb.set_trace()
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

    # pdb.set_trace()
    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question=question, question_id=question_id)

@app.route('/answer', methods=['POST'])
def handle_answer():
    # breakpoint()
    # responses = session.get('responses', [])
    answer = request.form.get('answer')
    # pdb.set_trace()
    if  not answer:
        flash('Please select an answer before moving on.', 'error')
        return redirect(url_for('show_question', question_id=len(responses)))
    
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))

    return redirect(url_for('show_question', question_id=len(responses)))

@app.route('/thank-you')
def thank_you():
    responses = session.get('responses', [])
    flash('Thank you for taking our survey!', 'success')
    return render_template('thankyou.html',responses=responses)


if __name__ == '__main__':
    app.run(debug=True)
