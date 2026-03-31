const WRITING_WORDS = [
    ["תפוח", "תַּפּוּחַ"], ["פרפר", "פַּרְפַּר"], ["שמש", "שֶׁמֶשׁ"], ["ירח", "יָרֵחַ"],
    ["עץ", "עֵץ"], ["דג", "דָּג"], ["בית", "בַּיִת"], ["פרח", "פֶּרַח"],
    ["כלב", "כֶּלֶב"], ["חתול", "חָתוּל"], ["ספר", "סֵפֶר"], ["כוכב", "כּוֹכָב"],
    ["אוטו", "אוֹטוֹ"], ["לב", "לֵב"], ["ענן", "עָנָן"], ["בננה", "בַּנָּנָה"],
    ["כדור", "כַּדּוּר"], ["רכבת", "רַכֶּבֶת"], ["עוגה", "עוּגָה"], ["גלידה", "גְּלִידָה"],
    ["ספינה", "סְפִינָה"], ["ארנב", "אַרְנָב"], ["תות", "תּוּת"], ["עפרון", "עִפָּרוֹן"],
    ["פיל", "פִּיל"], ["ענב", "עֵנָב"], ["עין", "עַיִן"], ["עורב", "עוֹרֵב"],
    ["עפיפון", "עֲפִיפוֹן"], ["אריה", "אַרְיֵה"], ["ציפור", "צִפּוֹר"], ["צב", "צָב"],
    ["ים", "יָם"], ["שולחן", "שֻלְחָן"], ["כיסא", "כִּיסֵא"], ["מטוס", "מָטֹס"],
    ["טיל", "טִיל"], ["דלת", "דֶּלֶת"], ["עכבר", "עַכבָּר"], ["עכביש", "עַכָּבִש"],
    ["סוס", "סוּס"], ["פרה", "פָּרָה"], ["צפרדע", "צְפַרדֵּע"], ["שמלה", "שִמְלָה"],
    ["מגפיים", "מַגָּפַיִם"], ["מתנה", "מַתָּנָה"], ["פטרייה", "פִטְרִיָה"], ["עיט", "עַיִט"],
    ["שמיים", "שָמַיִם"], ["גשר", "גֶּשֶׁר"]
];

const HEB_KEYBOARD = [
    ["ק","ר","א","ט","ו","ן","ם","פ"],
    ["ש","ד","ג","כ","ע","י","ח","ל","ך","ף"],
    ["ז","ס","ב","ה","נ","מ","צ","ת","ץ"]
];

let writingMode = 'A'; 
let currentWordPlain = "";
let currentWordNiqqud = "";
let currentInput = "";
let writingGuessesLeft = 3;

function startWritingGame(mode) {
    writingMode = mode;
    document.getElementById("writing-game-title").textContent = 
        mode === 'A' ? "🔤 מַה הָאוֹת הָרִאשׁוֹנָה?" : "📝 כְּתֹב אֶת הַמִּלָּה";
    document.getElementById("writing-instruction").textContent = 
        mode === 'A' ? "הִסְתַּכְּלוּ עַל הַתְּמוּנָה — כִּתְבוּ אֶת הָאוֹת הָרִאשׁוֹנָה!" : "הִסְתַּכְּלוּ עַל הַתְּמוּנָה — כִּתְבוּ אֶת הַמִּלָּה הַשְּׁלֵמָה!";
        
    generateKeyboard();
    navigate('view-writing-game');
    newWritingQuestion();
}

function generateKeyboard() {
    const kb = document.getElementById("writing-keyboard");
    kb.innerHTML = "";
    HEB_KEYBOARD.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "keyboard-row";
        row.forEach(letter => {
            const btn = document.createElement("button");
            btn.className = "key-btn";
            btn.textContent = letter;
            btn.onclick = () => handleKeyPress(letter);
            rowDiv.appendChild(btn);
        });
        kb.appendChild(rowDiv);
    });
    
    // add backspace
    const bsRow = document.createElement("div");
    bsRow.className = "keyboard-row";
    const bsBtn = document.createElement("button");
    bsBtn.className = "key-btn backspace-btn";
    bsBtn.textContent = "⌫ מְחַק";
    bsBtn.onclick = () => {
        currentInput = currentInput.slice(0, -1);
        updateInputDisplay();
    };
    bsRow.appendChild(bsBtn);
    kb.appendChild(bsRow);
}

