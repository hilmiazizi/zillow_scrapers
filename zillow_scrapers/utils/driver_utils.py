import time
import random
import traceback
import json

def fill_form(page, element, text):
    page.wait_for_load_state("domcontentloaded")
    human_interaction(page)
    element.click()
    time.sleep(random.uniform(0.5, 1))
    element.click()
    for char in text:
        element.press(char)
        time.sleep(random.uniform(0.05, 0.2))
    element.press("Enter")
    time.sleep(1)
    page.wait_for_load_state("domcontentloaded")
    
def captcha_checker(page):
    while True:
        meta_description = page.locator('meta[name="description"]').get_attribute("content")
        page_title = page.title()
        captcha_visible = page.locator('div[id="px-captcha-wrapper"]').count() > 0

        if (meta_description and "px-captcha" in meta_description.lower()) or \
           ("Access to this page has been denied" in page_title) or \
           captcha_visible or ("Human Verification" in page_title):
            page.wait_for_timeout(2000)
        else:
            break


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
    elif mode == "detail":
        try:
            result = page.locator('script[id="__NEXT_DATA__"][type="application/json"]').inner_html()
            result = json.loads(result)

            data = result['props']['pageProps']['displayUser']

            address_parts = [data['businessAddress'][x] if data['businessAddress'][x] else "" for x in data['businessAddress'].keys()]
            phone_parts = [data['phoneNumbers'][x] if data['phoneNumbers'][x] else "" for x in data['phoneNumbers'].keys()]
            try:
                website = result['props']['pageProps']['getToKnowMe']['websiteUrl']
            except:
                website = None
            address = ", ".join(filter(None, address_parts))
            phone = " - ".join(filter(None, phone_parts))

            email = data['email']
            
            agent_dict = {
                "address" : address,
                "phone": phone,
                "email": email,
                "website": website
            }

            return agent_dict

        except Exception:
            print(traceback.format_exc())
            return None, None, None
    return storage