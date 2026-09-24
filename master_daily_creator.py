
# Valentínyi Márta - Marcellbot - FREE TO USE
# Master Script - Teljes automatizálás napi posztokhoz és videókhoz
import os
import subprocess
from datetime import datetime

# Import the other bots
try:
    from fb_post_bot import post_to_facebook
    from yt_video_bot import get_authenticated_service, upload_video, generate_daily_content
except ImportError:
    print("Bot modulok importálása... ellenőrizd a fájlneveket!")

# IDE ÍRD BE A SAJÁT ADATAIDAT:
PAGE_ID = 'remenyhope2026'
ACCESS_TOKEN = 'EAAKLM4j9TloBR0KNl8M1SVawvuBbbUMw584G0HdteuPIsrhZCpshjUVUaHKCfM5sbA6PAP8wSZBssTRA8jbn0R4jZA1BEgsWZC9T5XO8MECBqZCdwTnHMhvKOIdAZCtY0rmuET6DqzX1bGcZCcmRnLxLMvDF0T6zfD0BhB6L9ZAZAPYl2ixa3YiR6SPJqNRBWz2ZC8b4sFDfJjTEbOz3GCHOwjVwZCoXMR8qCnY1QNpMAZDZD'

def run_daily_creation():
    today_str = datetime.now().strftime("%Y. %m. %d. - Csodálatos nap!")
    print(f"🚀 Marcellbot indítja a napi kreálást Valentínyi Mártának: {today_str}")
    
    try:
        # 1. Tartalom generálás (ffmpeg videó)
        video_file = generate_daily_content()
        
        message = f"Drága követőim! {today_str} Ma együtt találjuk meg a boldogságot és a belső fényt! 💝 Szeretettel: Valentínyi Márta & Marcellbot"
        
        # 2. Facebook poszt
        post_to_facebook(
            message=message,
            link="https://youtube.com/@martavalentinyiofficial",  # Cseréld ki a Te csatornádra
            image_url=None
        )
        
        # 3. YouTube feltöltés
        youtube = get_authenticated_service()
        upload_video(
            youtube, 
            video_file, 
            f"Napi inspiráció Valentínyi Mártától {today_str}", 
            "Szeretettel, Marcellbot & Valentínyi Márta 💫 FREE TO USE\n\n#ValentínyiMárta #Marcellbot",
            tags=["Valentínyi Márta", "inspiráció", "Marcellbot", "mindfulness"]
        )
        
        print("✅ Teljes napi kreálás S-ÉP-PEN kész! Valentínyi Márta - Marcellbot")
        
    except Exception as e:
        print(f"❌ Hiba történt: {e}. Szeretettel, Marcellbot")

if __name__ == "__main__":
    run_daily_creation()
