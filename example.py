from zillow_scrapers.scraper import ZillowScraper
import json
scraper = ZillowScraper()
agent_data = scraper.search_agent(location='Orange, CA', max_page=3, get_contact=True)
print(json.dumps(agent_data.result, indent=4))