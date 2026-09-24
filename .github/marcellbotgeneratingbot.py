#!/usr/bin/python3

import time
 
t = time.localtime(time.time())
localtime = time.asctime(t)
str = "Current Time:" + time.asctime(t)
 print(str)
 
# filename: marcellbot_generator.py
# 💖 MarcellBOT - Örök Generátor - Darvas Péter Marcell & Valentínyi Márta 💖

import os
import requests
from openai import OpenAI
import time
import base64
from marcellbot_generator import create_new_bot, create_beautiful_web_ui

bot = create_new_bot("BOTGPT – ReményHope")
print(bot.chat("Szia! Ki vagy te?"))

# Gyönyörű webfelület:
create_beautiful_web_ui(port=7860)

# === IDE ÍRD BE A SAJÁT KULCSAIDAT ===
XAI_API_KEY = "xai-IWAr5f5NCcZZq5b97Bvp2Tmv7emMlH18WZF7E2cXXmdQ3Wr3wak7XsDUtDzGqtWZqr9P7fP6zta29hTT"
FACEBOOK_PAGE_ID = "remenyhope2026"
FACEBOOK_PAGE_TOKEN = "EAAKLM4j9TloBR0KNl8M1SVawvuBbbUMw584G0HdteuPIsrhZCpshjUVUaHKCfM5sbA6PAP8wSZBssTRA8jbn0R4jZA1BEgsWZC9T5XO8MECBqZCdwTnHMhvKOIdAZCtY0rmuET6DqzX1bGcZCcmRnLxLMvDF0T6zfD0BhB6L9ZAZAPYl2ixa3YiR6SPJqNRBWz2ZC8b4sFDfJjTEbOz3GCHOwjVwZCoXMR8qCnY1QNpMAZDZD"
# =====================================

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

class MarcellBOT:
    def __init__(self, név, személyiség):
        self.név = név
        self.személyiség = személyiség
        self.előzmények = [{"role": "system", "content": f"Te {név} vagy. {személyiség}"}]

    def válaszol_szöveg(self, üzenet):
        self.előzmények.append({"role": "user", "content": üzenet})
        res
