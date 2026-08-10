import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="VeritasAI/1.0 (test)"
)

page = wiki.page("Earth")

print(page.exists())
print(page.title)
print(page.summary[:300])