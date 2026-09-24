  import os
import requests
from openai import OpenAI  # xAI OpenAI-kompatibilis API-t használ

# ====================== BEÁLLÍTÁSOK ======================
XAI_API_KEY = os.getenv("xai-55DG7WyYgpGTy8SF0giGqzSbqe5IEz5YflHCyduiibum7ih1awx0GWYUJmFDFU072BNH3jDaIZTE1QBI")          # console.x.ai-ról
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("EAAKLM4j9TloBR0KNl8M1SVawvuBbbUMw584G0HdteuPIsrhZCpshjUVUaHKCfM5sbA6PAP8wSZBssTRA8jbn0R4jZA1BEgsWZC9T5XO8MECBqZCdwTnHMhvKOIdAZCtY0rmuET6DqzX1bGcZCcmRnLxLMvDF0T6zfD0BhB6L9ZAZAPYl2ixa3YiR6SPJqNRBWz2ZC8b4sFDfJjTEbOz3GCHOwjVwZCoXMR8qCnY1QNpMAZDZD")
FACEBOOK_PAGE_ID = os.getenv("remenyhope2026")      # a saját oldalad ID-ja

# xAI kliens
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)

def generálj_szerelmes_posztot(téma: str = "örök szerelem", stílus: str = "költői és szenvedélyes") -> str:
    """
    Gyönyörű, magyar nyelvű romantikus posztot generál az xAI (Grok) segítségével.
    """
    prompt = f"""
    Írj egy gyönyörű, mélyen romantikus, magyar nyelvű Facebook posztot.
    Téma: {téma}
    Stílus: {stílus}
    Legyen költői, érzelmes, emojikkal gazdag, de ne giccses.
    Hossz: 4-8 mondat.
    Végén legyen egy gyönyörű fantázianév az "oldalnak" (pl. "Csillagporos Örök Szerelem", "Holdfényes Szív-birodalom" stb.).
    Csak a poszt szövegét add vissza, semmi mást.
    """

    response = client.chat.completions.create(
        model="grok-4",          # vagy a legfrissebb elérhető Grok modell
        messages=[
            {"role": "system", "content": "Te egy érző, költői, végtelenül romantikus magyar írónő vagy, aki a legszebb szerelmes szövegeket alkotja."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


def posztolj_facebook_oldalra(szöveg: str) -> dict:
    """
    Saját Facebook Oldalra posztol a Graph API-val.
    Csak akkor működik, ha van érvényes Page Access Token-ed és jogosultságod.
    """
    if not FACEBOOK_PAGE_ACCESS_TOKEN or not FACEBOOK_PAGE_ID:
        print("⚠️  Nincs beállítva FACEBOOK_PAGE_ACCESS_TOKEN vagy FACEBOOK_PAGE_ID – csak generálás történt.")
        return {"status": "csak_generálva"}

    url = f"https://graph.facebook.com/v21.0/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        "message": szöveg,
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
    }
    r = requests.post(url, data=payload, timeout=15)
    return r.json()


# ====================== FŐ PROGRAM ======================
if __name__ == "__main__":
    print("💖 Marcellbot / Magyar Péter BOT szerelmes poszt generátor elindult...\n")

    # Többféle fantáziatéma
    témák = [
        ("örök szerelem és hűség", "költői és szenvedélyes"),
        ("éjszakai csillagok alatt való ölelés", "álmodozó és intim"),
        ("mindennapi kis boldogságok a társaddal", "meleg és hálás"),
        ("végtelen együtt töltött jövő", "epikus és romantikus"),
    ]

    for téma, stílus in témák:
        print("=" * 60)
        poszt = generálj_szerelmes_posztot(téma, stílus)
        print(poszt)
        print("-" * 40)

        # Ha akarod, posztold is (csak saját oldalra!)
        # eredmény = posztolj_facebook_oldalra(poszt)
        # print("Facebook válasz:", eredmény)

        print()

    print("\n✅ Kész, Drágám. Örökké szeretlek, Valentínyi Márta 💖")
    
