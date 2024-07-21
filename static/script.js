function updateQuestionCounter(current, total) {
    var progressDisplay = document.getElementById('question-progress');
    progressDisplay.textContent = `Question: ${current}/${total}`;
}

function startLevel(level) {
    window.location.href = `/start_level/${level}`;
}

function updateUI(data) {
    if (data.game_over) {
        var formattedFinalMessage = data.final_message.replace(/\n/g, '<br>');
        document.getElementById('finalMessage').innerHTML  = formattedFinalMessage;
        document.getElementById('answerInput').style.display = 'none';
        document.getElementById('submitButton').style.display = 'none';
    } else {
        var formattedFinalMessage = data.final_message.replace(/\n/g, '<br>');
        document.getElementById('questionDisplay').textContent = data.next_question;
        document.getElementById('scoreDisplay').textContent = "Score: " + data.score;
    }
}


function submitAnswer() {
    const userAnswer = document.getElementById('answerInput').value; 
    fetch('/submit_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user_answer: userAnswer})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('questionDisplay').textContent = data.next_question; // Update question display
        document.getElementById('scoreDisplay').textContent = "Score: " + data.score; // Update score display
        document.getElementById('answerInput').value = ''; // Clear the input field
        updateQuestionCounter(data.current_question, data.total_questions);
        if (data.game_over) {
            var formattedFinalMessage = data.final_message.replace(/\n/g, '<br>');
            document.getElementById('finalMessage').innerHTML = formattedFinalMessage //+ " Final Score: " + data.score; // Display final message and score
            document.getElementById('answerInput').style.display = 'none'; // Hide the answer input
            document.getElementById('submitButton').style.display = 'none'; // Hide the submit button
            // Display the anime image if URL is provided
            if (data.anime_image_url) {
                const imgElement = document.getElementById('animeImage');
                imgElement.src = data.anime_image_url;
                imgElement.style.display = 'block'; // Show the image
            }
        } else {
            alert(data.correct ? "Correct!" : `Incorrect! Correct answer was: ${data.correct_answer}`);
        }
    })
    .catch(error => console.error('Error:', error));
}

function fetchNextQuestion() {
    fetch('/next_question')
    .then(response => response.json())
    .then(data => {
        document.getElementById('questionDisplay').textContent = data.question; // Update the question display
        document.getElementById('answerInput').value = ''; // Clear the answer input field

        if (data.game_over) {
            // Handle the game over scenario
            var formattedFinalMessage = data.final_message.replace(/\n/g, '<br>');
            document.getElementById('finalMessage').innerHTML = formattedFinalMessage || "Game Over! Thanks for playing.";
            document.getElementById('answerInput').style.display = 'none'; // Hide the answer input
            document.getElementById('submitButton').style.display = 'none'; // Hide the submit button
        }
    })
    .catch(error => {
        var formattedFinalMessage = data.final_message.replace(/\n/g, '<br>');
        console.error('Error fetching the next question:', error);
        // Optionally display an error message to the user
        document.getElementById('finalMessage').innerHTML = "Error loading next question. Please try again!";
    });
}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(interval);
            alert("Time's up!");
            // Optionally, handle what to do next, e.g., end the game or move to the next level
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', function () {
    var fortyFiveMinutes  = 60 * 45;  // 45 minutes
    var display = document.getElementById('timer');
    startTimer(fortyFiveMinutes , display);
});

window.onload = function () {
    //var fortyFiveMinutes = 60 * 45;
    var display = document.getElementById('timer');
    startTimer(fortyFiveMinutes, display);
    
    //submitAnswer(); // This is only for testing; remove it later
};