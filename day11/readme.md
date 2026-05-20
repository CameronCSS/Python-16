# Web Scraping with BeautifulSoup

## Basic Usage
```python
import bs4
import requests

result = requests.get('https://www.example.com', timeout=5)
soup = bs4.BeautifulSoup(result.text, 'html.parser')
```

## Selectors (`soup.select`)

| Character | Syntax                       | Result                                                                      |
|-----------|------------------------------|-----------------------------------------------------------------------------|
| ""        | soup.select('div')           | All the elements with the 'div' label                                       |
| #         | soup.select('#style_4')      | Elements that contain id='style4'                                           |
| .         | soup.select('.right_column') | Elements that contain class='right_column'                                  |
| (SPACE)   | soup.select('div span')      | Any element called 'span' inside a 'div' element                            |
| >         | soup.select('div>span')      | Any element called 'span' directly inside a 'div' element, with nothing in between |

## Common Methods

| Method                        | Result                                  |
|-------------------------------|-----------------------------------------|
| soup.select('tag')[0]         | First matching element                  |
| element.getText()             | Inner text of an element                |
| element.getText(strip=True)   | Inner text with whitespace removed      |
| element.get('href')           | Value of an attribute (e.g. href, id)   |
| element.get('class')          | Returns list of class names             |
| soup.find('div')              | First matching element                  |
| soup.find_all('div')          | All matching elements as a list         |

## Error Handling
```python
try:
    result = requests.get(url, timeout=5)
    result.raise_for_status()  # Catches 4xx/5xx errors
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print("HTTP error:", e)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
```

## Tips
- Use `timeout=5` to avoid hanging requests
- Some sites block scrapers — try removing headers if you get a 403
- Always check the final URL with `result.url` to detect redirects
- `soup.select()` returns a **list**; use `[0]` to get the first result
- `find()` returns a single element; `find_all()` returns a list of all found