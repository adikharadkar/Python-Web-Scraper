from bs4 import BeautifulSoup
import requests

# GET requests to the ubuntu.com/security/notices page
content = requests.get("https://ubuntu.com/security/notices").text

# Parsing the web page content
try:
	soup = BeautifulSoup(content, 'lxml')
except:
	print("Data could not be extracted using BeautifulSoup() function")

# Extracting the title name of the web page
titleName = soup.title.text

# Extracting the first section of the webpage
# The first section contains the header and the summary
try:
	section = soup.find('section', class_='p-strip--suru-topped')
except:
	print("Section tag not found!")

# Extracting the header i.e. "Ubuntu Security Notices"
try:
	header = section.find_all('div', class_='row')[0].div.h1.text
except IndexError:
	print("Index out of range")
	header = None
except:
	header = None

# Extracting the summary
try:
	summaries = section.find_all('div', attrs={"class": "row"})[1].div.find_all('p')
	summary = ''
	for smry in summaries:
		summary += smry.text
except IndexError:
	print("Index is out of range")
	summary = None
except:
	summary = None

# Extracting the links from the summary if the summary exists
if summary is not None:
	try:
		p_tags = section.find_all('div', class_="row")[1].div.find_all('p')
		links = []
		for p_tag in p_tags:
			link = p_tag.find('a')['href']
			links.append(link)
	except:
		links = None

# Printing the header, summary and links on the console
print("Header = {}".format(header))
print("Summary = {}".format(summary))

try:
	for link in links:
		print(link)
except IndexError:
	print("List index out of range")
except:
	print("Links = {}".format(None))