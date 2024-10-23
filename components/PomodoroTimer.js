// components/PomodoroTimer.js
import { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Settings } from 'lucide-react';
import '../styles/PomodoroTimer.css';

const PomodoroTimer = () => {
  // State management
  const [minutes, setMinutes] = useState(25);
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState('work'); // work, break, longBreak
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState({
    workTime: 25,
    breakTime: 5,
    longBreakTime: 15,
  });

  // Timer logic
  useEffect(() => {
    let interval = null;
    
    if (isActive) {
      interval = setInterval(() => {
        if (seconds > 0) {
          setSeconds(seconds - 1);
        }
        if (seconds === 0) {
          if (minutes === 0) {
            setIsActive(false);
            handleTimerComplete();
          } else {
            setMinutes(minutes - 1);
            setSeconds(59);
          }
        }
      }, 1000);
    }
    
    return () => clearInterval(interval);
  }, [isActive, minutes, seconds]);

  // Timer completion handler
  const handleTimerComplete = () => {
    if (mode === 'work') {
      setMode('break');
      setMinutes(settings.breakTime);
    } else if (mode === 'break') {
      setMode('work');
      setMinutes(settings.workTime);
    }
  };

  // Control functions
  const toggleTimer = () => setIsActive(!isActive);

  const resetTimer = () => {
    setIsActive(false);
    if (mode === 'work') {
      setMinutes(settings.workTime);
    } else if (mode === 'break') {
      setMinutes(settings.breakTime);
    } else {
      setMinutes(settings.longBreakTime);
    }
    setSeconds(0);
  };

  const updateSettings = (newSettings) => {
    setSettings(newSettings);
    setShowSettings(false);
    resetTimer();
  };

  return (
    <div className="pomodoro-container">
      <div className="timer-card">
        <div className="text-center">
          <h1 className="timer-title">
            {mode === 'work' ? 'Work Time' : mode === 'break' ? 'Break Time' : 'Long Break'}
          </h1>
          
          <div className="timer-display">
            {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
          </div>

          <div className="controls-container">
            <button
              onClick={toggleTimer}
              className="control-button play-button"
            >
              {isActive ? <Pause size={24} /> : <Play size={24} />}
            </button>
            
            <button
              onClick={resetTimer}
              className="control-button secondary-button"
            >
              <RotateCcw size={24} />
            </button>
            
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="control-button secondary-button"
            >
              <Settings size={24} />
            </button>
          </div>

          {showSettings && (
            <div className="settings-panel">
              <h2 className="settings-title">Settings</h2>
              <div className="settings-form">
                <div>
                  <label className="input-label">Work Time (minutes)</label>
                  <input
                    type="number"
                    value={settings.workTime}
                    onChange={(e) => setSettings({...settings, workTime: parseInt(e.target.value)})}
                    className="time-input"
                  />
                </div>
                <div>
                  <label className="input-label">Break Time (minutes)</label>
                  <input
                    type="number"
                    value={settings.breakTime}
                    onChange={(e) => setSettings({...settings, breakTime: parseInt(e.target.value)})}
                    className="time-input"
                  />
                </div>
                <button
                  onClick={() => updateSettings(settings)}
                  className="save-button"
                >
                  Save Settings
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PomodoroTimer;