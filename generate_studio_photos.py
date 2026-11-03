"""
La Mia Gioia - AI Studio Photo Generator
Uses the Photoroom API (v2 Edit endpoint) to generate high-end, editorial
studio backgrounds for handbag catalog photos with locked parameters.
"""

import json
import mimetypes
import os
import sys
import time
from pathlib import Path
import requests

# Constants
API_ENDPOINT = "https://image-api.photoroom.com/v2/edit"
CONFIG_FILE = "config.json"
RAW_DIR = Path("raw_bags")
PROCESSED_DIR = Path("processed_bags")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def load_config() -> dict:
    """Load studio generation parameters from config.json."""
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        print(f"[ERROR] Configuration file '{CONFIG_FILE}' not found!")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse '{CONFIG_FILE}': {e}")
        sys.exit(1)


def get_api_key() -> str:
    """Retrieve Photoroom API key from environment variable."""
    api_key = os.getenv("PHOTOROOM_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] Environment variable 'PHOTOROOM_API_KEY' is missing or empty.")
        print("Please set your Photoroom API key before running this script:")
        print("  Windows (CMD):  set PHOTOROOM_API_KEY=your_api_key_here")
        print("  Windows (PS):   $env:PHOTOROOM_API_KEY=\"your_api_key_here\"")
        print("  Or run via:     run_generator.bat")
        print("Get your API key at: https://photoroom.com/api")
        sys.exit(1)
    return api_key


def process_image(image_path: Path, config: dict, api_key: str) -> bool:
    """
    Send raw handbag image to Photoroom v2 API and save the processed studio photo.
    """
    prompt = config.get("prompt", "")
    negative_prompt = config.get("negative_prompt", "")
    seed = config.get("seed", 42)
    placement = config.get("placement", {})
    padding = placement.get("padding", 0.1)
    alignment = placement.get("alignment", "center")

    output_path = PROCESSED_DIR / image_path.name

    headers = {
        "x-api-key": api_key,
        "pr-ai-background-model-version": "background-studio-beta-2025-03-17",
    }

    form_data = {
        "background.prompt": prompt,
        "background.negativePrompt": negative_prompt,
        "background.seed": str(seed),
        "shadow.mode": "ai.soft",
        "lighting.mode": "ai.auto",
        "padding": str(padding),
        "horizontalAlignment": "center" if alignment == "center" else alignment,
        "verticalAlignment": "center" if alignment == "center" else alignment,
    }

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type:
        mime_type = "image/jpeg"

    try:
        with open(image_path, "rb") as img_file:
            files = {
                "imageFile": (image_path.name, img_file, mime_type),
            }

            response = requests.post(
                API_ENDPOINT,
                headers=headers,
                data=form_data,
                files=files,
                timeout=120,
            )

        if response.status_code == 200:
            with open(output_path, "wb") as out_file:
                out_file.write(response.content)
            size_kb = len(response.content) / 1024
            print(f"    [SUCCESS] Saved to {output_path} ({size_kb:.1f} KB)")
            return True

        # Error handling based on response code
        if response.status_code == 401 or response.status_code == 403:
            print(f"    [AUTH ERROR] HTTP {response.status_code}: Invalid or unauthorized Photoroom API key.")
        elif response.status_code == 402:
            print(f"    [PAYMENT ERROR] HTTP {response.status_code}: Insufficient credits on your Photoroom account.")
        elif response.status_code == 429:
            print(f"    [RATE LIMIT] HTTP {response.status_code}: Too many requests. Please slow down and retry.")
        else:
            try:
                err_detail = response.json()
            except Exception:
                err_detail = response.text
            print(f"    [API ERROR] HTTP {response.status_code}: {err_detail}")

        return False

    except requests.exceptions.Timeout:
        print(f"    [TIMEOUT ERROR] Request timed out while processing {image_path.name}.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"    [NETWORK ERROR] Failed to connect to Photoroom API: {e}")
        return False
    except Exception as e:
        print(f"    [ERROR] Unexpected error processing {image_path.name}: {e}")
        return False


def main():
    print("=" * 64)
    print("      LA MIA GIOIA - AI STUDIO PHOTO GENERATOR")
    print("=" * 64)
    print()

    # 1. Initialize environment & config
    api_key = get_api_key()
    config = load_config()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Collect raw images
    all_files = [p for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    all_files.sort(key=lambda p: p.name.lower())

    if not all_files:
        print(f"[INFO] No images found in '{RAW_DIR}'.")
        print(f"Please place your raw handbag photos (.jpg, .png, .webp) inside '{RAW_DIR}' and re-run.")
        print()
        sys.exit(0)

    total_images = len(all_files)
    print(f"[INFO] Found {total_images} raw image(s) to process in '{RAW_DIR}'.")
    print(f"[INFO] Using locked seed: {config.get('seed', 42)}")
    print(f"[INFO] Output folder: '{PROCESSED_DIR}'")
    print("-" * 64)
    print()

    success_count = 0
    fail_count = 0
    start_time = time.time()

    for idx, image_path in enumerate(all_files, start=1):
        print(f"[{idx}/{total_images}] Generating studio setting for: {image_path.name}...")
        ok = process_image(image_path, config, api_key)
        if ok:
            success_count += 1
        else:
            fail_count += 1

        # Small pause between API calls to avoid rate limiting
        if idx < total_images:
            time.sleep(1.0)

    elapsed = time.time() - start_time
    print()
    print("=" * 64)
    print("                  PROCESSING SUMMARY")
    print("=" * 64)
    print(f"  Total Images Processed: {total_images}")
    print(f"  Successful:             {success_count}")
    print(f"  Failed:                 {fail_count}")
    print(f"  Total Time:             {elapsed:.1f} seconds")
    print(f"  Processed Folder:       {PROCESSED_DIR.resolve()}")
    print("=" * 64)
    print()

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
