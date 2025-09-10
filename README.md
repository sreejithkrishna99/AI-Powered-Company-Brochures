# AI-Powered Company Brochure Generator

A Python tool that automatically creates **professional company brochures** for prospective clients, investors, and potential recruits. By providing a **company name** and its **primary website**, this project scrapes relevant content and uses **OpenAI GPT** to generate a polished brochure in **Markdown format**.

---

## **Project Overview**

The **AI-Powered Company Brochure Generator** intelligently analyzes a company’s website, including landing pages and other relevant sections like About, Careers, Products, and Services. It identifies key content, filters irrelevant links, and produces a structured, professional brochure highlighting:

- Company overview and mission
- Products and services
- Achievements and notable projects
- Company culture and values
- Career opportunities
- Customer and client information (if available)

The brochure is generated in **Markdown** for easy editing, sharing, or converting to PDF.

---

## **Features**

- **Automated Web Scraping:** Extracts clean textual content from company websites, removing scripts, styles, images, and forms.
- **AI Link Filtering:** Determines which pages are relevant for the brochure (About, Careers, Products/Services) while excluding irrelevant links.
- **Content Aggregation:** Combines information from multiple pages to provide a comprehensive overview.
- **AI-Powered Brochure Generation:** Uses OpenAI GPT-3.5-turbo (or GPT-4o-mini) to generate professional and concise content.
- **VS Code Compatible:** Runs locally using Python 3.8+ and OpenAI SDK v0.28.
- **Markdown Output:** Produces a ready-to-use brochure file (`CompanyName_brochure.md`).

---

## **Requirements**

- Python 3.8+
- [OpenAI Python SDK v0.28](https://pypi.org/project/openai/0.28/)
- Requests
- BeautifulSoup4
- python-dotenv


