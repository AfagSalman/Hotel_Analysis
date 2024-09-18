import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

def scrape_reviews(soup):
    reviews_list = []
    review_blocks = soup.find_all('li', class_='review_item')
    
    for review in review_blocks[:25]:  # Limiting to the first 25 reviews
        review_dict = {}
        
        # Review text
        review_text = review.find('span', itemprop='reviewBody')
        review_dict['review_text'] = review_text.get_text(strip=True) if review_text else 'N/A'
        
        # Review score
        review_score = review.find('span', class_='review-score-badge')
        review_dict['review_score'] = review_score.get_text(strip=True) if review_score else 'N/A'
        
        # Review date
        review_date = review.find('p', class_='review_item_date')
        review_dict['review_date'] = review_date.get_text(strip=True) if review_date else 'N/A'
        
        # Reviewer's name
        reviewer_name = review.find('p', class_='reviewer_name')
        review_dict['reviewer_name'] = reviewer_name.get_text(strip=True) if reviewer_name else 'N/A'
        
        # Reviewer country
        reviewer_country = review.find('span', class_='reviewer_country')
        review_dict['reviewer_country'] = reviewer_country.get_text(strip=True) if reviewer_country else 'N/A'
        
        reviews_list.append(review_dict)
        print(f"Collected review with score: {review_dict['review_score']}")
    
    return reviews_list

