import feedparser
import requests
import time

# --- إعدادات البوت الخاص بك ---
TOKEN = "8667925105:AAEAlTlTWry_BW8qwCMipwJjNAmUxJtznuQ"
CHAT_ID = "1300087126"
RSS_URL = "https://rss.app/feeds/3FaratVUao0nZydS.xml"

# متغير لحفظ آخر منشور تم إرساله لمنع التكرار
last_entry_id = None

def send_telegram_msg(title, link):
    message = f"📢 منشور جديد:\n\n{title}\n\nالرابط:\n{link}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

print("البوت بدأ العمل بمعدل فحص كل دقيقة...")

while True:
    try:
        # قراءة رابط الـ RSS
        feed = feedparser.parse(RSS_URL)
        
        if feed.entries:
            latest_entry = feed.entries[0]
            current_id = latest_entry.id if hasattr(latest_entry, 'id') else latest_entry.link
            
            # التأكد أن المنشور جديد وليس الذي أرسلناه سابقاً
            if current_id != last_entry_id:
                if last_entry_id is not None: # ليتجاهل القديم عند أول تشغيل
                    send_telegram_msg(latest_entry.title, latest_entry.link)
                
                last_entry_id = current_id
                print(f"تم إرسال منشور جديد: {latest_entry.title}")
        
    except Exception as e:
        print(f"حدث خطأ أثناء الفحص: {e}")

    # الانتظار لمدة 60 ثانية (دقيقة واحدة)
    time.sleep(60)
