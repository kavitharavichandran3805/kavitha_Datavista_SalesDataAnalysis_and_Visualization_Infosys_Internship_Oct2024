
from sample_chart import *

import requests 
from bs4 import BeautifulSoup as bs
from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

from datetime import datetime, timedelta
import time



def convert_relative_date(relative_date):
    current_date = datetime.now()

    if 'days ago' in relative_date:
        days_ago = int(relative_date.split()[0])
        converted_date = current_date - timedelta(days=days_ago)
    elif 'month ago' in relative_date or 'months ago' in relative_date:
        months_ago = int(relative_date.split()[0])
        converted_date = current_date - timedelta(days=30 * months_ago)
    else:
        converted_date = current_date

    formatted_date = converted_date.strftime('%d/%m/%Y')
    
    return formatted_date

def customer_reviews_flipkart(soup):
    reviews = []
    review_blocks = soup.find_all("div", class_="_27M-vq")
    for block in review_blocks:
        rating_element = block.find("img", class_="_1wB99o").find_parent()

        review_element = block.find("p", class_="_2-N8zT")
        comment_div = block.find("div", class_="t-ZTKy")
        p_elements = block.find("div", class_="row _3n8db9")
        
        if rating_element and review_element and comment_div and p_elements:
    
            comment_text = comment_div.find_all('div')[1].text
            a=p_elements.find_all('div')[0]
            b=a.find_all('p')[2]
            ratings = {
                'Ratings': rating_element.text,
                'Reviews': review_element.text,
                'Comments': comment_text,
                'Date': convert_relative_date(b.text)
            }
            reviews.append(ratings)
    return reviews

def customer_reviews_amazon(soup):
    reviews=[]
    review_blocks = soup.find_all("div", class_="a-section celwidget")
    for block in review_blocks:
        rating_element = block.find("span", class_="a-icon-alt").text
        rating = rating_element.split()[0]
        rating = rating.split('.')[0]
        review_element = block.find("span", class_="a-letter-space").find_next_sibling('span')
        comment_div = block.find('span', class_='a-size-base review-text review-text-content').find('span')
        date_div = block.find("span", class_="a-size-base a-color-secondary review-date").text
        date = date_div.split()[-3:] 
        date = ' '.join(date)
        original_date = datetime.strptime(date, '%d %B %Y')
        review_date = original_date.strftime('%d/%m/%Y')

        if rating_element and review_element and comment_div and date:

            ratings = {
                'Ratings': rating,
                'Reviews': review_element.text,
                'Comments': comment_div.text,
                'Date': review_date
            }
            reviews.append(ratings)
    return reviews





# url1='https://www.amazon.in/Samsung-Awesome-Iceblue-Storage-Nightography/product-reviews/B0CWPDYS2C/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
def start(url1):
    driver = webdriver.Chrome()   
    if 'product-reviews' in url1:
        product_reviews=[]
        next=True
        driver.get(url1)
        Thread.sleep(15)
        while next:
            soup= bs(driver.page_source,"html.parser")
            page_reviews=customer_reviews_amazon(soup)
            product_reviews.extend(page_reviews)
            try:
                next_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']/a")))
                if next_link.is_enabled():
                    next_link.click()
                    time.sleep(3)
                else:
                    next=False
            except (TimeoutException,ElementClickInterceptedException):
                time.sleep(3)
                try:
                    next_link = driver.find_element(By.XPATH, "//li[@class='a-last']/a")
                    next_link.click()
                    time.sleep(3)
                except NoSuchElementException:
                    next = False                
    else:
        product_reviews=None
       
    print(product_reviews)
    sentimental_score(product_reviews)