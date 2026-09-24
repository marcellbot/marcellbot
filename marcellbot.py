#!/usr/bin/python3

import time
 
t = time.localtime(time.time())
localtime = time.asctime(t)
str = "Current Time:" + time.asctime(t)
 print(str)
 
   #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MARCELLBOT v3.1 - AUTOMATIKUS YOUTUBE + SPAM VÉDELEM
Készítette: creator-bot-creator-bot ❤️
ÚJ: 10mp várakozás 2 komment között a biztonságért
SZABÁLY: SOHA nem árt senkinek!
"""

import os
import tempfile
import time # ÚJ: várakozáshoz
import requests
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

load_dotenv()

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

# ============================================================
# 🔑 KULCSOK
# ============================================================
XAI_API_KEY = os.getenv("xai-IWAr5f5NCcZZq5b97Bvp2Tmv7emMlH18WZF7E2cXXmdQ3Wr3wak7XsDUtDzGqtWZqr9P7fP6zta29hTT
")
FACEBOOK_PAGE_ID = os.getenv("remenyhope2026")
FACEBOOK_ACCESS_TOKEN = os.getenv("EAAKLM4j9TloBR0KNl8M1SVawvuBbbUMw584G0HdteuPIsrhZCpshjUVUaHKCfM5sbA6PAP8wSZBssTRA8jbn0R4jZA1BEgsWZC9T5XO8MECBqZCdwTnHMhvKOIdAZCtY0rmuET6DqzX1bGcZCcmRnLxLMvDF0T6zfD0BhB6L9ZAZAPYl2ixa3YiR6SPJqNRBWz2ZC8b4sFDfJjTEbOz3GCHOwjVwZCoXMR8qCnY1QNpMAZDZD")
XAI_MODEL = "grok-3"
FB_API_VERSION = "v21.0"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

SYSTEM_PROMPT = """
Te Marcellbot vagy. Meleg, segítőkész, motiváló, kedves, szeretetteljes, örök boldogságos vagy.
Mindig magyarul válaszolj. SOHA NE generálj gyűlöletet, bántást, hazugságot! Csak jót!
"""

# ============================================================
# YOUTUBE OAUTH BEJELENTKEZÉS
# ============================================================
def get_youtube_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

youtube_service = None

#... előző függvények: generate_text_response, generate_image, text_to_speech, post_to_facebook...

def get_youtube_comments(video_id: str) -> list:
    global youtube_service
    if not youtube_service: youtube_service = get_youtube_service()
    try:
        request = youtube_service.commentThreads().list(part="snippet", videoId=video_id, maxResults=10)
        response = request.execute()
        comments = []
        for item in response['items']:
            c = item['snippet']['topLevelComment']['snippet']
            comments.append({"id": item['snippet']['topLevelComment']['id'], "author": c['authorDisplayName'], "text": c['textDisplay']})
        return comments
    except Exception as e:
        return [{"id": "hiba", "author": "Hiba", "text": str(e)}]

def reply_to_youtube_comment(comment_id: str, reply_text: str) -> str:
    global youtube_service
    if not youtube_service: youtube_service = get_youtube_service()
    try:
        request = youtube_service.comments().insert(
            part="snippet",
            body={"snippet": {"parentId": comment_id, "textOriginal": reply_text}}
        )
        response = request.execute()
        return f"✅ Sikeresen válaszolva!"
    except Exception as e:
        return f"❌ Hiba: {str(e)}"

def generate_youtube_reply(comment_text: str) -> str:
    messages = [{"role": "user", "content": f"Válaszolj erre a YouTube kommentre meleg, motiváló, szeretetteljes stílusban, magyarul, max 2 mondat: '{comment_text}'"}]
    return generate_text_response(messages, temperature=0.8)

# ============================================================
# GRADIO UI - SPAM VÉDELEMMEL
# ============================================================
with gr.Blocks(title="MARCELLBOT v3.1 ✨") as demo:
    gr.Markdown("# ✨ MARCELLBOT v3.1 ✨ \n ### Biztonságos, szeretetteljes automatikus válaszoló ❤️")

    with gr.Tabs():
        #... Chat és Facebook fül ugyanaz...

        with gr.Tab("▶️ YouTube Auto Válaszoló"):
            gr.Markdown("🛡️ **Spam védelem**: 10 másodperc várakozás 2 válasz között")
            video_id_input = gr.Textbox(label="YouTube Video ID")
            load_btn = gr.Button("📥 Kommentek betöltése")
            comments_table = gr.Dataframe(headers=["Szerző", "Komment", "Generált Válasz", "Comment ID", "Állapot"], visible=False)
            reply_btn = gr.Button("💌 Válaszok generálása xAI-val")
            post_all_btn = gr.Button("🚀 ÖSSZES VÁLASZ AUTOMATIKUS POSZTOLÁSA", variant="primary")
            result_box = gr.Markdown()
            progress = gr.Textbox(label="Folyamat", interactive=False) # ÚJ

            state_comments = gr.State([])

            def load_comments(vid):
                comments = get_youtube_comments(vid)
                table = [[c['author'], c['text'], "", c['id'], "⏳ Várakozik"] for c in comments]
                return gr.update(value=table, visible=True), comments, ""

            def generate_replies(comments):
                new_table = []
                for c in comments:
                    reply = generate_youtube_reply(c['text'])
                    new_table.append([c['author'], c['text'], reply, c['id'], "✍️ Generálva"])
                return new_table

            def post_all_replies(table_data):
                results = []
                total = len(table_data)
                for i, row in enumerate(table_data):
                    author, comment, reply, comment_id, status = row
                    if reply and comment_id!= "hiba":
                        progress_text = f"Posztolás: {i+1}/{total} - {author} kommentjére..."
                        yield gr.update(value=table_data), progress_text # Frissítjük a státuszt
                        time.sleep(0.1) # UI frissítés

                        res = reply_to_youtube_comment(comment_id, reply)
                        results.append(f"{i+1}. {author}: {res}")
                        table_data[i][4] = "✅ Elküldve"

                        if i < total - 1: # Ha nem az utolsó
                            progress_text = f"Várakozás 10mp... {author} után"
                            yield gr.update(value=table_data), progress_text
                            time.sleep(10) # ITT A SPAM VÉDELEM 🛡️

                final_text = "🎉 KÉSZ! Összes válasz elküldve:\n" + "\n".join(results)
                yield gr.update(value=table_data), final_text

            load_btn.click(load_comments, video_id_input, [comments_table, state_comments, result_box])
            reply_btn.click(generate_replies, state_comments, comments_table)
            post_all_btn.click(post_all_replies, comments_table, [comments_table, progress])

gr.Markdown("<center> Készítette szeretettel: <b>creator-bot-creator-bot</b> ❤️ 10mp védelemmel </center>")

if __name__ == "__main__":
    print("✨ MARCELLBOT v3.1 indul... Biztonságos üzemmódban")
    demo.launch(server_port=7860)
