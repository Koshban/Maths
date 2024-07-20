#  Built this (mostly ) using GenAI prompts. 

## PerplexityPrompt to start the exercise: 
You are a Maths teacher and a Child Psychologist who specializes in making maths more interesting for 10-12 year olds.
My 11 year Old daughter likes Pop music and is a big fan of various Girl singers or bands. e.g. BlackPink, Twce, Taylor Swift, Sabrina Carpenter, Rihanna, Ariana Grande etc. I want to make a Maths-based game for her, and to make it interesting I want to involve points or cartoons or animes or anything else that you think you can make for this game. What suggestions do you have that I can incorporate? Would you be able to make anime images of these characters?

## PerplexityPrompt to generate prompts for creating images:  
Create Prompts for designing and creating the above Avatars so that I can use some AI Image generating bot like DALL-E to create them. Provide the prompts for all of the below BlackPink, Twce, Taylor Swift, Sabrina Carpenter, Rihanna, Ariana Grande , Beyonce, Camilla Cabelo, Meghan Trainor and Selena Gomez.

## artgenerator Prompts for generating the images: 
"Four chibi-style portraits of the members of the K-pop group Blackpink - Jennie, Jisoo, Rosé, and Lisa. The characters should have exaggerated features like large eyes, small bodies, and expressive poses. Use a vibrant, colorful palette to capture the playful, energetic spirit of the group. Ensure the images are appropriate for a 11-year old to consume. So ensure no nudity and appropriate clothing."

## artgenerator Prompts for generating the images: 
Generate some Pop Art Background . Use vibrant, pop art-inspired backgrounds and designs to make the math questions visually engaging.
Incorporate elements like neon colors, geometric patterns, and halftone effects

## ClaudePrompt to generate questions : 
Read the files, create a total of 30 similar questions as the ones in there . You can replace the image based questions with your own text based questions. For the questions with no images, you can use them as they are. Number the questions. Start numbering from 31. ie number the questions 31 to 120.

## ClaudePrompt to generate questions and answer mapping :
Take the following questions , convert them into a dictionary with Key as the question and the value as the answer.
e.g. question_answer = {"6. A shop sold 15 shirts on Monday and 12 shirts on Tuesday. How many shirts were sold in total over the two days? Let c be the total number of shirts sold." : "27"}

## ClaudePrompt to generate the Maths Game : 
You are a Middle School Maths Teacher and Python Expert. Write me Python Code for an interactive GUI-based game.
It should be a browser-based game.
The Game should have 16 Levels.
Each Level will have questions posed from the dictionary question_answer_N.
question_answer_N is a dictionary that is imported from common.config.question_answer_16.
It is of {key : value} type where key holds the questiona dn the value holds the answer.
for example question_answer_16 = {"question": "answer", }
Level 16 will have questions from the dictionary common.config.question_answer_16
question_answer_16 = {"question": "answer", }
For example :
question_answer_16 = { "In a class of 30 students, there are 18 girls. How many boys are there in the class? Let n be the number of boys.": "12", }

In a Level, one question will be asked at a time. Wait for the answer, and once provided confirm it's correct or not by checking it against the value of the question.
If not correct, show the correct answer on the screen.
After one question is completed, move to the next question for that level. Keep count of the score.
After every 5 maths questions in a level, interspersed with the trivia questions ( read from file common.triviaquestions.trivia_questions where the format is 

trivia_questions = {
    "1. What is the name of Blackpink's debut single?": "Whistle",
}
Add a countdown timer of 45 mins to each level.
At each level add a random background created from the jpeg files inside the folder  defined by the variable common.config.BackGroundImagesDir
After the Level is completed, give the score based on the total number of correct answers ( each correct answer is worth 10 marks ) and the time saved.
Where time saved in numbers = 45 mins - actual time in mins taken to complete the level.
Score Grading 
Less than 110 -- Needs more practise
110 - 140 -- Good
150 and above -- Excellent
After one Level is finished pick up a random jpeng or png file from the folder defined by the variable common.config.AnimeImagesDir and display it on the finished page.
Reset the Quesion_answer dictionary on RESET session or once a new level is started.

The below is my project structure.


math-trivia-game/
|── common
│   |── config.py
|   |── triviaquestions.py
|
├── static/
│ ├── images/
│ │ ├── BackGround/
│ │ └── AnimeArt/
│ |── script.js
│
├── templates/
│ └── index.html
|
├── app.py
└── requirements.txt

Create all the necessary files e.g. app.py , index.html ( if reqd ) and any othre HTML and CSS files if reqd.

# Math and Trivia Game

This project is a web-based game that combines math questions and trivia. The game is built using Flask for the backend and vanilla JavaScript for the frontend. Players are given 45 minutes to answer as many questions as possible, and their performance is graded based on their score and time saved.

## Features

- Dynamic question loading
- Timer functionality
- Score calculation
- Random background images
- Grading system based on performance

## Prerequisites

- Python 3.x
- Flask
- Basic knowledge of HTML, CSS, and JavaScript

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/math-trivia-game.git
    cd math-trivia-game
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```bash
    python app.py N
    ```
    where N is the Level you wnat to play. e.g. python app.py 4
5. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```

## Project Structure

math-trivia-game/
├── app.py
├── common/
│   ├── config.py
│   └── triviaquestions.py
├── static/
│   ├── images/
│   │   ├── BackGround/
│   │   └── AnimeArt/
│   ├── styles.css
│   └── script.js 
|── usefulscripts/
│   ├── create_question_sets.py
│   └── create_text_from_pdf.py
|
├── templates/
│   └── index.html
└── requirements.txt


- **`static/`**: Contains static files such as images and CSS.
- **`templates/`**: Contains HTML templates.
- **`triviaquestions.py`**: Contains trivia questions.
- **`app.py`**: The main Flask application.
- **`requirements.txt`**: Lists the Python dependencies.

## How to Play

1. Open the game in your browser.
2. Answer the questions that appear on the screen.
3. You have 45 minutes to answer as many questions as possible.
4. Your score and time saved will be displayed at the end of the game.
5. Your performance will be graded based on your score.

## Customization

### Adding Questions

- **Trivia Questions**: Add new questions to the `trivia_questions` dictionary in `triviaquestions.py`.
- **Math Questions**: To add more Maths Questions questions, 
    add them to dict question_answer.
    run usefulscripts/create_question_sets.py
        Change the range operator in the script above to modify the number of question sets you want
        Input those in some LLM , see prompt under section "ClaudePrompt to generate questions"
        Update the dictionaries in config , named question_answer_{N}.

### Adding/Changing Images

You can add them under static/images folder.
To generate more yourself, see prompt under section "artgenerator Prompts for generating the images"

### Changing Background Images

Add or remove images in the `static/images/BackGroundImagesDir` directory. The game will randomly select a background image from this directory each time it is loaded.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under a modified version of the MIT License that includes non-commercial use restrictions and revenue sharing terms. See the [LICENSE.txt](LICENSE.txt) file for more details.

Key points:
- Anyone is free to use, copy, modify, merge, publish, distribute, sublicense, and/or modify copies of the software.
- Commercial use of the software is not allowed without express written permission from the copyright holder, Kaushik Banerjee.
- If commercial use is permitted, the user must share 20% of the revenue generated from the commercial use with the copyright holder.

For more information about the license terms and conditions, please refer to the [LICENSE.txt](LICENSE.txt) file.