const COLORS = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange'];
let score = 0, timeLeft = 30, currentFontColor = '', timerInterval;

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-btn');
  const timerElem = document.getElementById('timer');
  const scoreElem = document.getElementById('score');
  const colorWordElem = document.getElementById('color-word');
  const buttonsDiv = document.getElementById('buttons');
  const resultElem = document.getElementById('result');

  if (!startBtn) return;

  startBtn.onclick = () => {
    startBtn.style.display = 'none';
    timerElem.style.display = 'block';
    scoreElem.style.display = 'block';
    scoreElem.innerText = 'Score: 0';
    resultElem.innerText = '';
    colorWordElem.innerText = 'Loading...';
    score = 0;
    timeLeft = 30;
    startTimer();
    nextChallenge();
  };

  function startTimer() {
    timerElem.innerText = 'Time left: ' + timeLeft;
    timerInterval = setInterval(() => {
      timeLeft--;
      timerElem.innerText = 'Time left: ' + timeLeft;
      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        endGame();
      }
    }, 1000);
  }

  function nextChallenge() {
    fetch('/game/get_color_challenge/')
      .then(res => res.json())
      .then(data => {
        resultElem.innerText = '';
        colorWordElem.innerText = data.word;
        colorWordElem.style.color = data.font_color.toLowerCase();
        currentFontColor = data.font_color;

        buttonsDiv.innerHTML = '';
        data.colors.forEach(color => {
          const btn = document.createElement('button');
          btn.className = 'color-btn';
          btn.style.backgroundColor = color.toLowerCase();
          btn.style.color = 'white';
          btn.style.margin = '5px';
          btn.innerText = color;
          btn.onclick = () => checkAnswer(color);
          buttonsDiv.appendChild(btn);
        });
      })
      .catch(() => {
        resultElem.innerText = 'Error loading challenge. Please try again.';
      });
  }

  function checkAnswer(color) {
    if (color === currentFontColor) {
      score++;
      scoreElem.innerText = 'Score: ' + score;
      nextChallenge();
    } else {
      resultElem.innerText = 'Oops! Wrong color.';
    }
  }

  function endGame() {
    colorWordElem.innerText = 'Game Over!';
    buttonsDiv.innerHTML = '';
    resultElem.innerText = 'Your final score: ' + score;
    timerElem.style.display = 'none';
    scoreElem.style.display = 'none';
    startBtn.style.display = 'inline-block';
  }
});
