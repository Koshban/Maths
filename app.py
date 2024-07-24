import os
import random
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timezone
import random
import argparse
import inspect
import logging
import re
from common import config, triviaquestions

app = Flask(__name__)
app.secret_key = 'your_very_secure_secret_key'  # Change this to a real secret key in production
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f'app_{ts}.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# Set up argparse
parser = argparse.ArgumentParser(description='Start the Math Game at a specific level.')
parser.add_argument('level', type=int, choices=range(1, 17), help='The starting level of the game (1-16)')
args = parser.parse_args()

# Validate and set the level in Flask app config
app.config['START_LEVEL'] = args.level
logging.debug(f"After Args , Level is {app.config['START_LEVEL']}")

def get_question(level, is_trivia=False):
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Inside {function_name}")
    if is_trivia:
        question, answer = random.choice(list(triviaquestions.trivia_questions.items()))
    else:
        questions = getattr(config, f'question_answer_{level}')
        question, answer = random.choice(list(questions.items()))
    return question, answer

def get_trivia_question():
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Inside {function_name}")
    if triviaquestions.trivia_questions:
        question, answer = random.choice(list(triviaquestions.trivia_questions.items()))
        return question, answer
    else:
        return None, None  # Return a default if no trivia questions are available

def fetch_next_question():
    level = session['level']
    total_math_questions = len(session['math_questions'])
    questions = session['math_questions']
    math_questions_answered = session.get('math_questions_answered', 0)
    trivia_questions_answered = session.get('trivia_questions_answered', 0)
    total_trivia_questions = 3 # session.get('total_trivia_questions', 0) 
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Questions are : {questions} Inside 1st Logging of {function_name}")
    logging.debug(f"Current Maths Count: {math_questions_answered} Inside 1st Logging of {function_name}")
    logging.debug(f"Total Maths Count: {total_math_questions} Inside 1st Logging of {function_name}")
    logging.debug(f"Trivia Count: {trivia_questions_answered} Inside 1st Logging of {function_name}")
    
    # Calculate the number of complete sets of five math questions answered
    complete_sets_of_five = math_questions_answered // 5

    # Check if it's time for a trivia question
    is_trivia_time = (complete_sets_of_five > trivia_questions_answered) and (math_questions_answered % 5 == 0)

    logging.debug(f"Math Questions Answered: {math_questions_answered} Inside {function_name}")
    logging.debug(f"Trivia Questions Answered: {trivia_questions_answered} Inside {function_name}")
    logging.debug(f"Is Trivia Time: {is_trivia_time}")

    if is_trivia_time:
        if trivia_questions_answered < total_trivia_questions:
            question, answer = get_trivia_question()
            logging.debug(f"Trivia Question: {question} Inside {function_name}")
            logging.debug(f"Trivia Answer: {answer} Inside {function_name}")
            session['trivia_questions_answered'] += 1
    elif math_questions_answered < total_math_questions:
        #question, answer = session['math_questions'][math_questions_answered]
        question, answer = questions[math_questions_answered]
        # session['current_question'] = question
        # session['current_answer'] = answer
        session['math_questions_answered'] = math_questions_answered + 1
        # session['question_count'] = math_questions_answered + 1
        current_frame = inspect.currentframe()
        function_name = inspect.getframeinfo(current_frame).function
        logging.debug(f"Current Maths Count: {math_questions_answered} Inside Else IF of {function_name}")
        logging.debug(f"Maths Question : {question} Inside Else IF of {function_name}")
    else:
        current_time = datetime.now(timezone.utc)  # Ensure time consistency
        start_time = session['start_time']
        time_difference = current_time - start_time
        time_taken = time_difference.total_seconds() // 60
        time_saved = max(45 - time_taken, 0)
        final_score = session['score'] + time_saved
        grade = calculate_grade(final_score)
        # Construct the final message
        session['final_message'] = (
            f"Final Score: {final_score}\n"
            f"You Completed {math_questions_answered} questions in {time_taken} minutes.\n"
            f"Your Grade is {grade}"
        )
        session['final_score'] = final_score
        question = "No more math questions. Check your results."
        answer = "N/A"
        session['game_over'] = True
        current_frame = inspect.currentframe()
        function_name = inspect.getframeinfo(current_frame).function
        logging.debug(f"Current Maths Count: {math_questions_answered} Inside Else ELSE of {function_name}")

    session['current_question'] = question
    session['current_answer'] = answer
    #session['math_questions_answered'] = math_questions_answered + 1
    session['question_count'] = math_questions_answered + 1
    #session['trivia_questions_answered'] += is_trivia_time 

    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Current Question Count: {session['question_count']} Inside 2nd logging of {function_name}")
    logging.debug(f"Current Maths Count: {math_questions_answered } Inside 2nd logging of {function_name}")
    logging.debug(f"Current Question to be returned is : {question } Inside 2nd logging of {function_name}")
    logging.debug(f"Current Answer to be returned is : {answer } Inside 2nd logging of {function_name}")

    return question, answer

