from trendyol import search_trendyol
import json

def main():
    print("SmartCart Scraper başlatılıyor...")
    query = input("Aramak istediğin ürünü yaz: ")

    print(f"\nTrendyol'da '{query}' aranıyor...\n")
    results = search_trendyol(query, max_results=5)

    if results:
        print(f"{len(results)} ürün bulundu:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']}")
            print(f"   Fiyat: {r['price']} TL")
            print(f"   Link: {r['url']}\n")
    else:
        print("Ürün bulunamadı.")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Sonuçlar results.json dosyasına kaydedildi.")

if __name__ == "__main__":
    main()