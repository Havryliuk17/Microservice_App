import requests
from dotenv import load_dotenv
load_dotenv()
import os
TOKEN = os.getenv("APP_TOKEN")


DB_PORT = 8001
BL_PORT = 8002
CLIENT_PORT = 8000

DB_URL = f"http://localhost:{DB_PORT}"
BL_URL = f"http://localhost:{BL_PORT}"
CLIENT_URL = f"http://localhost:{CLIENT_PORT}"


sample_articles = [
    {
        "title": "The Rise of AI",
        "body": (
            "Artificial Intelligence (AI) has rapidly evolved over the past decade, "
            "transforming industries from healthcare to finance. Its ability to learn "
            "from data and improve performance over time has made AI a critical tool "
            "in solving complex problems and driving innovation across the globe."
        )
    },
    {
        "title": "Climate Change Effects",
        "body": (
            "Climate change is affecting ecosystems and human livelihoods. Rising sea "
            "levels, increased frequency of extreme weather events, and shifting wildlife "
            "patterns are just some of the visible signs. Global efforts are being made to "
            "mitigate these effects through sustainable practices and international agreements."
        )
    },
    {
        "title": "Benefits of Remote Work",
        "body": (
            "Remote work has become increasingly popular, offering flexibility and better work-life balance. "
            "It reduces commuting stress, allows for personalized work environments, and can increase productivity. "
            "However, it also brings challenges in communication and collaboration that organizations must address."
        )
    },
    {
        "title": "Space Exploration in 2020s",
        "body": (
            "The 2020s mark a new era of space exploration with missions to Mars, commercial spaceflights, "
            "and ambitious plans to return humans to the Moon. Agencies like NASA, SpaceX, and ESA are leading "
            "this charge, pushing boundaries and inspiring the next generation of scientists and engineers."
        )
    },
    {
        "title": "Advancements in Biotechnology",
        "body": (
            "Biotechnology is revolutionizing medicine and agriculture. From CRISPR gene editing to lab-grown meat, "
            "scientists are developing innovative ways to improve human health and food production. "
            "Ethical considerations continue to guide research in this fast-paced field."
        )
    }
]

print("Populating the database with sample articles...")
article_ids = []
for article in sample_articles:
    response = requests.post(f"{DB_URL}/write", json=article)
    if response.status_code == 200:
        result = response.json()
        article_ids.append(result["id"])
        print(f"Saved: ID={result['id']}, Title='{article['title']}'")
    else:
        print(f"Error saving article '{article['title']}':", response.text)


if article_ids:
    article_id = article_ids[0] 
    print(f"\nRequesting summary for article ID: {article_id}")
    sum_url = f"{CLIENT_URL}/summarize"
    sum_resp = requests.post(sum_url, params={"id": article_id, "authorization": TOKEN})


    if sum_resp.status_code != 200:
        print("❌ Error from Summarize endpoint:", sum_resp.text)
    else:
        print("\n✅ Summary Response:")
        print(sum_resp.json())
else:
    print("❌ No articles saved. Cannot proceed with summarization.")