def calculate_grade(score):
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Inside {function_name}")
    if score < 150:
        return "Needs more practice"
    elif score < 180:
        return "Good"
    else:
        return "Excellent"

def random_bg_image():
    bg_images = os.listdir(config.BackGroundImagesDir)
    random_bg = random.choice(bg_images)
    # Normalize the path for URL usage
    web_path = os.path.join('images/BackGround', random_bg).replace('\\', '/')
    return web_path

def get_random_anime_image():
    # List all files in the AnimeImagesDir
    files = [f for f in os.listdir(config.AnimeImagesDir) if f.endswith(('.jpeg', '.png'))]
    if files:
        # Select a random file
        selected_image = random.choice(files)
        # Create a web-friendly path, ensuring to replace backslashes with forward slashes
        image_path = os.path.join('images', 'AnimeArt', selected_image)
        # Return the URL path for this image
        return url_for('static', filename=image_path.replace("\\", "/"))
    return None

@app.route('/start_level/<int:level>', methods=['GET'])
def start_level(level):
    logging.debug(f"Inside Start Level. Level is : {level}")
    session.clear()
    session['level'] = level
    session['math_questions'] = list(random.sample(list(getattr(config, f'question_answer_{level}').items()), 
                                                  k=len(getattr(config, f'question_answer_{level}'))))
    session['math_questions_answered'] = 0
    session['trivia_questions_answered'] = 0
    session['question_count'] = 0
    session['score'] = 0
    session['start_time'] = datetime.now(timezone.utc)  # Timezone-aware datetime set to UTC
    math_questions_answered = session['math_questions_answered']
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    question, _ = fetch_next_question()
    total_questions = len(session.get('math_questions', []))
    # Get a random background image
    bg_image = random_bg_image()
    logging.debug(f"Current Question Count: {session['question_count']} Inside {function_name}")
    logging.debug(f"Current Question is : {question} Inside {function_name}")
    logging.debug(f"Maths answered is : {math_questions_answered} Inside {function_name}")
    # Render the index.html template with the necessary variables
    return render_template('index.html', question=question, level=level, total_questions=total_questions, background_image=bg_image)

@app.route('/')
def index():
    return redirect(url_for('start_level', level=app.config['START_LEVEL']))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    user_answer = request.json['user_answer'].strip().lower()
    correct_answer = session.get('current_answer', '').strip().lower()
    logging.debug(f"user_answer: {user_answer} Inside {function_name}")
    logging.debug(f"correct_answer: {correct_answer} Inside {function_name}")
    # Initialize 'message' at the top to ensure it always has a value
    message = "Unexpected error occurred"  # Default message
    is_correct = user_answer == correct_answer

    if is_correct:
        session['score'] += 10  # Each correct answer gives 10 points
        session['correct_answers'] = session.get('correct_answers', 0) + 1
        message = "Correct"
    else:
        message = f"Incorrect Correct answer was: {correct_answer}"

    # Always fetch the next question regardless of the correctness of the answer
    
    next_question, next_answer = fetch_next_question()
    total_questions = len(session.get('math_questions', []))  
    anime_image_url = get_random_anime_image()  # Get a random anime image
    
    logging.debug("After submitting answer:")
    logging.debug(f"Math Questions Answered: {session['math_questions_answered']} Inside {function_name}")
    logging.debug(f"Trivia Questions Answered: {session['trivia_questions_answered']}")
    logging.debug(f"correct_answer: {correct_answer}")
    logging.debug(f"game_over: {session.get('game_over', False)}")
    logging.debug(f"final_message: {session.get('final_message', '  ')}")
    logging.debug(f"anime_image_url: anime_image_url")
    logging.debug(f"Current Quesion is : {session['math_questions_answered'] + 1}")
    current_frame = inspect.currentframe()
    function_name = inspect.getframeinfo(current_frame).function
    logging.debug(f"Current Question Count: {session['question_count']} Inside {function_name}")

    result = {
        'correct': is_correct,
        'score': session['score'],
        'next_question': next_question,
        'correct_answer': correct_answer, 
        'message': message,
        'game_over': session.get('game_over', False),
        'final_message': session.get('final_message', ''),
        'anime_image_url': anime_image_url,
        'current_question': session['math_questions_answered'],  
        'total_questions': total_questions
    }
    logging.debug(f"Returning  : {result}")
    return jsonify(result)
    

@app.route('/next_level', methods=['POST'])
def next_level():
    level = session.get('level', 1)
    if level < 16:
        session['level'] += 1
        session['question_count'] = 0
        question, answer = get_question(session['level'], session['question_count'])
        session['current_answer'] = answer
        current_frame = inspect.currentframe()
        function_name = inspect.getframeinfo(current_frame).function
        logging.debug(f"Current Question Count: {session['question_count']} Inside {function_name}")
        return jsonify({'next_level': session['level'], 'next_question': question})
    else:
        return jsonify({'game_over': True, 'final_score': session['score']})

if __name__ == '__main__':
    app.run(debug=True)