from zillow_scrapers.scraper import ZillowScraper

scraper = ZillowScraper()
agent_data = scraper.search_agent(location='Orange, CA', max_page=10, get_contact=False)
print(agent_data.result)