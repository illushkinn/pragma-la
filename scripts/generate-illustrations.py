#!/usr/bin/env python3
"""
Genera 4 ilustraciones para las capabilities de Pragma vía Pollinations.ai.
Sin API key, gratis, 100% automático.

Uso:
  python3 scripts/generate-illustrations.py            # genera todo
  python3 scripts/generate-illustrations.py --dry-run  # solo muestra prompts
"""

import argparse
import hashlib
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "images"

CAPABILITIES = [
    {
        "id": "chatbot",
        "name": "Chatbot Clínico",
        "prompt": (
            "Medical chatbot interface illustration, flat vector style, "
            "a doctor avatar talking to a patient avatar with a chat bubble "
            "containing a medical cross, electric blue #0057FF and mind purple accents, "
            "clean minimal design, white background, professional healthcare AI, "
            "simple shapes, no text, 2D flat illustration"
        ),
    },
    {
        "id": "diagnosis",
        "name": "Diagnóstico Diferencial",
        "prompt": (
            "Medical diagnosis network illustration, flat vector style, "
            "a central stethoscope connected to diagnosis nodes, "
            "electric blue #0057FF and mind purple accents, "
            "clean minimal design, white background, AI medical analysis, "
            "simple shapes, no text, 2D flat illustration"
        ),
    },
    {
        "id": "imaging",
        "name": "Análisis de Imágenes",
        "prompt": (
            "Medical imaging analysis illustration, flat vector style, "
            "an X-ray or CT scan image with analysis overlay circles, "
            "electric blue #0057FF and mind purple accents, "
            "clean minimal design, white background, radiology AI, "
            "simple shapes, no text, 2D flat illustration"
        ),
    },
    {
        "id": "literature",
        "name": "Procesamiento de Literatura",
        "prompt": (
            "Medical literature processing illustration, flat vector style, "
            "stack of medical papers and documents with a magnifying glass "
            "and a brain icon representing AI comprehension, "
            "electric blue #0057FF and mind purple accents, "
            "clean minimal design, white background, research AI, "
            "simple shapes, no text, 2D flat illustration"
        ),
    },
]

POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"


def generate_pollinations(prompt: str, seed: int, width: int = 512, height: int = 512) -> bytes | None:
    """Generate image via Pollinations.ai free API."""
    encoded = urllib.parse.quote(prompt)
    url = f"{POLLINATIONS_BASE}/{encoded}?width={width}&height={height}&seed={seed}&model=flux&nofeed=true"
    
    print(f"    ⏳ Generando...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except Exception as e:
        print(f"    ❌ Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate Pragma capability illustrations")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts only, don't generate")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n  🎨 Pragma — 4 capability illustrations")
    print(f"  📁 Output: {OUTPUT_DIR}")
    print()

    for cap in CAPABILITIES:
        filename = f"illustration-{cap['id']}.png"
        filepath = OUTPUT_DIR / filename
        seed = int(hashlib.md5(f"pragma-{cap['id']}".encode()).hexdigest()[:8], 16)

        print(f"  ───────────────────────────────────────────────")
        print(f"  [{cap['id']}] {cap['name']}")
        print(f"  File: {filename}")
        print(f"  Seed: {seed}")

        if args.dry_run:
            print(f"  Prompt: {cap['prompt'][:80]}...")
        else:
            img_data = generate_pollinations(cap["prompt"], seed)
            if img_data:
                with open(filepath, "wb") as f:
                    f.write(img_data)
                size_kb = filepath.stat().st_size / 1024
                print(f"    ✅ {size_kb:.0f} KB — guardado")
            else:
                print(f"    ❌ Falló la generación")

            # Brief pause between requests
            time.sleep(2)

    print(f"\n  {'='*50}")
    print(f"  ✅ Listo")
    if not args.dry_run:
        print(f"  Archivos en: {OUTPUT_DIR}")
    print(f"  {'='*50}")
    print()


if __name__ == "__main__":
    main()
