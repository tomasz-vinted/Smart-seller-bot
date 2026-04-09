# 🤖 Smart Seller Bot

Prywatny system automatyzacji sprzedaży na platformach Vinted/OLX. Aplikacja naśladuje ludzkie zachowania, integruje się z GPT-4o do inteligentnej obsługi klienta oraz powiadamia Cię na Telegramie o ważnych zapytaniach.

## 🚀 Funkcje
- **Logika Czasowa:** Wysyłanie ofert w przedziale 30-120 minut z rozkładem prawdopodobieństwa sprzyjającym dłuższemu oczekiwaniu.
- **Silent Night:** Bot śpi od 22:00 do 07:00. Akcje z nocy są kolejkowane na rano z losowym opóźnieniem.
- **Inteligentny Czat (GPT-4o):** Automatyczne odpowiedzi na pytania techniczne na podstawie opisu przedmiotu.
- **Integracja Telegram:** Powiadomienia o negocjacjach lub pytaniach, na które bot nie zna odpowiedzi.
- **Strategia Rebump:** Codzienny "Micro-edit" (zmiana ceny o 1 zł lub edycja opisu) w celu podbicia ogłoszenia bez utraty polubień.
- **Human-like Behavior:** Playwright Stealth, losowe ruchy myszki, emulacja pisania na klawiaturze.
- **Elegant Dashboard:** Interfejs Streamlit zoptymalizowany pod urządzenia mobilne.

## 🛠️ Instalacja i Uruchomienie

1. Zainstaluj zależności:
   ```bash
   pip install streamlit playwright playwright-stealth openai python-telegram-bot sqlalchemy schedule
   playwright install chromium
   ```

2. Uruchom interfejs Dashboard:
   ```bash
   streamlit run app.py
   ```

3. Uruchom silnik bota (w osobnym terminalu):
   ```bash
   python main.py
   ```

## ⚙️ Konfiguracja
W panelu Streamlit wprowadź:
- **OpenAI API Token:** Do obsługi inteligentnego czatu.
- **Telegram Bot Token & Chat ID:** Do otrzymywania powiadomień.
- **Zniżka:** Kwota, o którą bot będzie obniżał cenę w ofertach.

## 🔒 Bezpieczeństwo
Bot korzysta z trybu Stealth i naśladuje ludzkie opóźnienia, aby zminimalizować ryzyko wykrycia przez platformy sprzedażowe. Pamiętaj, aby używać go z rozwagą.

---
*Smart Seller Bot v1.0 | Made for Sellers*
