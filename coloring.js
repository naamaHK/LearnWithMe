const COLOR_THEMES = [
    { name: "🌊 עולם הים", key: "ocean", color: "#C8F0FF", count: 10 },
    { name: "🦕 דינוזאורים", key: "dinos", color: "#D5F5D5", count: 10 },
    { name: "🚗 כלי רכב", key: "vehicles", color: "#FFF9C4", count: 10 },
    { name: "🦄 חדי קרן", key: "unicorn", color: "#FFF0FA", count: 10 },
    { name: "🌸 מנדלות", key: "mandalas", color: "#F5E6FF", count: 10 },
    { name: "👸 נסיכות", key: "princess", color: "#F3D9F5", count: 10 },
    { name: "🚒 פאו פטרול – יחידת החילוץ", key: "rescue", color: "#FDEBD0", count: 10 },
    { name: "🐶 בלואי ובינגו", key: "bluey", color: "#D6F0FF", count: 10 },
    { name: "🐱 הלו קיטי", key: "hello_kitty", color: "#FADADD", count: 10 },
    { name: "🚀 חלל", key: "space", color: "#D6E4F7", count: 10 },
    { name: "👽 סטיץ׳", key: "stitch", color: "#C5CAE9", count: 14 }
];

const PALETTE = [
    "#FFE4E1", "#FFB6C1", "#FF69B4", "#FF1493", "#FF0000", "#8B0000",
    "#FFE4C4", "#FFDAB9", "#F4A460", "#FF7F50", "#FF8C00", "#D2691E",
    "#8B4513", "#A0522D", "#FFFACD", "#FFFF00", "#FFD700", "#DAA520",
    "#E0FFF0", "#98FB98", "#00FF00", "#32CD32", "#228B22", "#006400",
    "#E0FFFF", "#AFEEEE", "#00FFFF", "#00CED1", "#20B2AA", "#008080",
    "#E6E6FA", "#ADD8E6", "#87CEEB", "#1E90FF", "#0000FF", "#00008B",
    "#D8BFD8", "#DDA0DD", "#EE82EE", "#BA55D3", "#9932CC", "#4B0082",
    "#FFFFFF", "#E0E0E0", "#C0C0C0", "#808080", "#404040", "#000000"
];

let selectedColor = "#FF0000";
let coloringHistory = [];
const MAX_UNDO = 15;
let currentTheme = null;
let currentImagePath = "";

// Initialize Menus
function initColoringMenu() {
    const grid = document.getElementById("coloring-themes-grid");
    grid.innerHTML = "";
    COLOR_THEMES.forEach(t => {
        const btn = document.createElement("button");
        btn.className = "theme-card";
        btn.textContent = t.name;
        btn.style.backgroundColor = t.color;
        btn.onclick = () => openThemePages(t);
        grid.appendChild(btn);
    });
}
initColoringMenu();

function openThemePages(theme) {
    currentTheme = theme;
    document.getElementById("coloring-pages-title").textContent = `${theme.name} — בַּחֲרִי דַּף`;
    const grid = document.getElementById("coloring-pages-grid");
    grid.innerHTML = "";
    
    for (let i = 1; i <= theme.count; i++) {
        const path = `ColoringGame/pages/${theme.key}/${i}.png`;
        const card = document.createElement("div");
        card.className = "page-card";
        
        const img = document.createElement("img");
        img.src = path;
        card.appendChild(img);
        
        const lbl = document.createElement("div");
        lbl.textContent = `דף ${i}`;
        lbl.style.marginTop = "8px";
        lbl.style.fontWeight = "bold";
        card.appendChild(lbl);
        
        card.onclick = () => openColoringCanvas(path);
        grid.appendChild(card);
    }
    
    navigate('view-coloring-pages');
}

// Initialize Palette
function initPalette() {
    const grid = document.getElementById("palette-grid");
    grid.innerHTML = "";
    PALETTE.forEach(c => {
        const div = document.createElement("div");
        div.className = "color-swatch";
        div.style.backgroundColor = c;
        if (c === selectedColor) div.classList.add("active");
        
        div.onclick = () => {
            document.querySelectorAll(".color-swatch").forEach(s => s.classList.remove("active"));
            div.classList.add("active");
            selectedColor = c;
            document.getElementById("currentColorDisplay").style.backgroundColor = selectedColor;
        };
        grid.appendChild(div);
    });
    document.getElementById("currentColorDisplay").style.backgroundColor = selectedColor;
}
initPalette();

function hexToRgba(hex) {
    const r = parseInt(hex.slice(1,3), 16);
    const g = parseInt(hex.slice(3,5), 16);
    const b = parseInt(hex.slice(5,7), 16);
    return [r, g, b, 255];
}

