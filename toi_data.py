
""" Scrapping TOI data from links"""

toi = "http://timesofindia.indiatimes.com/business/india-business/Send-Money-to-India-the-safe-convenient-inexpensive-way/articleshow/11079712.cms"

page = requests.get(toi)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

""" Gets the text of the article  of TOI """

for item in soup.find_all('div', class_="Normal"):
    print(item.get_text())

""" Gets the heading of link """

soup.find('h1', class_="heading1").get_text()