def main():
    urls = {
        "Solo Hotel": "https://www.booking.com/reviews/az/hotel/solo.en-gb.html",
        "Premium Park Hotel": "https://www.booking.com/reviews/az/hotel/premium-park-baku.en-gb.html",
        "Nord West Hotel": "https://www.booking.com/reviews/az/hotel/nord-west-baku.en-gb.html",
        "Bristol Hotel": "https://www.booking.com/reviews/az/hotel/bristol-baku.en-gb.html",
        "The Merchant Baku": "https://www.booking.com/reviews/az/hotel/the-merchant-baku.en-gb.html",
        "Parkside Hotel & Apartments": "https://www.booking.com/reviews/az/hotel/parkside-amp-apartments.en-gb.html",
        "NOBEL Hotel": "https://www.booking.com/reviews/az/hotel/nobel-baku.en-gb.html",
        "Grand Hotel Baku Central Park": "https://www.booking.com/reviews/az/hotel/grand-central-park-baku.en-gb.html",
        "Parallel Hotel": "https://www.booking.com/reviews/az/hotel/parallel.en-gb.html",
        "Baku Panorama Hotel": "https://www.booking.com/reviews/az/hotel/baku-panorama.en-gb.html",
        "Perla De Mar Hotel": "https://www.booking.com/reviews/az/hotel/perla-de-mar-baku.en-gb.html",
        "Jupiter": "https://www.booking.com/reviews/az/hotel/jupiter-baku.en-gb.html",
        "Pilot Baku hotel": "https://www.booking.com/reviews/az/hotel/pilot-baku.en-gb.html",
        "Emerald Suite Hotel": "https://www.booking.com/reviews/az/hotel/emerald-suite.en-gb.html",
        "Citadel Hotel Baku": "https://www.booking.com/reviews/az/hotel/citadel-baku.en-gb.html",
        "Premier Hotel": "https://www.booking.com/reviews/az/hotel/premier-baku.en-gb.html",
        "Sebail Inn Hotel": "https://www.booking.com/reviews/az/hotel/sebail-inn.en-gb.html",
        "Supreme Hotel Baku": "https://www.booking.com/reviews/az/hotel/supreme-baku.en-gb.html",
        "West Shine Hotel": "https://www.booking.com/reviews/az/hotel/west-shine-baku.en-gb.html",
        "Pera Hotel Baku": "https://www.booking.com/reviews/az/hotel/pera-baku.en-gb.html",
        "Deniz Inn Hotel": "https://www.booking.com/reviews/az/hotel/deniz-inn.en-gb.html",
        "Modern Hotel": "https://www.booking.com/reviews/az/hotel/modern-baku.en-gb.html",
        "West Palace by Antique Hotel": "https://www.booking.com/reviews/az/hotel/west-palace-by-antique.en-gb.html",
        "SERA Hotel": "https://www.booking.com/reviews/az/hotel/sera.en-gb.html",
        "Alp Inn Hotel": "https://www.booking.com/reviews/az/hotel/alp-inn.en-gb.html",
        "Malakan Hotel Baku City": "https://www.booking.com/reviews/az/hotel/malakan-city.en-gb.html",
        "White Boutique Nizami Hotel": "https://www.booking.com/reviews/az/hotel/white-boutique-nizami.en-gb.html",
        "Sunday Palace Hotel": "https://www.booking.com/reviews/az/hotel/sunday-palace-baku.en-gb.html",
        "Safran Hotel": "https://www.booking.com/reviews/az/hotel/safran.en-gb.html",
        "Ammar Grand Hotel": "https://www.booking.com/reviews/az/hotel/ammar-grand.en-gb.html",
        "Alison Hotel": "https://www.booking.com/reviews/az/hotel/alison-baku.en-gb.html",
        "Swan Hotel Baku": "https://www.booking.com/reviews/az/hotel/swan.en-gb.html",
        "Khegany Mall Hotel": "https://www.booking.com/reviews/az/hotel/khegany-mall.en-gb.html",
        "Manor Luxury Hotel Baku": "https://www.booking.com/reviews/az/hotel/manor-luxury-baku.en-gb.html",
        "Harmony Hotel Baku": "https://www.booking.com/reviews/az/hotel/harmony-baku.en-gb.html",
        "Art Club": "https://www.booking.com/reviews/az/hotel/art-club.en-gb.html",
        "Baku Marriott Hotel Boulevard": "https://www.booking.com/reviews/az/hotel/baku-marriott-hotel-boulevard.en-gb.html",
        "Sheraton Baku Intourist": "https://www.booking.com/reviews/az/hotel/sheraton-baku-intourist.en-gb.html",
        "Volga Hotel Baku": "https://www.booking.com/reviews/az/hotel/volga-baku.en-gb.html",
        "West inn Hotel & Restaurant": "https://www.booking.com/reviews/az/hotel/west-inn.en-gb.html",
        "Premier Palace Baku": "https://www.booking.com/reviews/az/hotel/premier-palace-baku.en-gb.html",
        "Fairmont Baku, Flame Towers": "https://www.booking.com/reviews/az/hotel/fairmont-baku-flame-towers.en-gb.html",
        "ALBA HOTEL & SPA": "https://www.booking.com/reviews/az/hotel/alba-spa.en-gb.html",
        "Hilton Baku": "https://www.booking.com/reviews/az/hotel/hilton-baku.en-gb.html",
        "The Ritz-Carlton, Baku": "https://www.booking.com/reviews/az/hotel/the-ritz-carlton-baku.en-gb.html",
        "Lake Palace Baku": "https://www.booking.com/reviews/az/hotel/lake-palace-baku.en-gb.html",
        "JW Marriott Absheron Baku Hotel": "https://www.booking.com/reviews/az/hotel/jw-marriott-absheron-baku.en-gb.html",
        "InterContinental Baku, an IHG Hotel": "https://www.booking.com/reviews/az/hotel/intercontinental-baku.en-gb.html",
        "Promenade Hotel Baku": "https://www.booking.com/reviews/az/hotel/promenade-baku.en-gb.html",
        "Sapphire City Hotel": "https://www.booking.com/reviews/az/hotel/sapphire-city-baku.en-gb.html",
        "Wyndham Baku": "https://www.booking.com/reviews/az/hotel/wyndham-baku.en-gb.html",
        "Sapphire Hotel": "https://www.booking.com/reviews/az/hotel/sapphire.en-gb.html",
        "Ivy Garden Hotel Baku": "https://www.booking.com/reviews/az/hotel/ivy-garden.en-gb.html",
        "Hyatt Regency Baku": "https://www.booking.com/reviews/az/hotel/hyatt-regency-baku.en-gb.html",
        "Musafir by Lara": "https://www.booking.com/reviews/az/hotel/musafir-by-lara.en-gb.html",
        other hotel names...
    }
    
    options = Options()
    options.headless = False
    service = Service(executable_path="C:/Users/dataa/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        for hotel_name, url in urls.items():
            print(f"Navigating to {hotel_name} reviews page...")
            driver.get(url)
            time.sleep(3)  # Allow time for the page to load
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            reviews_list = scrape_reviews(soup)
            
            # Convert to DataFrame and save as CSV
            df = pd.DataFrame(reviews_list)
            filename = f"{hotel_name.replace(' ', '_').lower()}_reviews.csv"
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
    
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
