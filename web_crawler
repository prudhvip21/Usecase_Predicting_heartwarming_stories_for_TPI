import urllib2
from bs4 import BeautifulSoup
from time import  sleep

# Provide base url which is ideally list of pages of articles in base_url , define start_page as starting page number and end_page as ending page number - script will crawl through all these pages, recursively read articles and writes creates data_dump.txt
start_page = 1
end_page = 1
base_url = 'https://www.firstpost.com/category/politics/page/'
dump_file_name_with_path = "./data_dump.txt"



# for some reason function is not returing BS datatype through return - not using userdefined function for now

links_page_count = 0
for page_num in range(start_page, end_page + 1):

    sleep(10)

    page_url = base_url + str(page_num)
    page = urllib2.urlopen(page_url)
    page_html = page.read()
    page.close()
    page_soup_links = BeautifulSoup(page_html, "html.parser")

    links_list = page_soup_links.findAll("a", {"class": "list-item-link"}, href=True)
    print "Initiating search on link page number :" + str(links_page_count)
    links_page_count += 1
    url_counter = 0

    for url_ip in range(0, (len(links_list))):

        sleep(20)
        print "reading article number :" + str(url_counter)
        url_counter += 1
        page = urllib2.urlopen(str(links_list[url_ip]['href']))
        page_html = page.read()
        page.close()
        page_soup = BeautifulSoup(page_html, "html.parser")

        # pick heading here

        containers = page_soup.findAll("h1", {"class": "page-title article-title"})
        len(containers)
        heading = containers[0].text.strip()

        # pick body here

        containers = page_soup.findAll("div", {"class": "article-full-content"})

        # remove unnecessary div tags

        for div in containers[0].findAll('div'):
            div.decompose()

        article = containers[0].text

        text = heading + "|" + article
        text = text.replace('\n', ' ')

        # type cast utf 16 characterset

        text = text.encode('utf-8')

        # write to a file
        print "writing to file"

        f = open(dump_file_name_with_path, "a")
        f.write(text + '\n')
        f.close()














