# 🚀 Instrukcja Wdrożenia Smart Seller Bot na Streamlit Cloud

Poniżej znajdziesz krok po kroku instrukcję, jak wdrożyć aplikację na platformę Streamlit Cloud, aby mieć do niej dostęp z dowolnego urządzenia przez URL.

## Krok 1: Przygotowanie GitHub

Streamlit Cloud wymaga, aby kod znajdował się w repozytorium GitHub. Postępuj następująco:

1. **Utwórz konto GitHub** (jeśli jeszcze go nie masz): https://github.com/signup
2. **Utwórz nowe repozytorium**:
   - Kliknij na `+` w górnym prawym rogu i wybierz `New repository`
   - Nazwij je `smart-seller-bot`
   - Wybierz `Public` (aby Streamlit Cloud mógł je odczytać)
   - Kliknij `Create repository`

3. **Wyślij kod do GitHub**:
   - Otwórz Terminal/PowerShell na swoim komputerze
   - Przejdź do folderu `smart_seller_bot`
   - Wykonaj następujące polecenia:
   ```bash
   git remote add origin https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/smart-seller-bot.git
   git branch -M main
   git push -u origin main
   ```
   - Zamiast `TWOJA_NAZWA_UZYTKOWNIKA` wstaw swoją nazwę użytkownika GitHub

## Krok 2: Wdrożenie na Streamlit Cloud

1. **Przejdź do Streamlit Cloud**: https://streamlit.io/cloud
2. **Zaloguj się** na swoje konto GitHub (jeśli jeszcze tego nie zrobiłeś, kliknij `Sign up` i postępuj zgodnie z instrukcjami)
3. **Kliknij `New app`**
4. **Wypełnij formularz**:
   - **Repository**: `TWOJA_NAZWA_UZYTKOWNIKA/smart-seller-bot`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **Kliknij `Deploy`** i czekaj (może to potrwać kilka minut)

## Krok 3: Konfiguracja Aplikacji

Po wdrożeniu aplikacja otworzy się w przeglądarce. Zobaczysz ekran "Kreator Konfiguracji":

1. **Wklej OpenAI API Key**:
   - Przejdź do https://platform.openai.com/account/api-keys
   - Zaloguj się lub utwórz konto
   - Kliknij `Create new secret key`
   - Skopiuj klucz i wklej go w aplikacji

2. **Wklej Telegram Bot Token i Chat ID**:
   - Utwórz bota na Telegramie: napisz `/newbot` do @BotFather
   - Skopiuj token i wklej w aplikacji
   - Aby uzyskać Chat ID: wyślij wiadomość do swojego bota, a następnie przejdź do: `https://api.telegram.org/botTWÓJ_TOKEN/getUpdates`
   - Skopiuj `chat.id` z odpowiedzi JSON

3. **Wklej Vinted/OLX Session Cookies**:
   - Zaloguj się do Vinted/OLX w przeglądarce
   - Otwórz Narzędzia Deweloperskie (F12)
   - Przejdź do `Application` (Chrome) lub `Storage` (Firefox)
   - Wybierz `Cookies` i domenę Vinted/OLX
   - Skopiuj wszystkie ciasteczka (zazwyczaj jest opcja `Copy all as JSON`)
   - Wklej je w aplikacji

4. **Ustaw zniżkę** i kliknij `Zapisz i Uruchom Bota`

## Krok 4: Uzyskanie Publicznego Linku

Po wdrożeniu Twoja aplikacja będzie dostępna pod adresem:
```
https://smart-seller-bot-TWOJA_NAZWA_UZYTKOWNIKA.streamlit.app
```

Możesz otworzyć ten link na swoim telefonie, komputerze lub dowolnym urządzeniu z przeglądarką.

## Uwagi Ważne

- **Bezpieczeństwo**: Nigdy nie udostępniaj linku do aplikacji osobom trzecim, ponieważ zawiera ona Twoje klucze API.
- **Ciasteczka sesji**: Mają ograniczony czas ważności. Jeśli bot przestanie działać, zaloguj się ponownie do Vinted/OLX i zaktualizuj ciasteczka.
- **Koszty OpenAI**: Pamiętaj, że każda wiadomość wysłana do GPT-4o będzie kosztować. Monitoruj swoje użycie na https://platform.openai.com/account/usage/overview

## Rozwiązywanie Problemów

**Problem**: Aplikacja nie uruchamia się
- Sprawdź, czy wszystkie zależności w `requirements.txt` są zainstalowane
- Sprawdź logi w Streamlit Cloud (kliknij na aplikację i przejdź do `Logs`)

**Problem**: Bot nie wysyła wiadomości
- Sprawdź, czy ciasteczka sesji są aktualne
- Sprawdź, czy OpenAI API Key jest prawidłowy
- Sprawdź logi w aplikacji (zakładka `📊 Akcje i Logi`)

**Problem**: Nie otrzymuję powiadomień na Telegramie
- Sprawdź, czy Telegram Bot Token jest prawidłowy
- Sprawdź, czy Chat ID jest prawidłowy
- Wyślij wiadomość do bota, aby upewnić się, że jest aktywny

---

Jeśli masz pytania lub problemy, skontaktuj się z supportem Streamlit: https://docs.streamlit.io/
