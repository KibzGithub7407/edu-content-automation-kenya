import requests, json

def get_keywords(query):
    """
    Fetches relevant keywords and search results using the Serper API,
    optimized for the Kenyan context.
    """
    url = "https://api.serper.dev/search"
    # 'gl': 'ke' ensures results are geo-localized to Kenya
    payload = {"q": query, "gl": "ke", "num": 10}
    headers = {"X-API-KEY": "YOUR_SERPER_KEY"}

    try:
        res = requests.post(url, json=payload, headers=headers)
        res.raise_for_status()  # Raise an exception for bad status codes
        results = res.json().get("organic", [])
        return [r["title"] for r in results if "title" in r]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching keywords: {e}")
        return []

if __name__ == "__main__":
    # Example queries tailored for the Kenyan education market
    kenyan_queries = [
        "KCSE revision tips",
        "KCPE 2025 exam dates",
        "Muslim schools Nairobi admissions",
        "Best high schools Kenya",
        "Form One selection process Kenya"
    ]
    all_keywords = []
    for q in kenyan_queries:
        print(f"Fetching keywords for: {q}")
        all_keywords.extend(get_keywords(q))

    # Save unique keywords to prevent duplication
    unique_keywords = list(set(all_keywords))

    with open("data/keyword_trends.json", "w") as f:
        json.dump(unique_keywords, f, indent=2)
    print(f"Fetched and saved {len(unique_keywords)} keywords to data/keyword_trends.json")
