import os
import random
import time
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime, timedelta, timezone
from collections import deque
import random
from common import config, triviaquestions

app = Flask(__name__)
app.secret_key = 'your_very_secure_secret_key'  # Change this to a real secret key in production

def get_question(level, is_trivia=False):
    if is_trivia:
        question, answer = random.choice(list(triviaquestions.trivia_questions.items()))
    else:
        questions = getattr(config, f'question_answer_{level}')
        question, answer = random.choice(list(questions.items()))
    return question, answer

def get_trivia_question():
    # Assuming triviaquestions.trivia_questions is a dictionary {question: answer}
    if triviaquestions.trivia_questions:
        question, answer = random.choice(list(triviaquestions.trivia_questions.items()))
        return question, answer
    else:
        return None, None  # Return a default if no trivia questions are available

def fetch_next_question():
    level = session['level']
    total_math_questions = len(session['math_questions'])
    math_questions_answered = session.get('math_questions_answered', 0)
    trivia_questions_answered = session.get('trivia_questions_answered', 0)
    
    # Calculate the number of complete sets of five math questions answered
    complete_sets_of_five = math_questions_answered // 5

    # Check if it's time for a trivia question
    is_trivia_time = (complete_sets_of_five > trivia_questions_answered) and (math_questions_answered % 5 == 0)

    print(f"Math Questions Answered: {math_questions_answered}")
    print(f"Trivia Questions Answered: {trivia_questions_answered}")
    print(f"Is Trivia Time: {is_trivia_time}")

    if is_trivia_time:
        question, answer = get_trivia_question()
        session['trivia_questions_answered'] += 1
    else:
        if math_questions_answered < total_math_questions:
            question, answer = session['math_questions'][math_questions_answered]
            session['math_questions_answered'] += 1
        else:
            # Handle case where no more math questions are available
            # Calculate final score
            current_time = datetime.now(timezone.utc)  # Ensure time consistency
            start_time = session['start_time']
            time_difference = current_time - start_time
            time_taken = time_difference.total_seconds() // 60
            time_saved = max(45 - time_taken, 0)
            final_score = session['score'] + time_saved

            # Determine grade based on final score
            grade = calculate_grade(final_score)

            # Construct the final message
            session['final_message'] = (
                f"Final Score: {final_score}\n"
                f"You Completed {math_questions_answered} questions in {time_taken} minutes.\n"
                f"Your Grade is {grade}"
            )
            session['final_score'] = final_score
            session['game_over'] = True

            question = "No more math questions. Check your results."
            answer = "N/A"

    session['current_question'] = question
    session['current_answer'] = answer
    session['question_count'] += 1
    return question, answer

def calculate_grade(score):
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
    try:
        question_set = getattr(config, f'question_answer_{level}')
    except AttributeError:
        flash('Selected level does not exist.', 'error')
        return redirect(url_for('index'))

    if not question_set:
        flash('No questions available for this level.', 'error')
        return redirect(url_for('index'))
    session.clear()
    session['level'] = level
    session['math_questions'] = list(random.sample(list(getattr(config, f'question_answer_{level}').items()), 
                                                  k=len(getattr(config, f'question_answer_{level}'))))
    session['math_questions_answered'] = 0
    session['trivia_questions_answered'] = 0
    session['question_count'] = 0
    session['score'] = 0
    session['start_time'] = datetime.now(timezone.utc)  # Timezone-aware datetime set to UTC

    # Fetch the first question
    fetch_next_question()

    # Get a random background image
    bg_image = random_bg_image()

    # Render the index.html template with the necessary variables
    return render_template('index.html', question=session['current_question'], background_image=bg_image)

@app.route('/')
def index():
    # Redirect to the start_level route to initialize the game at level 1
    return redirect(url_for('start_level', level=1))

@app.route('/next_question', methods=['GET'])
def next_question():
    level = session['level']
    total_math_questions = len(session['math_questions'])
    math_questions_answered = session['math_questions_answered']
    trivia_questions_answered = session['trivia_questions_answered']

    is_trivia_time = (math_questions_answered % 5 == 0 and math_questions_answered != 0) or \
                     (math_questions_answered == total_math_questions and trivia_questions_answered < 1)

    if is_trivia_time:
        question, answer = get_trivia_question()
        session['trivia_questions_answered'] += 1
    else:
        if math_questions_answered < total_math_questions:
            question, answer = session['math_questions'][math_questions_answered]
            session['math_questions_answered'] += 1
        else:
            # Handle case where no more questions are available
            question, answer = "No more questions", "N/A"

    session['current_answer'] = answer
    session['question_count'] += 1

    return jsonify(question=question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.json['user_answer'].strip()
    correct_answer = session.get('current_answer').strip()
    # Initialize 'message' at the top to ensure it always has a value
    message = "Unexpected error occurred"  # Default message
    try:
        is_correct = float(user_answer) == float(correct_answer)
    except ValueError:
        is_correct = user_answer.lower() == correct_answer.lower()

    if is_correct:
        session['score'] += 10  # Each correct answer gives 10 points
        session['correct_answers'] = session.get('correct_answers', 0) + 1
        message = "Correct"
    else:
        message = f"Incorrect Correct answer was: {correct_answer}"

    # Always fetch the next question regardless of the correctness of the answer
    next_question, next_answer = fetch_next_question()
    #if session.get('game_over', False):
    anime_image_url = get_random_anime_image()  # Get a random anime image
    #else:
#        anime_image_url = ''

    

    print("After submitting answer:")
    print("Current Question Count:", session['question_count'])
    print("Math Questions Answered:", session['math_questions_answered'])
    print("Trivia Questions Answered:", session['trivia_questions_answered'])
    print("game_over:", session.get('game_over', False))
    print("final_message:", session.get('final_message', ''))
    print("anime_image_url:", anime_image_url)
    

    result = {
        'correct': is_correct,
        'score': session['score'],
        'next_question': next_question,
        'correct_answer': correct_answer,  # Ensure this is sent back
        'message': message,
        'game_over': session.get('game_over', False),
        'final_message': session.get('final_message', ''),
        'anime_image_url': anime_image_url
    }
    return jsonify(result)
    

@app.route('/next_level', methods=['POST'])
def next_level():
    level = session.get('level', 1)
    if level < 16:
        session['level'] += 1
        session['question_count'] = 0
        question, answer = get_question(session['level'], session['question_count'])
        session['current_answer'] = answer
        return jsonify({'next_level': session['level'], 'next_question': question})
    else:
        return jsonify({'game_over': True, 'final_score': session['score']})

if __name__ == '__main__':
    app.run(debug=True)