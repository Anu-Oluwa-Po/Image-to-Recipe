import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium with Chrome
options = Options()
options.add_argument("--headless")  # Runs browser in background
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_images(search_term, num_images, save_dir):
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_term}"
    driver.get(search_url)

    # Scroll down to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # wait for images to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or len(driver.find_elements('css selector', "img")) > num_images:
            break
        last_height = new_height

    # Parse page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all('img')
    urls = []
    for img in img_tags:
        try:
            url = img['src']
            if url.startswith('http'):
                urls.append(url)
        except:
            continue
        if len(urls) >= num_images:
            break

    print(f"Found {len(urls)} images for {search_term}")

    # Save images
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, url in enumerate(urls):
        try:
            img_data = requests.get(url).content
            with open(os.path.join(save_dir, f"{search_term}_{i+1}.jpg"), 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            print(f"Could not download {url} - {e}")

# Example usage:
search_terms = ['Nigeria Fried rice', 'Gizdodo (Gizzard and Plantain)',
    'Efo Riro (Vegetable Soup)', 'Bole and Fish (Roasted Plantain and Fish)',
    'Meat-pie', 'Kilishi', 'Fura da Nono (Milk and Millet)', 'Nsala soup',
    'Ofe Nsala (White Soup)', 'Fiofio and Yam (Pigeon Peas)', 'Ofe Owerri',
    'Ogbono Soup (Full)', 'Akara', 'Adalu (Beans and Corn)', 'Egusi Soup, (Full)',
    'Fried Plantains (dodo)', 'Miyan Kuka (Baobab Soup)',
    'Ayanfemi (Fried Yam)', 'Okpa (Bambara Nut Pudding)', 'Atama Soup',
    'Okro Stew', 'Chin Chin', 'Efo Riro', 'Puff Puff', 'Ewedu Soup',
    'Peppered Snails', 'Jollof Rice', 'Eba and Egusi Soup',
    'Buka Stew (Obe Ata)', 'Moi Moi', 'Ewa Agoyin', 'Banga Soup and Starch',
    'Miyan Taushe (Pumpkin Soup)', 'Iyan (Pounded Yam) and Efo Riro',
    'Corn (Agbado)', 'Miyan Karkashi', 'Nigeria Chapman',
    'Ekpang Nkukwo (Cocoyam Pottage)', 'Alkaki (Honey Dumplings)',
    'Nigeria ikokore', 'Amala, Gbegiri and ewedu', 'Pepper Soup with protein',
    'Zobo Drink (Hibiscus)', 'Nigeria groundnut soup',
    'Ji Mmiri Oku (Ukodo) - Yam Pepper Soup', 'Oha Soup',
    'Waina (Masa) - Rice pancake', 'Nkwobi (Cow Foot)',
    'Ofada Rice and Ayamase', 'Kunun Zaki (Sweet Millet Drink)',
    'Asaro (Yam Porridge)', 'Ogi (Pap) and Akara',
    'Abacha and Ugba (African Salad)', 'Afang Soup', 'Fisherman Soup', 'Suya',
    'Edikang Ikong', 'Palm Wine'
]

for term in search_terms:
    fetch_images(term, 500, f'test/{term}')

driver.quit()