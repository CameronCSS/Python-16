"""
This module is practicing web scraping using beautiful soup
"""
import bs4
import requests

def main():
    """
    Our main function scrapes the given website for basic information
    """
    result = requests.get('https://www.videoschool.com/')

    soup = bs4.BeautifulSoup(result.text, 'html.parser')

    title = soup.select('title')[0].getText()

    print(title)

if __name__ == "__main__":
    main()