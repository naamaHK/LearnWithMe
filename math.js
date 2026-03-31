const MATH_THEMES = [
    ["🍎", "#FDEDEC"], ["🦋", "#F5EEF8"], ["⭐", "#FEFCBF"], ["🍌", "#FFFDE7"],
    ["🐟", "#EAF4FB"], ["🌸", "#FCE4EC"], ["🍊", "#FFF3E0"], ["🐝", "#FFFDE7"],
    ["🍇", "#F3E5F5"], ["🚀", "#E8EAF6"]
];

const PRAISES = [
    "🎉 כׇּל הַכָּבוֹד! עֲנִיתֶם נָכוֹן! אַתֶּם מַדְהִימִים! 🌟",
    "⭐ יָפֶה מְאֹד! פָּתַרְתֶּם נָכוֹן! 🎊",
    "🏆 וָאוּ! נָכוֹן לְגַמְרֵי! אַתֶּם גְּאוֹנִים! 🎉",
    "🌈 מְצֻיָּן! כׇּל הַכָּבוֹד לָכֶם! ⭐",
    "🎯 נָכוֹן! אַתֶּם מַמָּשׁ טוֹבִים בָּזֶה! 🥳"
];
const TRY_AGAIN = [
    "💪 נַסוּ שׁוּב! אַתֶם יְכוֹלִים! 😊",
    "🤔 כִּמְעַט! נַסּוּ לִסְפּוֹר שׁוּב בִּזְהִירוּת...",
    "✨ תְּנחוּ שׁוּב פַּעַם אַחַת!",
    "🧐 הִסְתַּכְּלוּ טוֹב טוֹב עַל הַצִּיּוּרִים..."
];

let mathMaxVal = 10;
let mathOp = "+";
let mathA = 0;
let mathB = 0;
let mathAnswer = 0;
let mathGuessesLeft = 3;
let mathTheme = MATH_THEMES[0];

function startMathGame(maxVal) {
    mathMaxVal = maxVal;
    
    let titleStr = "";
    let colorStr = "";
    if (maxVal <= 10) { titleStr = "🌱 חִבּוּר וְחִסּוּר עַד 10"; colorStr = "#1E8449"; }
    else if (maxVal <= 20) { titleStr = "🌿 חִבּוּר וְחִסּוּר עַד 20"; colorStr = "#2874A6"; }
    else { titleStr = "🌳 חִבּוּר וְחִסּוּר עַד 100"; colorStr = "#6C3483"; }
    
    document.getElementById("math-game-title").textContent = titleStr;
    document.getElementById("math-game-title").style.color = colorStr;
    
    navigate('view-math-game');
    newMathQuestion();
}

function updateMathLives() {
    const hearts = "❤️".repeat(mathGuessesLeft) + "🖤".repeat(3 - Math.max(0, mathGuessesLeft));
    document.getElementById("math-lives").textContent = `נִסְיוֹנוֹת: ${hearts}`;
}

