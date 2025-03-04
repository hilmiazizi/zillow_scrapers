import time
import random
import traceback
import json

def fill_form(page, element, text):
    element.scroll_into_view_if_needed()
    element.click()
    for char in text:
        element.press(char)
        time.sleep(random.uniform(0.05, 0.2))
    element.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    
def captcha_checker(page):
    try:
        while True:
            if page.locator("text=Press & Hold to confirm").is_visible(timeout=2000):
                page.wait_for_timeout(2000)
            else:
                break
    except:
        return
      
def human_interaction(page, min_sleep=1, max_sleep=2):
    time.sleep(random.uniform(0.05, 0.1))

    viewport = page.viewport_size or {"width": 1920, "height": 1080}
    screen_width, screen_height = viewport["width"], viewport["height"]

    if random.random() > 0.3:
        scroll_amount = random.randint(400, viewport["height"])
        page.mouse.wheel(0, scroll_amount)
        time.sleep(random.uniform(0.5, 1.2))

    start_x, start_y = random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)
    end_x, end_y = random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)
    steps = random.randint(25, 35)

    for i in range(steps):
        t = (i + 1) / steps
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.015, 0.045))

    sleep_time = random.uniform(min_sleep, max_sleep)
    time.sleep(sleep_time)

def extract_page(page, mode):
    storage = []
    if mode == 'list':
        try:
            result = page.locator('script[id="__NEXT_DATA__"][type="application/json"]').inner_html()
            result = json.loads(result)
            data = result['props']['pageProps']['proResults']['results']['professionals']
        except:
            print(traceback.format_exc())
            return None

        for line in data:
            business_name = line['businessName']
            full_name = line['fullName']
            profile_url = 'https://zillow.com'+line['profileLink']
            photo = line['profilePhotoSrc']
            reviews = line['numTotalReviews']
            rating = line['reviewStarsRating']
            sale_count_all = line['saleCountAllTime']
            sale_count_year = line['saleCountLastYear']
            sale_min_range = line['salePriceRangeThreeYearMin']
            sale_max_range = line['salePriceRangeThreeYearMax']
            top_agent = line['isTopAgent']
            agent_dict = {
                'business_name': business_name,
                'full_name': full_name,
                'profile_url': profile_url,
                'photo': photo,
                'reviews': reviews,
                'rating': rating,
                'sale_count_all': sale_count_all,
                'sale_count_year': sale_count_year,
                'sale_min_range': sale_min_range,
                'sale_max_range': sale_max_range,
                'top_agent': top_agent
            }
            storage.append(agent_dict)
    return storage