from playwright.sync_api import sync_playwright
from utils import get_random_user_agent, random_delay, clean_price, clean_text

def search_trendyol(query: str, max_results: int = 10):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=get_random_user_agent(),
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        try:
            url = f"https://www.trendyol.com/sr?q={query.replace(' ', '+')}"
            print(f"Aranıyor: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            random_delay(3, 6)

            page.wait_for_selector(".p-card-wrppr", timeout=15000)
            products = page.query_selector_all(".p-card-wrppr")

            for product in products[:max_results]:
                try:
                    name_el    = product.query_selector(".prdct-desc-cntnr-name")
                    brand_el   = product.query_selector(".prdct-desc-cntnr-ttl-w")
                    price_el   = product.query_selector(".prc-box-dscntd, .prc-box-sllng")
                    link_el    = product.query_selector("a")

                    name  = clean_text(name_el.inner_text())  if name_el  else ""
                    brand = clean_text(brand_el.inner_text()) if brand_el else ""
                    price = clean_price(price_el.inner_text()) if price_el else None
                    link  = "https://www.trendyol.com" + link_el.get_attribute("href") if link_el else ""

                    if name and price:
                        results.append({
                            "platform": "trendyol",
                            "name": f"{brand} {name}".strip(),
                            "price": price,
                            "currency": "TRY",
                            "url": link
                        })
                except Exception as e:
                    print(f"Ürün parse hatası: {e}")
                    continue

        except Exception as e:
            print(f"Sayfa hatası: {e}")
        finally:
            browser.close()

    return results