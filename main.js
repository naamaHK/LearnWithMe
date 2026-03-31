// Audio Context for the whole app
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let masterAudioCtx = null;

function playAppTone(freq, type, duration, vol=0.1) {
    if (!masterAudioCtx) masterAudioCtx = new AudioCtx();
    if (masterAudioCtx.state === 'suspended') masterAudioCtx.resume();
    
    const osc = masterAudioCtx.createOscillator();
    const gain = masterAudioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, masterAudioCtx.currentTime);
    gain.gain.setValueAtTime(vol, masterAudioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, masterAudioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(masterAudioCtx.destination);
    osc.start();
    osc.stop(masterAudioCtx.currentTime + duration);
}

function playSuccessApp() {
    playAppTone(523.25, 'sine', 0.1); 
    setTimeout(() => playAppTone(659.25, 'sine', 0.1), 100); 
    setTimeout(() => playAppTone(783.99, 'sine', 0.2), 200); 
}

function playFailApp() {
    playAppTone(300, 'triangle', 0.2);
    setTimeout(() => playAppTone(250, 'triangle', 0.4), 150);
}

function shakeApp() {
    const app = document.getElementById("app-container");
    app.classList.remove("shake");
    void app.offsetWidth;
    app.classList.add("shake");
}

function navigate(viewId) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
    document.getElementById(viewId).classList.add('active-view');
}
