import requests

def send_message(bottoken: str, chatid: str, message: str) -> str:
    url = f"https://api.telegram.org/bot{bottoken}/sendMessage"
    payload = {"chat_id": chatid, "text": message}
    response = requests.post(url, data=payload)
    return response.text

