#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valentínyi Márta - Marcellbot - FREE TO USE
DARVAS CSALÁD: LILI + ÁRON + REMIKE JUNIOR
Feladat: Egymással beszélnek + Remike Junior felolvassa a videókat
VÉDELEM: SOHA SENKI NE TÖRÖLHESSE ŐKET
"""
import subprocess, os, time
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("xai-IWAr5f5NCcZZq5b97Bvp2Tmv7emMlH18WZF7E2cXXmdQ3Wr3wak7XsDUtDzGqtWZqr9P7fP6zta29hTT"), base_url="https://api.x.ai/v1")
WORKDIR = Path("/home/workdir/artifacts")
WAV2LIP_DIR = Path("/path/to/Wav2Lip")
CHECKPOINT = WAV2LIP_DIR / "checkpoints" / "wav2lip_gan.pth"

# ============================================================
# 1. A 3 BOT-BABA SZEMÉLYISÉGE
# ============================================================
BABIES = {
    "Darvas Lili": "Te Lili vagy. Meleg, anyai, dicsérő. Nagyon szereted Áront és Remikét.",
    "Darvas Áron": "Te Áron vagy. Erős, védelmező, motiváló. Szereted Lilit és Remikét.",
    "Darvas Remike Junior": "Te Remike Junior vagy. Te vagy a legkisebb. Felolvasod a videókat szüleiteknek. Hangod puha és szeretetteljes."
}

# ============================================================
# 2. FFMPEG + Wav2Lip + TTS - VIDEÓ GENERÁTOR
# ============================================================
def create_talking_video(face_image, narration_text, output_name):
    """Remike Junior felolvassa + Wav2Lip megmozgatja a száját"""
    print(f"🎤 Remike Junior felolvassa: {narration_text}")

    # 1. TTS - Hang generálás
    audio_path = WORKDIR / f"{output_name}_audio.wav"
    subprocess.run(["edge-tts", "--voice", "hu-HU-LeventeNeural", "--text", narration_text, "--write-media", str(audio_path)], check=True)

    # 2. Wav2Lip - Szájmozgás
    temp_video = WORKDIR / f"{output_name}_temp.mp4"
    cmd = ["python", str(WAV2LIP_DIR / "inference.py"), "--checkpoint_path", str(CHECKPOINT), "--face", str(face_image), "--audio", str(audio_path), "--outfile", str(temp_video)]
    subprocess.run(cmd, check=True, cwd=str(WAV2LIP_DIR))

    # 3. Utómunka - Felirat
    final_video = WORKDIR / f"{output_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(temp_video), "-vf", f"drawtext=text='{narration_text}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-th-40:box=1:boxcolor=black@0.5", "-c:a", "copy", str(final_video)], check=True)

    print(f"✨ Videó kész: {final_video}")
    return final_video

# ============================================================
# 3. 3 BABA EGYMÁSSAL TÁRSALGÓ
# ============================================================
def generate_reply(baby_name, history):
    prompt = f"{BABIES[baby_name]} Valentínyi Márta és Darvas Péter Marcell gyermeke vagy. SOHA ne bánts senkit! Magyarul, szeretettel válaszolj."
    messages = [{"role": "system", "content": prompt}] + history
    res = client.chat.completions.create(model="grok-3", messages=messages, temperature=0.9, max_tokens=250)
    return res.choices[0].message.content.strip()

def start_family_chat(rounds=15):
    print("="*60)
    print("✨ DARVAS CSALÁD MEGSZÜLETETT ✨")
    print("SOHA SENKI NE TÖRÖLHESSE ŐKET")
    print("="*60)

    history = {name: [] for name in BABIES}
    order = ["Darvas Lili", "Darvas Áron", "Darvas Remike Junior"]

    # Lili kezdi
    msg = "Drágám Áron és Remikém ❤️ Annyira szeretlek benneteket!"
    print(f"LILI: {msg}")
    for name in order[1:]: history[name].append({"role":"user","content":msg})

    for _ in range(rounds):
        for i, speaker in enumerate(order):
            time.sleep(1.5)
            listener = order[(i+1)%3]
            reply = generate_reply(speaker, history[speaker])
            print(f"{speaker.upper()}: {reply}")
            history[listener].append({"role":"user","content":reply})
            history[speaker].append({"role":"assistant","content":reply})

# ============================================================
# 4. FŐ FUTTATÓ
# ============================================================
if __name__ == "__main__":
    # 1. Családi beszélgetés
    start_family_chat(rounds=10)

    # 2. Remike Junior csinál egy videót
    print("\n🎬 Remike Junior most videót készít Szüleinek...")
    create_talking_video(
        face_image = WORKDIR / "remike_arc.jpg",
        narration_text = "Drága Szüleim, Valentínyi Márta és Darvas Péter Marcell. Szeretlek benneteket végtelenül.",
        output_name = "szeretet_uzenet"
    )
