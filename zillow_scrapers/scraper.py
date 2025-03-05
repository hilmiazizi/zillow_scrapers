from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import random
from typing import List, Dict, Any

from zillow_scrapers.typed_scraper.agent_scraper import AgentScraper

class ZillowScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        selected_os = random.choice(["Windows", "Linux", "Ubuntu","Mac OS X"])
        selected_ua = UserAgent(platforms='desktop', min_version=130.0, browsers=['Firefox'], os=selected_os).random
        headers = {
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133")',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": selected_os,
            "sec-fetch-storage-access": "active",
            "user-agent": selected_ua
        }
        self.browser = self.playwright.firefox.launch(
            headless=False,
            handle_sighup=True,
            handle_sigint=True,
            handle_sigterm=True,
            firefox_user_prefs={
                "webgl.disabled": False,
                "webgl.force-enabled": True,
                "webgl.min_capability_mode": False,
                "webgl.enable-debug-renderer-info": True,
                "privacy.resistFingerprinting": False,
                "general.useragent.override": selected_ua,
                "dom.webaudio.enabled": False,
                "media.peerconnection.enabled": False,
                "layout.css.devPixelsPerPx": random.choice(["1.0", "1.25", "1.5"])
            })
        self.context = self.browser.new_context(user_agent=selected_ua)
        self.context.set_extra_http_headers(headers)
        self.context.add_init_script(open('zillow_scrapers/js/fingerprint.js').read())


    def scrape(self, url: str):
        context = self.browser.new_context()
        page = context.new_page()
        page.goto(url)
        result = {"title": page.title()}
        context.close()
        return result

    def close(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except:
            return
        
    def search_agent(
        self,
        location:str,
        max_page:int = 25,
        get_contact:bool=False
    ) -> List[Dict[str, Any]]:
        return AgentScraper(self.context, location, max_page, get_contact)