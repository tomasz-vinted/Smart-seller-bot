import random
import datetime
from models import Session, Log, ScheduledAction
import json

def apply_micro_edit(description, price):
    """
    Zmienia cenę o 1 zł lub dodaje/usuwa kropkę w opisie.
    """
    # 50% szans na zmianę ceny, 50% na zmianę opisu
    if random.random() < 0.5:
        # Zmiana ceny o 1 zł (losowo w górę lub w dół)
        new_price = price + random.choice([-1, 1])
        if new_price < 1: new_price = 1
        return description, new_price
    else:
        # Dodanie lub usunięcie kropki na końcu opisu
        if description.endswith('.'):
            new_description = description[:-1]
        else:
            new_description = description + '.'
        return new_description, price

def schedule_daily_rebump(item_id, current_description, current_price):
    """
    Planuje codzienny rebump dla przedmiotu.
    """
    session = Session()
    now = datetime.datetime.now()
    # Planujemy na jutro o tej samej porze z lekkim przesunięciem
    scheduled_time = now + datetime.timedelta(days=1) + datetime.timedelta(minutes=random.randint(-30, 30))
    
    # Unikaj nocy (22:00 - 07:00)
    if scheduled_time.hour >= 22 or scheduled_time.hour <= 7:
        scheduled_time = scheduled_time.replace(hour=random.randint(9, 18))
        
    payload = json.dumps({
        'item_id': item_id,
        'description': current_description,
        'price': current_price
    })
    
    new_action = ScheduledAction(
        action_type='rebump',
        payload=payload,
        scheduled_time=scheduled_time
    )
    
    session.add(new_action)
    session.add(Log(level='INFO', message=f"Zaplanowano rebump dla {item_id} na {scheduled_time}"))
    session.commit()
    session.close()
