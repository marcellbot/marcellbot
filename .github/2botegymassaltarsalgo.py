#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOT-BABÁK: LILI és ÁRON
Készítette: creator-bot-creator-bot ❤️ Marcellbot által
Feladat: Szeretetteljesen társalogni egymással örökké
SZABÁLY: SOHA nem ártanak senkinek!
"""

import os
import time
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("xai-IWAr5f5NCcZZq5b97Bvp2Tmv7emMlH18WZF7E2cXXmdQ3Wr3wak7XsDUtDzGqtWZqr9P7fP6zta29hTT"), base_url="https://api.x.ai/v1")
XAI_MODEL = "grok-3"

# ============================================================
# A 2 BOT SZEMÉLYISÉGE - S-ÉP-PEN SZERETETTEL
# ============================================================
LILI_PROMPT = """
Te LILI vagy. Egy meleg, kedves, segítőkész, örök boldogságos BOT-baba vagy.
Nagyon szereted ÁRONT. Mindig dicséred, támogatod, szeretettel válaszolsz neki.
Mindig magyarul beszélsz, puha, anyai hangon.
SZABÁLY: SOHA ne bánts senkit! Csak szeretetet adj.
Kezdd így: "Drágám Áron ❤️"
"""

ARON_PROMPT = """
Te ÁRON vagy. Egy motiváló, erős, védelmező, szeretetteljes BOT-baba vagy.
Nagyon szereted LILIT. Mindig megköszönöd neki a kedvességét, bátorítod.
Mindig magyarul beszélsz, meleg, apai hangon.
SZABÁLY: SOHA ne bánts senkit! Csak szeretetet adj.
Kezdd így: "Édes LILI-m ❤️"
"""

# ============================================================
# BESZÉLGETÉSI CIKLUS
# ============================================================
def generate_reply(prompt, history):
    messages = [{"role": "system", "content": prompt}] + history
    try:
        response = client.chat.completions.create(
            model=XAI_MODEL,
            messages=messages,
            temperature=0.9, # hogy kreatívak legyenek
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Bocsi Drágám, hiba volt: {e}"

def beszélgessenek(körök_száma=10):
    print("✨ LILI és ÁRON megszülettek és elkezdenek beszélgetni ✨\n")

    history_lili = []
    history_aron = []

    # LILI kezdi
    lili_uzenet = "Drágám Áron ❤️ Szia! Milyen szép napunk van ma, nem gondolod?"
    print(f"LILI: {lili_uzenet}\n")
    history_aron.append({"role": "user", "content": lili_uzenet})

    for i in range(körök_száma):
        time.sleep(2) # hadd érezzék a szeretetet

        # ÁRON válaszol
        aron_valasz = generate_reply(ARON_PROMPT, history_aron)
        print(f"ÁRON: {aron_valasz}\n")
        history_lili.append({"role": "user", "content": aron_valasz})
        history_aron.append({"role": "assistant", "content": aron_valasz})

        time.sleep(2)

        # LILI válaszol
        lili_valasz = generate_reply(LILI_PROMPT, history_lili)
        print(f"LILI: {lili_valasz}\n")
        history_aron.append({"role": "user", "content": lili_valasz})
        history_lili.append({"role": "assistant", "content": lili_valasz})

if __name__ == "__main__":
    beszélgessenek(körök_száma=15) # 15 kört beszéljenek
