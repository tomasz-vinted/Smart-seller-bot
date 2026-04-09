import streamlit as st
import pandas as pd
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Konfiguracja bazy danych bezpośrednio w app.py dla stabilności
Base = declarative_base()
class BotConfig(Base):
__tablename__ = 'bot_config'
id = Column(Integer, primary_key=True)
is_active = Column(Boolean, default=False)
discount_amount = Column(Float, default=5.0)
openai_token = Column(String)
telegram_token = Column(String)
telegram_chat_id = Column(String)
platform_session_cookie = Column(Text)

engine = create_engine('sqlite:///smart_seller.db')
Base.metadata.create_all(engine)
# Kluczowa poprawka: expire_on_commit=False
Session = sessionmaker(bind=engine, expire_on_commit=False)

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
if not config:
config = BotConfig()
session.add(config)
config.is_active = is_active
config.discount_amount = discount
config.openai_token = openai_token
config.telegram_token = telegram_token
config.telegram_chat_id = str(chat_id).strip()
if session_cookie:
config.platform_session_cookie = session_cookie
session.commit()
session.close()

config = get_config()
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

t1, t2 = st.tabs(["Ustawienia", "Status"])
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
with t2:
st.write("Bot jest skonfigurowany i gotowy do pracy.")
st.info("Sprawdzaj powiadomienia na Telegramie!")
