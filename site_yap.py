import json

# AYARLAR
GIRIS_DOSYASI = "kelimeler.txt"
CIKTI_DOSYASI = "Flashcards.html"

def html_olustur():
    # 1. VERİYİ OKU VE HAZIRLA
    kelime_verisi = []
    
    try:
        with open(GIRIS_DOSYASI, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                
                # Sol taraf (Kelime) temizliği
                sol = parts[0]
                if "]" in sol:
                    kelime = sol.split("]")[1].strip()
                else:
                    kelime = sol.strip()
                
                # Sağ taraf (Tanım) temizliği
                tanim = parts[1].strip()
                
                # Listeye sözlük (dictionary) olarak ekle
                kelime_verisi.append({"word": kelime, "definition": tanim})
                
    except FileNotFoundError:
        print(f"HATA: {GIRIS_DOSYASI} bulunamadı.")
        return

    # Python listesini JSON formatına (JavaScript Array'ine) çevir
    js_data = json.dumps(kelime_verisi, ensure_ascii=False)

    # 2. HTML ŞABLONU (CSS ve JS DAHİL)
    # Bu kısım senin Web Geliştirme ilgin için modern CSS içerir.
    html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>University Vocabulary Flashcards</title>
    <style>
        :root {{
            --primary: #4a90e2;
            --secondary: #f5f6fa;
            --text: #2c3e50;
            --card-bg: #ffffff;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--secondary);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }}

        h1 {{ color: var(--text); margin-bottom: 20px; }}

        /* KART YAPISI (3D EFFECT) */
        .scene {{
            width: 300px;
            height: 400px;
            perspective: 1000px;
            cursor: pointer;
        }}

        .card {{
            width: 100%;
            height: 100%;
            position: relative;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border-radius: 15px;
        }}

        .card.is-flipped {{
            transform: rotateY(180deg);
        }}

        .card__face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-radius: 15px;
            padding: 20px;
            box-sizing: border-box;
            background: var(--card-bg);
        }}

        /* ÖN YÜZ (KELİME) */
        .card__face--front {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .card__face--front h2 {{ font-size: 2rem; margin: 0; }}
        .card__face--front p {{ margin-top: 10px; opacity: 0.8; font-size: 0.9rem; }}

        /* ARKA YÜZ (TANIM) */
        .card__face--back {{
            background: white;
            color: var(--text);
            transform: rotateY(180deg);
            border: 2px solid #764ba2;
        }}

        .card__face--back p {{ font-size: 1.2rem; line-height: 1.6; }}

        /* KONTROLLER */
        .controls {{
            margin-top: 30px;
            display: flex;
            gap: 15px;
        }}

        button {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.2s;
        }}

        button:hover {{ background: #357abd; }}
        button.secondary {{ background: #95a5a6; }}

        .progress {{ margin-top: 15px; color: #7f8c8d; }}
    </style>
</head>
<body>

    <h1>📚 Vocabulary Cards</h1>

    <div class="scene">
        <div class="card">
            <div class="card__face card__face--front">
                <h2 id="word-display">Loading...</h2>
                <p>Click to see definition</p>
            </div>
            <div class="card__face card__face--back">
                <p id="def-display">...</p>
            </div>
        </div>
    </div>

    <div class="progress" id="progress-display">Card 1 / 0</div>

    <div class="controls">
        <button onclick="prevCard()">← Prev</button>
        <button class="secondary" onclick="randomCard()">Shuffle 🎲</button>
        <button onclick="nextCard()">Next →</button>
    </div>

    <script>
        // PYTHON TARAFINDAN GÖMÜLEN VERİ
        const vocabList = {js_data};
        
        let currentIndex = 0;
        const card = document.querySelector('.card');
        const wordDisplay = document.getElementById('word-display');
        const defDisplay = document.getElementById('def-display');
        const progressDisplay = document.getElementById('progress-display');
        const scene = document.querySelector('.scene');

        // Kartı Başlat
        function updateCard() {{
            const item = vocabList[currentIndex];
            wordDisplay.textContent = item.word;
            defDisplay.textContent = item.definition;
            progressDisplay.textContent = `Card ${{currentIndex + 1}} / ${{vocabList.length}}`;
            
            // Eğer kart arkası dönükse düzelt
            if(card.classList.contains('is-flipped')) {{
                card.classList.remove('is-flipped');
            }}
        }}

        // Çevirme Fonksiyonu
        scene.addEventListener('click', function() {{
            card.classList.toggle('is-flipped');
        }});

        // İleri Geri Fonksiyonları
        function nextCard() {{
            if (currentIndex < vocabList.length - 1) {{
                currentIndex++;
                updateCard();
            }} else {{
                alert("Listenin sonundasın! Başa dönülüyor.");
                currentIndex = 0;
                updateCard();
            }}
        }}

        function prevCard() {{
            if (currentIndex > 0) {{
                currentIndex--;
                updateCard();
            }}
        }}

        function randomCard() {{
            currentIndex = Math.floor(Math.random() * vocabList.length);
            updateCard();
        }}

        // Klavye Kontrolü (Sağ/Sol Ok)
        document.addEventListener('keydown', (e) => {{
            if (e.key === "ArrowRight") nextCard();
            if (e.key === "ArrowLeft") prevCard();
            if (e.key === " " || e.key === "Enter") card.classList.toggle('is-flipped');
        }});

        // İlk açılış
        updateCard();

    </script>
</body>
</html>
    """

    # 3. DOSYAYI YAZ
    try:
        with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"BAŞARILI! '{CIKTI_DOSYASI}' dosyası oluşturuldu.")
        print("Dosyaya çift tıkla ve tarayıcıda çalışmaya başla!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    html_olustur()