import time
import traceback
import json
from zillow_scrapers.utils.driver_utils import human_interaction, fill_form, captcha_checker, extract_page

class AgentScraper:
    def __init__(self, context, location, max_page, get_contact):
        self.page = context.new_page()
        self.location = location
        self.max_page = max_page
        self.get_contact = get_contact
        self.result = self._search_by_location()

    def _search_by_location(self):
        self.page.goto('https://www.zillow.com/professionals/real-estate-agent-reviews/')
        self.page.wait_for_load_state("domcontentloaded")
        captcha_checker(self.page)
        form = self.page.locator('input[placeholder="City, neighborhood, or ZIP code"]')
        human_interaction(self.page)
        fill_form(self.page, form, self.location)
        return self._scrape_agent_list()

    def _scrape_agent_list(self):
        page_counter = 0
        storage = []
        next_button = True
        while next_button and page_counter < self.max_page:
            try:
                captcha_checker(self.page)
                self.page.wait_for_load_state('domcontentloaded')
                next_button = self.page.locator('button[rel="next"][title="Next page"]').first
                self.page.wait_for_load_state("domcontentloaded")
                storage.extend(extract_page(self.page, "list"))
                page_counter+=1
                if next_button.get_attribute("disabled") is not None:
                    next_button = False
                else:
                    human_interaction(self.page)
                    next_button.scroll_into_view_if_needed()
                    next_button.click()
                    
            except Exception as e:
                print(traceback.format_exc())
                break
        return storage
    
        