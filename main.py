import asyncio
import time
import json
import datetime
from models import Session, BotConfig, Log, UserAction, ScheduledAction
from automation import SmartSellerEngine
from scheduler import get_pending_actions, is_silent_night
from ai_telegram import handle_incoming_message
from rebump import apply_micro_edit

async def process_actions():
    """
    Główna pętla przetwarzająca zaplanowane akcje.
    """
    engine = SmartSellerEngine()
    
    while True:
        session = Session()
        config = session.query(BotConfig).first()
        
        if config and config.is_active:
            session_data = json.loads(config.platform_session_cookie) if config.platform_session_cookie else None
            # 1. Sprawdź czy są akcje do wykonania
            pending_actions = get_pending_actions()
            
            for action in pending_actions:
                if is_silent_night():
                    # Jeśli nastała noc, pomiń przetwarzanie (zostaną na rano)
                    continue
                
                payload = json.loads(action.payload)
                success = False
                
                if action.action_type == 'send_offer':
                    # Logika wysyłania oferty
                    message = f"Hej! Widzę, że {payload['item_name']} wpadła Ci w oko. Jeśli zdecydujesz się na zakup, jestem w stanie zaoferować Ci zniżkę i gwarantuję, że postaram się, aby paczka została nadana w 24h! 🚚 Zerknij też na moje pozostałe ogłoszenia – mam tam jeszcze kilka perełek, które mogą Ci się spodobać. Miłego dnia! 😁"
                    
                    # Tutaj wywołanie silnika Playwright (wymaga ciasteczek sesji)
                    # success = await engine.send_offer("https://www.vinted.pl", payload["user_id"], payload["item_id"], message, session_data)
                    
                    # Symulacja sukcesu dla celów demonstracyjnych
                    success = True 
                    
                    if success:
                        new_user_action = UserAction(
                            platform_user_id=payload['user_id'],
                            item_id=payload['item_id'],
                            item_name=payload['item_name'],
                            action_type='offer_sent'
                        )
                        session.add(new_user_action)
                        session.add(Log(level='INFO', message=f"Wysłano ofertę do {payload['user_id']}"))
                
                elif action.action_type == 'rebump':
                    # Logika rebump (micro-edit)
                    new_desc, new_price = apply_micro_edit(payload['description'], payload['price'])
                    # success = await engine.update_item(payload["item_id"], new_desc, new_price, session_data)
                    success = True
                    if success:
                        session.add(Log(level='INFO', message=f"Wykonano rebump dla przedmiotu {payload['item_id']}"))
                
                if success:
                    action.is_completed = True
                    session.commit()
            
            # 2. Sprawdź nowe powiadomienia (polubienia)
            # To powinno dziać się rzadziej, np. co 15 minut
                        # new_likes = await engine.check_notifications("https://www.vinted.pl", session_data)
            # for like in new_likes:
            #     schedule_offer(like['user_id'], like['item_id'], like['item_name'])
            
        session.close()
        await asyncio.sleep(60) # Czekaj minutę przed kolejnym sprawdzeniem

if __name__ == "__main__":
    print("Uruchamianie Smart Seller Bot Engine...")
    asyncio.run(process_actions())
