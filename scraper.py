from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

fileHandler = logging.FileHandler('scraper.log')
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-->%(levelname)s-->%(message)s')

# GET requests to the ubuntu.com/security/notices page
content = requests.get("https://ubuntu.com/security/notices").text

# Parsing the web page content
try:
	soup = BeautifulSoup(content, 'lxml')
except:
	logger.error("Data could not be extracted using BeautifulSoup() function")

# Extracting the title name of the web page
titleName = soup.title.text

# Extracting the first section of the webpage
# The first section contains the header and the summary
try:
	section = soup.find('section', class_='p-strip--suru-topped')
except:
	logger.error("Section tag not found!")

# Extracting the header i.e. "Ubuntu Security Notices"
try:
	header = section.find_all('div', class_='row')[0].div.h1.text
except IndexError:
	logger.error("Index out of range")
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
	logger.error("Index is out of range")
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

# LATEST NOTICES

# Extracting the whole section of articles
try:
	section_latest_notices = soup.find('section', class_='p-strip')
except:
	logger.error("Section tag of latest notices could not be extracted")

# Extracting the header i.e. "Latest Notices"
try:
	header_lates_notices = section_latest_notices.div.div.h2.text
except:
	header_lates_notices = None

# Extracting all the articles of latest notices
try:
	articles_latest_notices = section_latest_notices.div.div.find_all('article')
except:
	articles_latest_notices = None

lst_latest_notices = []
lst_latest_notice = []
print("-"*200)

# Extracting the name, link, date and summary of the latest notice
try:
	for article in articles_latest_notices:
		try:
			latest_notices_name = article.h3.text
		except:
			latest_notices_name = None
		try:
			latest_notices_link = article.h3.a['href']
		except:
			latest_notices_link = None
		try:
			latest_notices_date = article.find_all('p')[0].text
		except:
			latest_notices_date = None
		try:
			latest_notices_summary = article.find_all('p')[1].text
		except:
			latest_notices_summary = None
		
		lst_latest_notice = [latest_notices_name, latest_notices_link, latest_notices_date, latest_notices_summary]
		logger.info(lst_latest_notice)

		lst_latest_notices.append(lst_latest_notice)
except IndexError:
	logger.error("Index is out of range")
except:
	lst_latest_notices = None

# Extracting the Ubuntu Versions and storing them in a dictionary
dict_ubuntu_versions = {}
try:
	for article in articles_latest_notices:
		list_items = article.ul.find_all('li')
		try:
			for list_item in list_items:
				name = list_item.a.text
				link = list_item.a['href']
				dict_ubuntu_versions.update({name: link})
		except IndexError:
			logger.error("Index is out of range")
		except:
			dict_ubuntu_versions = None
except IndexError:
	logger.error('Index is out of range')
except:
	logger.error('Error - Ubuntu Versions')

# Extracting all the CVE IDs and storing them in a dictionary
dict_cve_ids = {}
try:
	for article in articles_latest_notices:
		try:
			latest_notices_cves = article.find_all('p')[2].small.find_all('a')
		except:
			logger.error("CVE IDs not found!")
		try:
			for cve in latest_notices_cves:
				try:
					cve_name = cve.text
				except:
					cve_name = None

				try:
					cve_link = cve['href']
				except:
					cve_link = None
				dict_cve_ids.update({cve_name: cve_link})
		except IndexError:
			logger.error("Index is out of range")
		except:
			dict_cve_ids = None
except IndexError:
	logger.error("Index is out of range")
except:
	dict_cve_ids = None

# Printing the header, summary and links on the console
print("-"*200)
logger.info("Header = {}".format(header))
logger.info("Summary = {}".format(summary))
print("-"*200)
try:
	for link in links:
		logger.info("Link: {}".format(link))
except IndexError:
	logger.error("List index out of range")
except:
	logger.warning("Links = {}".format(None))
print("-"*200)
# print(lst_latest_notice)
logger.info("UBUNTU VERSION - {}".format(dict_ubuntu_versions))
print("-"*200)
logger.info("CVE IDs: {}".format(dict_cve_ids))
