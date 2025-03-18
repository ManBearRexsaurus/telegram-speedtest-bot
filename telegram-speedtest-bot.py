import os
from dotenv import load_dotenv
import speedtest
import requests

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def run_speedtest():
    print("Running speed test...")
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping
    server = st.results.server

    results = {
        "download": round(download_speed, 2),
        "upload": round(upload_speed, 2),  # Fixed the bug here
        "ping": round(ping, 2),
        "server": server['host']
    }
    print("Speed test completed.")
    print("Results:", results)
    return results

def send_message(results):
    message = (
        f"📡 **Speed Test Results:**\n"
        f"- Download: {results['download']} Mbps\n"
        f"- Upload: {results['upload']} Mbps\n"
        f"- Ping: {results['ping']} ms\n"
        f"- Server: {results['server']}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    
    return response.ok

if __name__ == "__main__":
    results = run_speedtest()
    success = send_message(results)
    if success:
        print("Message sent to Telegram successfully!")
    else:
        print("Failed to send Telegram message.")

