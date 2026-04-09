import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Seller Bot", page_icon="🤖")

# Inicjalizacja konfiguracji w pamięci aplikacji
if 'config' not in st.session_state:
st.session_state.config = {'is_active': False, 'discount_amount': 5.0, 'openai_token': '', 'telegram_token': '', 'telegram_chat_id': '', 'platform_session_cookie': ''}

def is_configured():
c = st.session_state.config
return c['openai_token'] and c['telegram_token'] and c['telegram_chat_id'] and c['platform_session_cookie']

st.title("🚀 Smart Seller Bot")

if not is_configured():
st.subheader("Kreator Konfiguracji")
with st.form("setup"):
o_token = st.text_input("OpenAI API Key", type="password")
t_token = st.text_input("Telegram Bot Token", type="password")
t_id = st.text_input("Telegram Chat ID (Same cyfry)")
cookies = st.text_area("Cookies (JSON)")
disc = st.number_input("Zniżka (PLN)", value=5.0)
if st.form_submit_button("Zapisz i Uruchom"):
st.session_state.config.update({'is_active': True, 'discount_amount': disc, 'openai_token': o_token, 'telegram_token': t_token, 'telegram_chat_id': t_id, 'platform_session_cookie': cookies})
st.success("Zapisano! Odśwież stronę.")
st.rerun()
else:
c = st.session_state.config
is_active = st.toggle("Bot Aktywny", value=c['is_active'])
st.session_state.config['is_active'] = is_active
st.markdown(f"**Status:** {'✅ AKTYWNY' if is_active else '❌ NIEAKTYWNY'}")
t1, t2 = st.tabs(["Ustawienia", "Status"])
with t1:
with st.form("update"):
d = st.number_input("Zniżka", value=c['discount_amount'])
ot = st.text_input("OpenAI Key", value=c['openai_token'], type="password")
tt = st.text_input("Telegram Token", value=c['telegram_token'], type="password")
ti = st.text_input("Chat ID", value=c['telegram_chat_id'])
co = st.text_area("Cookies", value=c['platform_session_cookie'])
if st.form_submit_button("Aktualizuj"):
st.session_state.config.update({'discount_amount': d, 'openai_token': ot, 'telegram_token': tt, 'telegram_chat_id': ti, 'platform_session_cookie': co})
st.success("Zaktualizowano!")
st.rerun()
with t2:
st.info("Bot pracuje w chmurze. Powiadomienia otrzymasz na Telegramie.")
st.write("Ostatnia synchronizacja: " + pd.Timestamp.now().strftime("%H:%M:%S"))
