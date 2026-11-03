# La Mia Gioia — AI Studio Handbag Photo Generator

A standalone, automated batch photoshoot generator for **La Mia Gioia** luxury Italian leather handbags powered by the **Photoroom API**. 

This tool takes raw product photos (taken on a phone, simple white sweep, or casual setting) and automatically places each handbag onto a locked, consistent luxury studio set with a minimalist dark slate podium, atmospheric deep navy/charcoal backdrop, warm champagne spotlights, and realistic contact shadows.

---

## 🌟 Key Features

- **Brand Consistency:** Uses locked `seed`, `negative_prompt`, and `placement` settings so every bag in your collection shares the exact same lighting, studio depth, and podium proportions.
- **Batch Processing:** Drop 5, 20, or 100 bag photos into `raw_bags/` and generate a full collection photoshoot in minutes.
- **Zero Configuration Run:** Double-click `run_generator.bat` on Windows to check dependencies, install requirements, prompt for your API key, and process your catalog.
- **High-End Studio Aesthetics:** Leverages Photoroom's generative AI background engine with AI relighting (`lighting.mode: ai.auto`) and contact shadows (`shadow.mode: ai.soft`).

---

## 📁 Repository Structure

```
la-mia-handbag-studio-generator/
│
├── config.json                 # Studio prompt, negative prompt, seed, & placement settings
├── generate_studio_photos.py   # Python batch processing engine
├── run_generator.bat           # 1-Click Windows launcher
├── requirements.txt            # Python dependencies (requests)
├── .gitignore                  # Ignores photos while preserving folder tracking
├── README.md                   # Documentation & setup guide
│
├── raw_bags/                   # Place your original handbag photos here (.jpg, .png, .webp)
│   └── .gitkeep
│
└── processed_bags/             # Final AI studio photos are exported here
    └── .gitkeep
```

---

## 🚀 Quick Start Guide (Windows)

### 1. Prerequisites
- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/). *Ensure you check **"Add Python to PATH"** during installation.*
- **Photoroom API Key**: Sign up at [photoroom.com/api](https://photoroom.com/api) to get your API key. *(Keys starting with `sandbox_` allow testing for free).*

### 2. Add Your Photos
1. Copy your raw handbag photos into the `raw_bags` folder.
2. Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`.

### 3. Run the Generator
- **Double-click `run_generator.bat`**:
  - The script will automatically verify Python and install dependencies from `requirements.txt`.
  - If `PHOTOROOM_API_KEY` is not set in your Windows environment, the script will prompt you to paste it in.
  - It will process all images in `raw_bags/` one by one.
- **Collect Results**: Open `processed_bags/` to view your final studio photos.

---

## 💻 Manual CLI Usage (Mac / Linux / Windows)

If you prefer running via terminal or on macOS/Linux:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ah107gemi/la-mia-handbag-studio-generator.git
   cd la-mia-handbag-studio-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Photoroom API key:**
   - **Linux / macOS:**
     ```bash
     export PHOTOROOM_API_KEY="your_api_key_here"
     ```
   - **Windows (Command Prompt):**
     ```cmd
     set PHOTOROOM_API_KEY=your_api_key_here
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:PHOTOROOM_API_KEY="your_api_key_here"
     ```

4. **Run the script:**
   ```bash
   python generate_studio_photos.py
   ```

---

## ⚙️ Configuration Reference (`config.json`)

You can customize the studio environment by editing `config.json`:

```json
{
  "prompt": "A high-end luxury leather handbag resting on a sleek, minimalist dark slate podium. The background is a moody, elegant studio setting with deep navy and charcoal tones, featuring subtle, out-of-focus champagne gold geometric accents in the distance. The lighting is cinematic and editorial: warm champagne studio spotlights shining down to highlight the rich texture and stitching of the leather, casting soft, dramatic shadows beneath the bag to create depth. Shot on an 85mm macro lens, photorealistic, 8k resolution, perfectly capturing a premium Italian artisanal brand aesthetic.",
  "negative_prompt": "people, hands, text, logos, cluttered background, bright colors, outdoor, different podium, wood, marble, floating, distorted shadows",
  "seed": 42,
  "placement": {
    "padding": 0.1,
    "alignment": "center"
  }
}
```

### Parameter Details
- **`prompt`**: Describes the scene, podium material, backdrop tones, and lighting style.
- **`negative_prompt`**: Explicitly instructs the AI to prevent unwanted elements (hands, mannequins, cluttered objects, distortion).
- **`seed`**: Integer value (default `42`). Keeps the background scene generation locked so all photos have identical visual continuity.
- **`placement.padding`**: The margin breathing room around the handbag (e.g. `0.1` = 10% canvas padding).
- **`placement.alignment`**: Centers the bag horizontally and vertically on the canvas.

---

## 🛠️ Troubleshooting

- **`[AUTH ERROR] HTTP 401/403`**: Double-check that your `PHOTOROOM_API_KEY` is active and correctly typed without quotes or whitespace.
- **`[PAYMENT ERROR] HTTP 402`**: Your Photoroom account may have run out of API credits. Check your balance in the Photoroom developer portal.
- **`[INFO] No images found in 'raw_bags'`**: Make sure your original photos are placed directly inside `raw_bags/` and end in a supported image extension (`.jpg`, `.jpeg`, `.png`, `.webp`).
- **Python not found**: Ensure Python is added to your system `PATH`. Restart your terminal or command prompt after installing Python.

---

## 📄 License
MIT License. Created for **La Mia Gioia** luxury leather goods.
