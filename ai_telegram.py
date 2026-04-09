import openai
import requests
from models import Session, BotConfig, Log

class SmartAI:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def analyze_and_respond(self, item_description, user_question):
        """
        Analizuje opis przedmiotu i odpowiada na pytanie techniczne.
        """
        prompt = f"""
        Jesteś pomocnym sprzedawcą na platformie Vinted/OLX. 
        Oto opis przedmiotu: {item_description}
        Klient pyta: {user_question}
        
        Odpowiedz na pytanie techniczne na podstawie opisu. 
        Jeśli nie znasz odpowiedzi lub pytanie dotyczy negocjacji ceny, 
        odpowiedz dokładnie: "NEGOTIATION_OR_UNKNOWN".
        W przeciwnym razie odpowiedz uprzejmie i krótko po polsku.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Błąd OpenAI: {e}")
            return "NEGOTIATION_OR_UNKNOWN"

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}/sendMessage"

    def send_notification(self, message, conversation_link=None):
        """
        Wysyła powiadomienie na Telegram.
        """
        text = message
        if conversation_link:
            text += f"\n\nLink do rozmowy: {conversation_link}"
            
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            requests.post(self.base_url, json=payload)
        except Exception as e:
            print(f"Błąd Telegram: {e}")

def handle_incoming_message(user_question, item_description, conversation_link):
    """
    Główna logika obsługi wiadomości przychodzącej.
    """
    session = Session()
    config = session.query(BotConfig).first()
    
    if not config or not config.openai_token:
        return "Brak konfiguracji AI"
        
    ai = SmartAI(config.openai_token)
    response = ai.analyze_and_respond(item_description, user_question)
    
    if response == "NEGOTIATION_OR_UNKNOWN":
        if config.telegram_token and config.telegram_chat_id:
            notifier = TelegramNotifier(config.telegram_token, config.telegram_chat_id)
            notifier.send_notification(
                f"⚠️ *Wymagana interwencja!* \nKlient pyta: {user_question}",
                conversation_link
            )
        return None # Bot nie odpowiada, czeka na użytkownika
    
    return response
