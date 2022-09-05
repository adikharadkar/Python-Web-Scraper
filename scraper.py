from bs4 import BeautifulSoup
import requests

content = requests.get("https://ubuntu.com/security/notices").text
print(content)