from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from bs4 import BeautifulSoup
import json

username = 'SPusername'
password = 'SPpassword'
endpoint = 'gate.smartproxy.com'
port = '7000'
website = 'https://www.yelp.com/search?find_desc=Cafe&find_loc=New%20Orleans,%20LA'

chrome_options = webdriver.ChromeOptions()

proxies_extension = proxies(username, password, endpoint, port)

chrome_options.add_extension(proxies_extension)
chrome_options.add_argument("--headless=new")


chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
chrome.get(website)

html = chrome.page_source

def main():
    
    soup = BeautifulSoup(html, "html.parser")

    # Select div containing data points

    div_tags = soup.find_all('div', class_='padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border-color--default__09f24__NPAKY')

    # Extract data points

    data = []
    for div_tag in div_tags:
        
        name_tags = div_tag.find_all('a', class_="css-19v1rkv")
        name_text = [name_tag.text for name_tag in name_tags]

        inline_tags = div_tag.find_all('a', class_="css-abnp9g")
        inline_text = [inline_tag.text for inline_tag in inline_tags]

        price_tags = div_tag.find_all('span', class_="priceRange__09f24__mmOuH css-1s7bx9e")
        price_text = [price_tag.text for price_tag in price_tags]

        rating_tags = div_tag.find_all('span', class_="css-chan6m")
        rating_text = [rating_tag.text for rating_tag in rating_tags]

        rating1_tags = div_tag.find_all('div', class_="five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY")
        rating1_text = [rating1_tag['aria-label'] for rating1_tag in rating1_tags]


        element = {
            "Name": name_text,
            "Price": price_text,
            "Inline": inline_text,
            "StarRating": rating1_text,
            "RatingsCount": rating_text[0],
            "Location": rating_text[1e]

        }
        data.append(element)

    # Save data to JSON

    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
