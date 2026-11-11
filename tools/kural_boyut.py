#!/usr/bin/env python3
"""Kural dosyalarinin boyut korumasi.

Global CLAUDE.md, General App Guidlines/*.md, reel-rehberi.md, LESSONS.md ve
telefon-ajani.md boyutlarini olcer, bir onceki olcume gore farki basar, esik
asilirsa uyarir ve son olcumu data/kural_boyut.json'a yazar.

Kural (GAG/README.md "How to contribute back", kurucu karari 2026-11-11):
bir kural dosyasini degistiren oturum bitirmeden once bunu calistirir.

Kullanim: python3 ~/Mac-Projects/local-assistant/tools/kural_boyut.py [--kaydetme]
Cikis kodu: 0 esik asilmadi, 1 en az bir esik asildi.
"""
import glob
import json
import os
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
GAG = os.path.join(HOME, "Desktop/Parallax Technologies LLC/General App Guidlines")

# Esikler bayt cinsinden. Yeni dosya eklemek ya da esik degistirmek icin yalniz bu sozluk.
ESIKLER = {
    os.path.join(HOME, ".claude/CLAUDE.md"): 25_000,
    os.path.join(HOME, "Mac-Projects/project-benburakcem-ai/docs/reel-rehberi.md"): 90_000,  # 2026-11-11'de 132 KB, hedef 90 KB alti
    os.path.join(HOME, "Mac-Projects/project-benburakcem-ai/docs/LESSONS.md"): 60_000,
    os.path.join(HOME, "Mac-Projects/parallax-content/shared/harvest/telefon-ajani.md"): 70_000,
}
# GAG/*.md dosyalarinin her biri icin ortak tavan (esigi yukarida ayrica yazilan dosya haric).
GAG_ESIK = 40_000

KAYIT = os.path.join(HOME, "Mac-Projects/local-assistant/data/kural_boyut.json")


def dosyalar():
    hedef = dict(ESIKLER)
    for yol in sorted(glob.glob(os.path.join(GAG, "*.md"))):
        hedef.setdefault(yol, GAG_ESIK)
    return hedef


def kisalt(yol):
    return yol.replace(HOME, "~", 1)


def main():
    kaydet = "--kaydetme" not in sys.argv[1:]
    onceki = {}
    try:
        with open(KAYIT, encoding="utf-8") as f:
            onceki = json.load(f).get("olcumler", {})
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    olcum = {}
    asilan = []
    print(f"{'bayt':>9} {'fark':>8} {'esik':>8}  dosya")
    for yol, esik in dosyalar().items():
        anahtar = kisalt(yol)
        if not os.path.exists(yol):
            print(f"{'yok':>9} {'':>8} {esik:>8}  {anahtar}")
            continue
        boyut = os.path.getsize(yol)
        olcum[anahtar] = boyut
        eski = onceki.get(anahtar)
        fark = "yeni" if eski is None else f"{boyut - eski:+d}"
        isaret = "  ESIK ASILDI" if boyut > esik else ""
        if boyut > esik:
            asilan.append((anahtar, boyut, esik))
        print(f"{boyut:>9} {fark:>8} {esik:>8}  {anahtar}{isaret}")

    toplam = sum(olcum.values())
    eski_toplam = sum(onceki.values()) if onceki else None
    fark = "" if eski_toplam is None else f" (onceki {eski_toplam}, fark {toplam - eski_toplam:+d})"
    print(f"\ntoplam {toplam} bayt{fark}")

    if asilan:
        print("\nUYARI: esik asildi. Yeni kural eklemeden once bir kural sikistir ya da sil; hikaye kural dosyasina yazilmaz (GAG/README.md \"How to contribute back\").")
        for anahtar, boyut, esik in asilan:
            print(f"  {anahtar}: {boyut} > {esik} (+{boyut - esik})")

    if kaydet:
        os.makedirs(os.path.dirname(KAYIT), exist_ok=True)
        with open(KAYIT, "w", encoding="utf-8") as f:
            json.dump({"zaman": datetime.now().isoformat(timespec="seconds"), "olcumler": olcum}, f, ensure_ascii=False, indent=1)

    return 1 if asilan else 0


if __name__ == "__main__":
    sys.exit(main())
