const COLOR_THEMES = [
    { name: "🌊 עולם הים", key: "ocean", color: "#C8F0FF", count: 3 },
    { name: "🦕 דינוזאורים", key: "dinos", color: "#D5F5D5", count: 10 },
    { name: "🚗 כלי רכב", key: "vehicles", color: "#FFF9C4", count: 3 },
    { name: "🦄 חדי קרן", key: "unicorn", color: "#FFF0FA", count: 3 },
    { name: "🌸 מנדלות", key: "mandalas", color: "#F5E6FF", count: 10 },
    { name: "👸 נסיכות", key: "princess", color: "#F3D9F5", count: 10 },
    { name: "🚒 פאו פטרול – יחידת החילוץ", key: "rescue", color: "#FDEBD0", count: 3 },
    { name: "🐶 בלואי ובינגו", key: "bluey", color: "#D6F0FF", count: 4 },
    { name: "🐱 הלו קיטי", key: "hello_kitty", color: "#FADADD", count: 3 },
    { name: "🚀 חלל", key: "space", color: "#D6E4F7", count: 3 },
    { name: "👽 סטיץ׳", key: "stitch", color: "#C5CAE9", count: 4 }
];

const PALETTE = [
    "#FF0000", "#FF6600", "#FFEA00", "#C8FF00",
    "#00CC44", "#00AAFF", "#0000EE", "#6600CC",
    "#FF00FF", "#FF0077", "#FF99CC", "#FFCCAA",
    "#FF3333", "#FF9900", "#88FF00", "#00FFCC",
    "#FF69B4", "#663300", "#CC8800", "#FFD700",
    "#FFFFFF", "#BBBBBB", "#555555", "#000000"
];

let selectedColor = "#FF0000";
let coloringHistory = [];
const MAX_UNDO = 15;
let currentTheme = null;

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
    coloringHistory = [];
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = () => {
        // scale to fit nicely
        const MAX_W = 750, MAX_H = 550;
        let scale = Math.min(MAX_W / img.width, MAX_H / img.height, 1);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        originalImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
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

function saveColoring() {
    const link = document.createElement("a");
    link.download = `coloring_${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
}
