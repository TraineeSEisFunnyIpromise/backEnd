from  selenium import webdriver
from bs4 import BeautifulSoup
from flask import Flask, render_template
import amazon_scraper
app = Flask(__name__)
@app.route('/')
def image():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Web Driver\chromedriver.exe')
    url = 'https://www.amazon.com/s?k='
    search = 'smartphone' 
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    search_area = soup.findAll('div', 'a-section a-spacing-medium')
    return render_template('withImage.html', area = search_area)

@app.route('/without_image')
def without_image():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browserdriver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Web Driver\chromedriver.exe')
    url = 'https://www.amazon.com/s?k='
    search = 'smartphone'
    browserdriver.get(url+search)
    content = browserdriver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    search_area = soup.findAll('div', 'a-section a-spacing-medium')
    return render_template('withoutImage.html', area = search_area)

if __name__ == '__main__':
    app.run(debug=True)


