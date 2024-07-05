from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCDE"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Select the survey"""
    return render_template("sur_start.html" , survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """clears the responses"""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer" , methods=["POST"])
def handle_responses():
    """Save response and go to next question"""

    # get the choice that the user selects
    choice = request.form["answer"]

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question"""

    # get the responses session list
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect("/")
    
    if (len(responses) != id):
        flash(f"Invalid question id: {id}")
        return redirect(f"/questions/{len(responses)}")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    question = survey.questions[id]
    return render_template("question.html" , question=question , question_num=id)
    

@app.route("/complete")
def thank_survey():
    """Thank for completing the survey"""

    return render_template("complete.html")