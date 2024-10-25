from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import selenium.common.exceptions

def scrape_hotels(soup):
    hotels_list = []

    hotel_cards = soup.find_all('div', {'data-testid': 'property-card'})
    print(f'Found {len(hotel_cards)} hotels on this page.')

    for hotel in hotel_cards:
        hotel_dict = {}

        # Hotel name
        hotel_name = hotel.find('div', {'data-testid': 'title'})
        hotel_dict['hotel'] = hotel_name.get_text(strip=True) if hotel_name else 'N/A'

        # Location
        location = hotel.find('span', class_='f4bd0794db b4273d69aa')
        hotel_dict['location'] = location.get_text(strip=True) if location else 'N/A'

        # Distance to center
        distance = hotel.find('span', string=lambda text: 'from centre' in text.lower() if text else False)
        hotel_dict['distance_to_center'] = distance.get_text(strip=True) if distance else 'N/A'

        # Review score
        review_score = hotel.find('div', {'data-testid': 'review-score'})
        if review_score:
            score_text = review_score.find('div').get_text(strip=True).split() if review_score.find('div') else None
            hotel_dict['score'] = score_text[1] if score_text and len(score_text) > 1 else 'N/A'
            
            review_summary = review_score.find('div', class_='b8ef7618fe')
            hotel_dict['review_summary'] = review_summary.get_text(strip=True) if review_summary else 'N/A'

            reviews_count = review_score.find('div', class_='d8eab2cf7f')
            hotel_dict['reviews_count'] = reviews_count.get_text(strip=True).split()[0] if reviews_count else 'N/A'
        else:
            hotel_dict['score'] = 'N/A'
            hotel_dict['review_summary'] = 'N/A'
            hotel_dict['reviews_count'] = 'N/A'

        # Room type
        room_type = hotel.find('span', class_='df597226dd')
        hotel_dict['room_type'] = room_type.get_text(strip=True) if room_type else 'N/A'

        # Bed type
        bed_type = hotel.find('span', string=lambda text: 'bed' in text.lower() if text else False)
        hotel_dict['bed_type'] = bed_type.get_text(strip=True) if bed_type else 'N/A'

        # Policies
        hotel_dict['breakfast'] = "Included" if "Breakfast included" in hotel.get_text() else "Not included"
        hotel_dict['cancellation_policy'] = "Free cancellation" if "Free cancellation" in hotel.get_text() else "No free cancellation"
        hotel_dict['prepayment_policy'] = "No prepayment needed" if "No prepayment needed" in hotel.get_text() else "Prepayment needed"

        # Rooms left
        rooms_left = hotel.find('div', string=lambda text: 'Only' in text and 'room left' in text if text else False)
        hotel_dict['rooms_left'] = rooms_left.get_text(strip=True) if rooms_left else 'N/A'

        hotels_list.append(hotel_dict)
        print(f"Collected data for hotel: {hotel_dict['hotel']}")

    return hotels_list

def scroll_and_load_more(driver, expected_count):
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_count = len(driver.find_elements("css selector", "div[data-testid='property-card']"))

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait a random amount of time between 3 and 7 seconds to load the page
        pause_time = random.randint(3, 7)
        print(f"Pausing for {pause_time} seconds to allow content to load...")
        time.sleep(pause_time)

        # Check for and click the "Load More Results" button using JavaScript
        try:
            load_more_button = driver.find_element("xpath", "//button[contains(text(),'Load more results')]")
            if load_more_button.is_displayed():
                print("Clicking 'Load More Results' button via JavaScript...")
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(pause_time)  # Give time for content to load
        except selenium.common.exceptions.NoSuchElementException:
            print("No 'Load More Results' button found.")

        # Calculate new scroll height and number of hotels loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        new_count = len(driver.find_elements("css selector", "div[data-testid='property-card']"))

        print(f"Currently loaded {new_count} hotels out of {expected_count}...")

        # If the scroll height and hotel count haven't changed, or all hotels are loaded, stop
        if (new_height == last_height and new_count == last_count) or new_count >= expected_count:
            print("No more hotels to load on this page, stopping scroll.")
            break

        last_height = new_height
        last_count = new_count

def navigate_pages(driver):
    all_hotels = []

    while True:
        scroll_and_load_more(driver, 257)
        
        # Parse current page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        hotels_list = scrape_hotels(soup)
        all_hotels.extend(hotels_list)

        # Attempt to find and click the "Next" button
        try:
            next_button = driver.find_element("css selector", "a[aria-label='Next page']")
            if next_button.is_displayed():
                print("Navigating to the next page...")
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
            else:
                print("No more pages to navigate.")
                break
        except selenium.common.exceptions.NoSuchElementException:
            print("Next page button not found or not clickable.")
            break

    return all_hotels

def main():
    checkin_date = '2024-08-31'
    checkout_date = '2024-09-01'

    print("Starting web scraping...")

    url = f'https://www.booking.com/searchresults.en-gb.html?label=en-az-booking-desktop-Oc6SXVIi3zR74vxUy1EKMgS652828998604%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9069514%3Ali%3Adec%3Adm&aid=2311236&ss=Baku%2C+Azerbaijan&ssne=Baku&ssne_untouched=Baku&efdco=1&lang=en-gb&src=searchresults&dest_id=-2705195&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=44073b66c2550270&checkin={checkin_date}&checkout={checkout_date}&group_adults=1&no_rooms=1&group_children=0&nflt=class%3D5%3Bht_id%3D204%3Bclass%3D4%3Bclass%3D3%3Bclass%3D2'

    options = Options()
    options.headless = False  # Set to True if you don't need a browser window to appear

    # Set the correct path to your chromedriver.exe
    service = Service(executable_path="C:/Users/dataa/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe")

    try:
        # Initialize the WebDriver
        print("Initializing WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)
        print("Navigating to Booking.com...")
        driver.get(url)

        # Navigate through all pages and load all hotels
        all_hotels = navigate_pages(driver)

        # Convert to DataFrame and save as CSV
        print("Saving data to CSV...")
        df = pd.DataFrame(all_hotels)
        df.to_csv('baku_hotels_info.csv', index=False)
        print("Data saved to baku_hotels_info.csv")

    except selenium.common.exceptions.NoSuchWindowException:
        print("The browser window was closed unexpectedly.")
    
    finally:
        try:
            driver.quit()
            print("Web scraping completed.")
        except:
            print("Driver already closed.")

if __name__ == '__main__':
    main()
