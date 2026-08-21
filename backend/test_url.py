from app.url.service import extract_article

url = "https://www.bbc.com/news"

result = extract_article(url)

print(result["title"])
print(result["text"][:500])