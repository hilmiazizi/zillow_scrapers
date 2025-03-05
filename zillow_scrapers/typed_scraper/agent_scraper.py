import time
import traceback
import json
from zillow_scrapers.utils.driver_utils import human_interaction, fill_form, captcha_checker, extract_page

class AgentScraper:
    def __init__(self, context, location, max_page, get_contact):
        self.context = context
        self.page = self.context.new_page()
        self.location = location
        self.max_page = max_page
        self.get_contact = get_contact
        self.result = self._search_by_location()

    def _search_by_location(self):
        self.page.goto('https://www.zillow.com/professionals/real-estate-agent-reviews/', wait_until="domcontentloaded")
        captcha_checker(self.page)
        form = self.page.locator('input[placeholder="City, neighborhood, or ZIP code"]')
        fill_form(self.page, form, self.location)
        if self.get_contact:
            agent_data = self._scrape_agent_list()
            if agent_data:
                with self.context.expect_page() as new:
                    self.page.evaluate("window.open('about:blank', '_blank')")
                    page2 = new.value
                
                page2.bring_to_front()

                for data in agent_data:
                    result = self._scrape_agent_detail(page2, data['profile_url'])
                    print(f'Contact found for {data["full_name"]}')
                    data.update(result)
            return agent_data
        else:
            return self._scrape_agent_list()

    def _scrape_agent_list(self):
        page_counter = 0
        storage = []
        
        while page_counter < self.max_page:
            try:
                self.page.wait_for_load_state("networkidle")
                captcha_checker(self.page)
                next_button = self.page.locator('button[rel="next"][title="Next page"]').first
                self.page.wait_for_selector('script[id="__NEXT_DATA__"][type="application/json"]', state="attached")
                storage.extend(extract_page(self.page, "list"))
                page_counter += 1
                if not next_button or next_button.evaluate("button => button.disabled") or page_counter >= self.max_page:  
                    print("Next button is disabled or does not exist. Stopping pagination.")
                    break  

                human_interaction(self.page)
                next_button.scroll_into_view_if_needed()
                next_button.click()

            except Exception as e:
                print(traceback.format_exc())
                break

        return storage

    
        
    def _scrape_agent_detail(self, page2, url):
        retries = 0
        while retries < 3:
            try:
                page2.goto(url, wait_until="domcontentloaded")
                captcha_checker(page2)
                page2.wait_for_selector('script[id="__NEXT_DATA__"][type="application/json"]', state="attached")
                human_interaction(page2)
                return extract_page(page2, "detail")
            except TimeoutError:
                page2.reload(wait_until="domcontentloaded")
                retries += 1
        print("Failed to load page after retries.")
        