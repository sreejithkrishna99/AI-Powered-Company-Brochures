import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai

# ==============================
# Load API Key
# ==============================
load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ OpenAI API key not found. Please add it to your .env file.")

# Model
MODEL = "gpt-3.5-turbo"

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

# ==============================
# Website Scraper
# ==============================
class Website:
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
            self.body, self.text, self.title, self.links = "", "", "", []
            return

        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        self.links = [link.get("href") for link in soup.find_all("a") if link.get("href")]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nContents:\n{self.text}\n\n"

# ==============================
# Get Relevant Links
# ==============================
link_system_prompt = """
You are provided with a list of links found on a webpage.
Select which links are most relevant for a company brochure:
About, Products, Services, Careers, Contact.
Respond in JSON like this:
{
    "links": [
        {"type": "about page", "url": "https://example.com/about"},
        {"type": "careers page", "url": "https://example.com/careers"}
    ]
}
"""

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on {website.url}.\n"
    user_prompt += "Select relevant links for a brochure. Respond ONLY in JSON.\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url):
    website = Website(url)
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ]
    )
    content = response.choices[0].message["content"]
    return json.loads(content)

# ==============================
# Fetch All Details
# ==============================
def get_all_details(url):
    result = Website(url).get_contents()
    links = get_links(url)
    print("🔗 Found relevant links:", links)

    for link in links.get("links", []):
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

# ==============================
# Build Brochure Prompt
# ==============================
system_prompt = """
You are an assistant that creates a short, professional company brochure.
Highlight overview, products, services, culture, achievements, customers, careers.
Respond in Markdown.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"Company: {company_name}\n"
    user_prompt += "Contents from relevant pages:\n"
    user_prompt += get_all_details(url)
    return user_prompt[:5000]  # truncate to avoid token limit

# ==============================
# Create Brochure
# ==============================
def create_brochure(company_name, url):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    brochure_text = response.choices[0].message["content"]
    filename = f"{company_name}_brochure.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(brochure_text)
    print(f"✅ Brochure created: {filename}")

# ==============================
# Main
# ==============================
if __name__ == "__main__":
    company_name = input("Enter company name: ").strip()
    website = input("Enter company website (https://...): ").strip()
    create_brochure(company_name, website)
