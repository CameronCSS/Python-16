"""
This module is practicing web scraping using beautiful soup
"""
import bs4
import requests

def main():
    """
    Our main function scrapes the given website for basic information
    """
    try:
        result = requests.get('https://www.videoschool.com', timeout=5)
        result.raise_for_status()  # Raises an error for 4xx/5xx responses
        soup = bs4.BeautifulSoup(result.text, 'html.parser')
        title = soup.select('title')[0].getText()
        print("Title:", title)
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
