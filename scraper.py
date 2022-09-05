from bs4 import BeautifulSoup
import requests

content = requests.get("https://ubuntu.com/security/notices").text

try:
	soup = BeautifulSoup(content, 'lxml')
except:
	print("Data could not be extracted using BeautifulSoup() function")

titleName = soup.title.text
try:
	section = soup.find('section', class_='p-strip--suru-topped')
except:
	print("Section tag not found!")

try:
	header = section.find_all('div', class_='row')[0].div.h1.text
except IndexError:
	print("Index out of range")
	header = None
except:
	header = None

print(header)