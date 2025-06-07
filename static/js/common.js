(() => {
  let totalSeconds = 5 * 60;
  let interval = null;
  let sessionId = null;
  let clicks = 0;
  let errors = 0;
  let score = 0;

  const timeLeftEl = document.getElementById('time-left');
  const stopBtn = document.getElementById('stop-game-btn');
  const messageEl = document.getElementById('ai-message');

  if (!timeLeftEl || !stopBtn || !messageEl) {
    console.warn('AI control panel elements not found!');
    return;
  }

  function formatTime(s) {
    const m = Math.floor(s / 60).toString().padStart(2, '0');
    const sec = (s % 60).toString().padStart(2, '0');
    return `${m}:${sec}`;
  }

  async function startGameSession(gameName) {
    try {
      const resp = await fetch('/game/start-session/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add auth headers if needed
        },
        body: JSON.stringify({ game_name: gameName }),
        credentials: 'include', // if using session auth
      });
      const data = await resp.json();
      sessionId = data.session_id;
      console.log('Session started:', sessionId);
    } catch (e) {
      console.error('Failed to start session', e);
    }
  }

  async function stopGameSession() {
    if (!sessionId) return;
    try {
      await fetch('/game/stop-session/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          session_id: sessionId,
          duration_seconds: 5 * 60 - totalSeconds,
          clicks,
          errors,
          score,
        }),
      });
      console.log('Session stopped');
      sessionId = null;
    } catch (e) {
      console.error('Failed to stop session', e);
    }
  }

  function stopGame() {
    if (interval) clearInterval(interval);
    interval = null;
    messageEl.textContent = "⏰ Time's up! The game has been stopped.";
    stopBtn.disabled = true;
    document.dispatchEvent(new CustomEvent('gameStopRequested'));
    stopGameSession();
  }

  function startTimer(seconds = 5 * 60, gameName = 'unknown') {
    if (interval) clearInterval(interval);
    totalSeconds = seconds;
    stopBtn.disabled = false;
    messageEl.textContent = '';
    timeLeftEl.textContent = formatTime(totalSeconds);

    clicks = 0; // reset
    errors = 0; // reset
    score = 0;  // reset

    startGameSession(gameName);

    interval = setInterval(() => {
      totalSeconds--;
      timeLeftEl.textContent = formatTime(totalSeconds);
      if (totalSeconds <= 0) stopGame();

      if (totalSeconds === 60) {
        messageEl.textContent = "⚠️ One minute remaining!";
      }
    }, 1000);
  }

  stopBtn.onclick = () => {
    stopGame();
  };

  // Example of capturing clicks - customize per game needs
  document.addEventListener('click', () => {
    clicks++;
  });

  window.AIBehaviorControl = {
    startTimer,
    stopGame,
    incrementError: () => { errors++; },
    updateScore: (newScore) => { score = newScore; }
  };

  document.addEventListener('DOMContentLoaded', () => {
    startTimer();
  });
})();
