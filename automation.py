import asyncio
import random
import time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def human_delay(min_sec=1, max_sec=3):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def type_like_human(page, selector, text):
    await page.focus(selector)
    for char in text:
        await page.keyboard.type(char, delay=random.uniform(50, 150))
        if random.random() < 0.1: # 10% szans na krótką przerwę
            await asyncio.sleep(random.uniform(0.2, 0.5))

async def move_mouse_randomly(page):
    width, height = 1280, 720 # Domyślne wymiary
    for _ in range(random.randint(3, 7)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        await page.mouse.move(x, y, steps=random.randint(10, 20))
        await asyncio.sleep(random.uniform(0.1, 0.3))

class SmartSellerEngine:
    def __init__(self, user_agent=None):
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    async def get_browser_context(self, playwright, session_data=None):
        browser = await playwright.chromium.launch(headless=True) # Można zmienić na False do debugowania
        context = await browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1280, 'height': 720}
        )
        if session_data:
            # Playwright oczekuje listy słowników z ciasteczkami
            # Zakładamy, że session_data to już sparsowany JSON z ciasteczkami
            await context.add_cookies(session_data)
        
        page = await context.new_page()
        await stealth_async(page)
        return browser, context, page

    async def check_notifications(self, platform_url, session_data):
        async with async_playwright() as p:
            browser, context, page = await self.get_browser_context(p, session_data)
            try:
                await page.goto(platform_url)
                await human_delay(2, 5)
                await move_mouse_randomly(page)
                
                # Logika specyficzna dla platformy (Vinted/OLX)
                # Tutaj będa selektory do sprawdzania polubień
                # Na potrzeby szkieletu zwracamy pustą listę
                new_likes = [] 
                return new_likes
            finally:
                await browser.close()

    async def send_offer(self, platform_url, user_id, item_id, message, session_data):
        async with async_playwright() as p:
            browser, context, page = await self.get_browser_context(p, session_data)
            try:
                # Przejdź do konwersacji lub strony przedmiotu
                await page.goto(f"{platform_url}/items/{item_id}")
                await human_delay(3, 6)
                
                # Symulacja pisania wiadomości
                # await type_like_human(page, "selector-wiadomosci", message)
                # await page.click("selector-wyslij")
                
                return True
            except Exception as e:
                print(f"Błąd podczas wysyłania oferty: {e}")
                return False
            finally:
                await browser.close()
