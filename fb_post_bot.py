# Valentínyi Márta - Marcellbot - FREE TO USE
import requests

# IDE ÍRD BE A SAJÁT ADATAIDAT:
PAGE_ID = 'remenyhope2026' # pl. 123456789012345
ACCESS_TOKEN = 'YOUR_LONG_LIVED_PAGE_ACCESS_TOKEN'  # Hosszú életű token!

def post_to_facebook(message, link=None, image_url=None):
    if image_url:
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
        payload = {'message': message, 'url': image_url, 'access_token': ACCESS_TOKEN}
    else:
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
        payload = {'message': message, 'access_token': ACCESS_TOKEN}
        if link:
            payload['link'] = link
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Poszt sikeresen feltöltve! Valentínyi Márta - Marcellbot")
        return response.json()
    else:
        print("❌ Hiba:", response.text)

# Példa napi használat:
if __name__ == "__main__":
    post_to_facebook(
        message="Drága követőim! Ma csodálatos napunk van! 💝 Szeretettel: Valentínyi Márta & Marcellbot",
        link="https://youtube.com/@martavalentinyiofficial",
        image_url="https://example.com/beautiful_image.jpg"
    )