const canvas = document.getElementById("coloringCanvas");
const ctx = canvas.getContext("2d", { willReadFrequently: true });
let originalImageData = null;

function saveState() {
    coloringHistory.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    if (coloringHistory.length > MAX_UNDO) {
        coloringHistory.shift();
    }
}

function openColoringCanvas(imagePath) {
    currentImagePath = imagePath;
    coloringHistory = [];
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = () => {
        const MAX_W = 750, MAX_H = 550;
        let scale = Math.min(MAX_W / img.width, MAX_H / img.height, 1);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        originalImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        
        // Check for saved progress (48 hours)
        const saved = localStorage.getItem(`saved_color_${imagePath}`);
        if (saved) {
            try {
                const data = JSON.parse(saved);
                if (Date.now() - data.t < 48 * 60 * 60 * 1000) {
                    const savedImg = new Image();
                    savedImg.onload = () => {
                        ctx.drawImage(savedImg, 0, 0);
                    };
                    savedImg.src = data.img;
                } else {
                    localStorage.removeItem(`saved_color_${imagePath}`);
                }
            } catch(e) {}
        }
    };
    img.src = imagePath;
    navigate('view-coloring-active');
}

canvas.addEventListener("click", (e) => {
    // Get mouse coordinates
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) * (canvas.width / rect.width));
    const y = Math.floor((e.clientY - rect.top) * (canvas.height / rect.height));
    
    floodFill(x, y, hexToRgba(selectedColor));
});

function floodFill(startX, startY, fillColor) {
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imgData.data;
    const w = canvas.width;
    const h = canvas.height;
    
    const startPos = (startY * w + startX) * 4;
    const startR = data[startPos];
    const startG = data[startPos + 1];
    const startB = data[startPos + 2];
    
    // Don't fill dark lines (brightness < 60)
    if (startR < 60 && startG < 60 && startB < 60) return;
    
    // Don't fill if color is already identical
    if (Math.abs(startR - fillColor[0]) < 5 && 
        Math.abs(startG - fillColor[1]) < 5 && 
        Math.abs(startB - fillColor[2]) < 5) return;
        
    saveState();

    const stack = [[startX, startY]];
    
    function match(p) {
        // Dark line boundary
        if (data[p] < 60 && data[p+1] < 60 && data[p+2] < 60) return false;
        return (Math.abs(data[p] - startR) < 35 && 
                Math.abs(data[p+1] - startG) < 35 && 
                Math.abs(data[p+2] - startB) < 35);
    }
    
    function colorPixel(p) {
        data[p] = fillColor[0];
        data[p+1] = fillColor[1];
        data[p+2] = fillColor[2];
        data[p+3] = 255;
    }
    
    while(stack.length) {
        let [x, y] = stack.pop();
        let p = (y * w + x) * 4;
        
        while(y >= 0 && match(p)) {
            y--;
            p -= w * 4;
        }
        p += w * 4;
        y++;
        
        let reachLeft = false;
        let reachRight = false;
        
        while(y++ < h - 1 && match(p)) {
            colorPixel(p);
            
            if (x > 0) {
                if (match(p - 4)) {
                    if (!reachLeft) {
                        stack.push([x - 1, y]);
                        reachLeft = true;
                    }
                } else if (reachLeft) {
                    reachLeft = false;
                }
            }
            
            if (x < w - 1) {
                if (match(p + 4)) {
                    if (!reachRight) {
                        stack.push([x + 1, y]);
                        reachRight = true;
                    }
                } else if (reachRight) {
                    reachRight = false;
                }
            }
            
            p += w * 4;
        }
    }
    
    ctx.putImageData(imgData, 0, 0);
}

function undoColoring() {
    if (coloringHistory.length > 0) {
        ctx.putImageData(coloringHistory.pop(), 0, 0);
    }
}

function clearColoring() {
    if (originalImageData) {
        saveState();
        ctx.putImageData(originalImageData, 0, 0);
    }
}

function saveProgress() {
    if (!currentImagePath) return;
    const base64 = canvas.toDataURL();
    const data = { t: Date.now(), img: base64 };
    try {
        localStorage.setItem(`saved_color_${currentImagePath}`, JSON.stringify(data));
        const btn = document.getElementById("btn-save-progress");
        const origText = btn.textContent;
        btn.textContent = "✅ נִשְׁמַר!";
        setTimeout(() => btn.textContent = origText, 2500);
    } catch (e) {
        alert("לא ניתן לשמור. ייתכן שנגמר המקום בדפדפן.");
    }
}

function downloadColoring() {
    const link = document.createElement("a");
    link.download = `coloring_${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
}