function handleKeyPress(letter) {
    if (writingGuessesLeft <= 0) return;
    const maxLen = writingMode === 'A' ? 1 : currentWordPlain.length;
    if (currentInput.length < maxLen) {
        currentInput += letter;
        updateInputDisplay();
    }
}

function updateInputDisplay() {
    const disp = document.getElementById("writing-input-display");
    disp.innerHTML = "";
    const targetLen = writingMode === 'A' ? 1 : currentWordPlain.length;
    
    for (let i = 0; i < targetLen; i++) {
        const span = document.createElement("span");
        span.className = "letter-box";
        if (i < currentInput.length) {
            span.textContent = currentInput[i];
            span.classList.add("filled");
        }
        disp.appendChild(span);
    }
}

function newWritingQuestion() {
    const wordPair = WRITING_WORDS[Math.floor(Math.random() * WRITING_WORDS.length)];
    currentWordPlain = wordPair[0];
    currentWordNiqqud = wordPair[1];
    currentInput = "";
    writingGuessesLeft = 3;
    
    updateWritingLives();
    updateInputDisplay();
    
    const img = document.getElementById("writing-image");
    img.src = `images/${currentWordPlain}.png`;
    img.style.borderColor = "#AED6F1";
    
    const fb = document.getElementById("writing-feedback");
    fb.textContent = "";
    fb.className = "feedback";
    document.getElementById("btn-check-writing").disabled = false;
}

function updateWritingLives() {
    const hearts = "❤️".repeat(writingGuessesLeft) + "🖤".repeat(3 - Math.max(0, writingGuessesLeft));
    document.getElementById("writing-lives").textContent = `נִסְיוֹנוֹת: ${hearts}`;
}

function checkWritingAnswer() {
    if (writingGuessesLeft <= 0) return;
    const target = writingMode === 'A' ? currentWordPlain[0] : currentWordPlain;
    if (currentInput.length < target.length) return;
    
    const fb = document.getElementById("writing-feedback");
    
    if (currentInput === target) {
        playSuccessApp();
        fb.textContent = PRAISES[Math.floor(Math.random() * PRAISES.length)];
        fb.className = "feedback success";
        writingGuessesLeft = 0;
        document.getElementById("btn-check-writing").disabled = true;
        document.getElementById("writing-image").style.borderColor = "#2CD889";
        setTimeout(newWritingQuestion, 2000);
    } else {
        writingGuessesLeft--;
        playFailApp();
        shakeApp();
        updateWritingLives();
        currentInput = "";
        updateInputDisplay();
        if (writingGuessesLeft === 0) {
            fb.textContent = `😔 התשובה היא: ${target} (${currentWordNiqqud})`;
            fb.className = "feedback error";
            document.getElementById("btn-check-writing").disabled = true;
            document.getElementById("writing-image").style.borderColor = "#FF5A5A";
            setTimeout(newWritingQuestion, 3000);
        } else {
            fb.textContent = TRY_AGAIN[Math.floor(Math.random() * TRY_AGAIN.length)];
            fb.className = "feedback error";
        }
    }
}

function readWritingWord() {
    const text = currentWordPlain;
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = 'he-IL';
    const voices = window.speechSynthesis.getVoices();
    const hebrewVoice = voices.find(v => v.lang.includes('he')) || voices.find(v => v.name.includes('Carmit'));
    if (hebrewVoice) msg.voice = hebrewVoice;
    window.speechSynthesis.speak(msg);
}

// Support physical keyboard
document.addEventListener('keydown', (e) => {
    if (!document.getElementById('view-writing-game').classList.contains('active-view')) return;
    const char = e.key;
    if (/^[א-ת]$/.test(char)) {
        handleKeyPress(char);
    } else if (char === 'Backspace') {
        currentInput = currentInput.slice(0, -1);
        updateInputDisplay();
    } else if (char === 'Enter') {
        checkWritingAnswer();
    }
});
