import streamlit as st
import pandas as pd
import json
from models import Session, BotConfig, Log, UserAction, ScheduledAction
from datetime import datetime

st.set_page_config(page_title="Smart Seller Bot", page_icon="🤖")

def get_config():
    session = Session()
    config = session.query(BotConfig).first()
    if not config:
        config = BotConfig(is_active=False, discount_amount=5.0)
        session.add(config)
        session.commit()
    session.close()
    return config

def update_config(is_active, discount, openai_token, telegram_token, chat_id, session_cookie=None):
    session = Session()
    config = session.query(BotConfig).first()
    config.is_active = is_active
    config.discount_amount = discount
    config.openai_token = openai_token
    config.telegram_token = telegram_token
    config.telegram_chat_id = str(chat_id).strip()
    if session_cookie:
        config.platform_session_cookie = session_cookie
    session.commit()
    session.close()

# Pobierz aktualną konfigurację
config = get_config()

# Sprawdź czy bot jest skonfigurowany
is_configured = config.openai_token and config.telegram_token and config.telegram_chat_id and config.platform_session_cookie

if not is_configured:
    st.title("🚀 Kreator Konfiguracji")
    with st.form("setup"):
        o_token = st.text_input("OpenAI API Key", type="password")
        t_token = st.text_input("Telegram Bot Token", type="password")
        t_id = st.text_input("Telegram Chat ID (Same cyfry)")
        cookies = st.text_area("Cookies (JSON)")
        disc = st.number_input("Zniżka (PLN)", value=5.0)
        if st.form_submit_button("Zapisz i Uruchom"):
            update_config(True, disc, o_token, t_token, t_id, cookies)
            st.success("Zapisano! Odśwież stronę.")
            st.rerun()
else:
    st.title("🚀 Smart Seller Bot")
    is_active = st.toggle("Bot Aktywny", value=config.is_active)
    if is_active != config.is_active:
        update_config(is_active, config.discount_amount, config.openai_token, config.telegram_token, config.telegram_chat_id, config.platform_session_cookie)
        st.rerun()
    
    t1, t2, t3 = st.tabs(["Ustawienia", "Logi", "Kolejka"])
    
    with t1:
        with st.form("u"):
            d = st.number_input("Zniżka", value=config.discount_amount)
            ot = st.text_input("OpenAI Key", value=config.openai_token, type="password")
            tt = st.text_input("Telegram Token", value=config.telegram_token, type="password")
            ti = st.text_input("Chat ID", value=config.telegram_chat_id)
            co = st.text_area("Cookies", value=config.platform_session_cookie)
            if st.form_submit_button("Aktualizuj"):
                update_config(is_active, d, ot, tt, ti, co)
                st.rerun()
    
    session = Session()
    with t2:
        st.subheader("Ostatnie Akcje")
        actions = session.query(UserAction).order_by(UserAction.timestamp.desc()).limit(5).all()
        for a in actions:
            st.info(f"{a.timestamp.strftime('%H:%M')} - {a.username}")
        
        st.subheader("Logi Systemowe")
        logs = session.query(Log).order_by(Log.timestamp.desc()).limit(10).all()
        if logs:
            st.table([{"Czas": l.timestamp.strftime("%H:%M"), "Log": l.message} for l in logs])
    
    with t3:
        st.subheader("Zaplanowane Akcje")
        sch = session.query(ScheduledAction).filter(ScheduledAction.is_completed == False).limit(5).all()
        for s in sch:
            st.warning(f"{s.scheduled_time.strftime('%H:%M')} - {s.action_type}")
    session.close()
