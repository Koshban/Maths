function updateQuestionCounter(current, total) {
    var progressDisplay = document.getElementById('question-progress');
    progressDisplay.textContent = `Question: ${current}/${total}`;
}

function startLevel(level) {
    window.location.href = `/start_level/${level}`;
}

function updateUI(data) {
    if (data.game_over) {
        document.getElementById('finalMessage').textContent = data.final_message;
        document.getElementById('answerInput').style.display = 'none';
        document.getElementById('submitButton').style.display = 'none';
    } else {
        document.getElementById('questionDisplay').textContent = data.next_question;
        document.getElementById('scoreDisplay').textContent = "Score: " + data.score;
    }
}


function submitAnswer() {
    const userAnswer = document.getElementById('answerInput').value; // Ensure you are using 'answerInput' as the ID in your HTML
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

        if (data.game_over) {
            document.getElementById('finalMessage').textContent = data.final_message + " Final Score: " + data.score; // Display final message and score
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

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startGameButton').addEventListener('click', function() {
        const selectedLevel = document.getElementById('levelSelect').value;
        startLevel(selectedLevel);
    });
});

function setupLevelDropdown() {
    const levelSelect = document.getElementById('levelSelect');
    for (let i = 1; i <= 16; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = 'Level ' + i;
        levelSelect.appendChild(option);
    }
    document.getElementById('startGameButton').addEventListener('click', function() {
        const selectedLevel = document.getElementById('levelSelect').value;
        console.log("Attempting to start level: " + selectedLevel); // Check if this logs in the console
        startLevel(selectedLevel);
    });
}

fetch('/submit_answer', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({user_answer: userAnswer})
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    console.log("Received data:", data);
    if (data.next_question === "No more questions") {
        alert("No more questions available.");
    } else {
        document.getElementById('question').textContent = data.next_question;
    }
    document.getElementById('score').textContent = "Score: " + data.score;
    document.getElementById('answer').value = ''; // Clear the input field
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
});

function fetchNextQuestion() {
    fetch('/next_question')
    .then(response => response.json())
    .then(data => {
        document.getElementById('questionDisplay').textContent = data.question; // Update the question display
        document.getElementById('answerInput').value = ''; // Clear the answer input field

        if (data.game_over) {
            // Handle the game over scenario
            document.getElementById('finalMessage').textContent = data.final_message || "Game Over! Thanks for playing.";
            document.getElementById('answerInput').style.display = 'none'; // Hide the answer input
            document.getElementById('submitButton').style.display = 'none'; // Hide the submit button
        }
    })
    .catch(error => {
        console.error('Error fetching the next question:', error);
        // Optionally display an error message to the user
        document.getElementById('finalMessage').textContent = "Error loading next question. Please try again!";
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

window.onload = function () {
    setupLevelDropdown();
    var fortyFiveMinutes = 60 * 45;
    var display = document.getElementById('timer');
    startTimer(fortyFiveMinutes, display);
    //submitAnswer(); // This is only for testing; remove it later
};