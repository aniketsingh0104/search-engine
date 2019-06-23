import requests
from bs4 import BeautifulSoup
import xlsxwriter
import os
url_prefix = "https://curlie.org"
cat = "Categories ->\n\n"

# Trims input URL and returns category
def trim_for_category(str):
    lens = len(str)
    finals = ""
    index = 0
    for i in range(0, lens, 1):
        if str[i] == '/':
            index = i

    finals = str[index + 1:]
    return finals

# Scraps complete page at current depth and then enters into depth +1 to repeat same.
#CURRENTLY GOING TILL DEPTH = 2
def scrap(url, genre, depth):
    if depth > 2:
        return
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, "html.parser")
    # To Find all site URL on current webpage - >
    sites = soup.find_all('div', {'class': 'site-item'})
    # Check if any sites are present
    if (len(sites) > 0):
        data = "Title Link Description"
        workbook = xlsxwriter.Workbook("data/" + genre + '.xlsx')
        worksheet = workbook.add_worksheet()
        row = 1 # denotes row in which text will be written
        worksheet.write('A' + str(row), 'Title')
        worksheet.write('B' + str(row), 'Link')
        worksheet.write('C' + str(row), 'Description')
        row = row + 1
        for site in sites:
            curr = site.find('div', {'class': 'title-and-desc'})
            curr_a = curr.find('a')
            link = curr_a['href']
            title = curr_a.find('div').text
            description = (curr.find('div', {'class': 'site-descr'}).text).strip();
            worksheet.write('A' + str(row), title)
            worksheet.write('B' + str(row), link)
            worksheet.write('C' + str(row), description)
            row = row + 1
            print (title + " " + link + " " + description)
        workbook.close()
    global cat
    # To Find all SubCategories and URLs ->
    divs = soup.find('div', {'id': 'subcategories-div'})
    if divs is not None:
        if (len(divs) > 0):
            special_divs = divs.find_all('div', {'class': 'cat-item'})
            for a_text in special_divs:
                links = a_text.find_all('a')
                for final_text in links:
                    hrefText = (final_text['href'])
                    category = trim_for_category(hrefText[:len(hrefText) - 1])
                    cat = cat + category + "\n"
                    temp = url_prefix + hrefText
                    scrap(temp, category, depth + 1)
    
if __name__=="__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    scrap("https://curlie.org/Computers", "computers", 1)
    print(cat)
    file = open("data/categories.txt", "w")
    file.write(cat)
    file.close()