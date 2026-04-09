import random
import datetime
import json
from models import Session, ScheduledAction, Log

def get_random_delay():
    """
    Zwraca losowe opóźnienie w sekundach (30 - 120 minut).
    Rozkład prawdopodobieństwa: częściej wybiera czasy bliższe 120 minut.
    Używamy rozkładu trójkątnego (triangular) lub potęgowego.
    """
    # random.triangular(low, high, mode) - mode=high sprawia, że częściej wybiera wartości bliskie high
    delay_minutes = random.triangular(30, 120, 120)
    return int(delay_minutes * 60)

def is_silent_night():
    """
    Sprawdza czy aktualnie jest tryb nocny (22:00 - 07:00).
    """
    now = datetime.datetime.now().time()
    start_silent = datetime.time(22, 0)
    end_silent = datetime.time(7, 0)
    
    if start_silent <= now or now <= end_silent:
        return True
    return False

def schedule_offer(user_id, item_id, item_name):
    """
    Kolejkuje wysłanie oferty z odpowiednim opóźnieniem.
    """
    session = Session()
    delay_seconds = get_random_delay()
    now = datetime.datetime.now()
    scheduled_time = now + datetime.timedelta(seconds=delay_seconds)
    
    # Jeśli zaplanowany czas wypada w nocy, przesuń na rano
    if is_silent_night() or (scheduled_time.time() >= datetime.time(22, 0) or scheduled_time.time() <= datetime.time(7, 0)):
        # Ustaw na 07:00 rano + dodatkowe losowe opóźnienie (np. 10-60 min)
        tomorrow = now + datetime.timedelta(days=1 if now.hour >= 22 else 0)
        morning_start = datetime.datetime.combine(tomorrow.date(), datetime.time(7, 0))
        extra_delay = random.randint(600, 3600) # 10-60 min
        scheduled_time = morning_start + datetime.timedelta(seconds=extra_delay)
    
    payload = json.dumps({
        'user_id': user_id,
        'item_id': item_id,
        'item_name': item_name
    })
    
    new_action = ScheduledAction(
        action_type='send_offer',
        payload=payload,
        scheduled_time=scheduled_time
    )
    
    session.add(new_action)
    session.add(Log(level='INFO', message=f"Zaplanowano ofertę dla {user_id} na {scheduled_time}"))
    session.commit()
    session.close()

def get_pending_actions():
    """
    Pobiera akcje, których czas wykonania już nadszedł.
    """
    session = Session()
    now = datetime.datetime.now()
    actions = session.query(ScheduledAction).filter(
        ScheduledAction.scheduled_time <= now,
        ScheduledAction.is_completed == False
    ).all()
    session.close()
    return actions