function drawMathVisual(a, b, op, theme, maxVal) {
    const canvas = document.getElementById("mathCanvas");
    const ctx = canvas.getContext("2d");
    const emoji = theme[0];
    const bgCol = theme[1];
    
    // sizing
    let iconSize = 34, maxCols = 5;
    if (maxVal > 10 && maxVal <= 20) { iconSize = 28; maxCols = (op==="+")?5:10; }
    else if (maxVal > 20) { iconSize = 22; maxCols = 10; }
    
    const cell = iconSize + 4;
    
    function measureBox(count) {
        if(count === 0) return {w: 52, h: 52};
        const cols = Math.min(count, maxCols);
        const rows = Math.ceil(count / maxCols);
        return {w: cols * cell + 10, h: rows * cell + 10};
    }
    
    const dimA = measureBox(a);
    const dimB = measureBox(b);
    
    if (op === "+") {
        canvas.width = 10 + dimA.w + 44 + dimB.w + 10;
        canvas.height = Math.max(dimA.h, dimB.h) + 20;
    } else {
        const dimTotal = measureBox(a);
        canvas.width = Math.max(200, dimTotal.w + 20);
        canvas.height = Math.max(80, dimTotal.h + 20);
    }
    
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.textBaseline = "middle";
    ctx.textAlign = "center";
    
    function drawIconBox(count, x, y, fill, outline, isCrossedOffset=0) {
        let bw = measureBox(count).w;
        let bh = measureBox(count).h;
        
        ctx.fillStyle = fill;
        ctx.strokeStyle = outline;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.roundRect(x,y,bw,bh,8);
        ctx.fill(); ctx.stroke();
        
        if (count === 0) {
            ctx.fillStyle = "#7F8C8D";
            ctx.font = "bold 18px Arial";
            ctx.fillText("0", x + bw/2, y + bh/2);
            return;
        }
        
        for (let i=0; i<count; i++) {
            let col = i % maxCols;
            let row = Math.floor(i / maxCols);
            let cx = x + 5 + col*cell + iconSize/2;
            let cy = y + 5 + row*cell + iconSize/2;
            
            let crossed = (i >= isCrossedOffset && op === "-");
            
            ctx.beginPath();
            ctx.arc(cx, cy, iconSize/2, 0, Math.PI*2);
            ctx.fillStyle = crossed ? "#FFCDD2" : bgCol;
            ctx.strokeStyle = crossed ? "#EF9A9A" : "#D5D8DC";
            ctx.fill(); ctx.stroke();
            
            ctx.font = `${Math.max(8, iconSize-8)}px Arial`;
            ctx.fillText(emoji, cx, cy);
            
            if (crossed) {
                let r = iconSize/2 - 3;
                ctx.strokeStyle = "#C62828"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(cx-r, cy-r); ctx.lineTo(cx+r, cy+r); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(cx+r, cy-r); ctx.lineTo(cx-r, cy+r); ctx.stroke();
            }
        }
    }

    if (op === "+") {
        drawIconBox(a, 10, 10, "#D5F5E3", "#1E8449");
        let opX = 10 + dimA.w + 6;
        drawIconBox(b, opX + 44, 10, "#D6EAF8", "#1A5276");
        
        ctx.fillStyle = "#E67E22";
        ctx.font = "bold 30px Arial";
        ctx.fillText("+", opX + 22, 10 + Math.max(dimA.h, dimB.h)/2);
    } else {
        drawIconBox(a, 10, 10, "#F8F9FA", "#AEB6BF", a - b);
    }
}

function newMathQuestion() {
    mathTheme = MATH_THEMES[Math.floor(Math.random() * MATH_THEMES.length)];
    mathGuessesLeft = 3;
    updateMathLives();
    
    document.getElementById("math-answer-input").disabled = false;
    document.querySelector('.btn-action.check').disabled = false;
    document.getElementById("math-answer-input").value = "";
    document.getElementById("math-answer-input").focus();
    
    const fb = document.getElementById("math-feedback");
    fb.textContent = "";
    fb.className = "feedback";
    
    mathOp = Math.random() < 0.5 ? "+" : "-";
    if (mathOp === "+") {
        mathA = Math.floor(Math.random() * (mathMaxVal + 1));
        mathB = Math.floor(Math.random() * (mathMaxVal - mathA + 1));
        mathAnswer = mathA + mathB;
        document.getElementById("math-question-text").textContent = `${mathA} + ${mathB} = ?`;
        document.getElementById("math-instruction").textContent = "סִפְרוּ אֶת כָּל הַסִּמְלִים יַחַד! 🔢";
    } else {
        mathA = Math.floor(Math.random() * (mathMaxVal + 1));
        mathB = Math.floor(Math.random() * (mathA + 1));
        mathAnswer = mathA - mathB;
        document.getElementById("math-question-text").textContent = `${mathA} − ${mathB} = ?`;
        document.getElementById("math-instruction").textContent = "סִפְרוּ כַּמָּה נִשְׁאַר! 🔢";
    }
    
    drawMathVisual(mathA, mathB, mathOp, mathTheme, mathMaxVal);
}

function checkMathAnswer() {
    if (mathGuessesLeft <= 0) return;
    const inp = document.getElementById("math-answer-input");
    const fb = document.getElementById("math-feedback");
    const raw = inp.value.trim();
    if (raw === "") return;
    
    const userAns = parseInt(raw);
    
    if (userAns === mathAnswer) {
        playSuccessApp();
        fb.textContent = PRAISES[Math.floor(Math.random() * PRAISES.length)];
        fb.className = "feedback success";
        mathGuessesLeft = 0;
        inp.disabled = true;
        document.querySelector('.btn-action.check').disabled = true;
        setTimeout(newMathQuestion, 2000);
    } else {
        mathGuessesLeft--;
        playFailApp();
        shakeApp();
        updateMathLives();
        if (mathGuessesLeft === 0) {
            fb.textContent = `😔 התשובה הנכונה היא: ${mathAnswer}`;
            fb.className = "feedback error";
            inp.disabled = true;
            document.querySelector('.btn-action.check').disabled = true;
            setTimeout(newMathQuestion, 2000);
        } else {
            fb.textContent = TRY_AGAIN[Math.floor(Math.random() * TRY_AGAIN.length)];
            fb.className = "feedback error";
        }
    }
}

document.getElementById("math-answer-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") checkMathAnswer();
});
