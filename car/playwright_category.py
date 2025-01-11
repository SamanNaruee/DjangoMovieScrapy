import asyncio
from playwright.async_api import async_playwright

async def extract_categories():
    links = {}
    url = "https://www.digikala.com/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the website
        await page.goto(url, wait_until="networkidle")

        try:
            await page.wait_for_selector("span[data-cro-id='header-main-menu']", timeout=10000)
            await page.click("span[data-cro-id='header-main-menu']")
            await page.wait_for_timeout(2000)  # Wait for the dropdown to appear
        except Exception as e:
            print(f"Error clicking main menu: {e}")
            await browser.close()
            return

        try:
            categories = await page.query_selector_all("a[href*='/search/category-']")  # Example selector
            for category in categories:
                name = await category.text_content()
                link = await category.get_attribute("href")
                print(f"{name.strip()}: {link}")
                links[name.strip()] = link
        except Exception as e:
            print(f"Error extracting categories: {e}")

        await browser.close()    


asyncio.run(extract_categories())
