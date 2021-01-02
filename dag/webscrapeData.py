###########################
#import modules
###########################
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def get_data():
    #URL of Steam's Specials
    page_url = "https://store.steampowered.com/search/?specials=1"

    # opens the connection and downloads html page from url
    uClient = uReq(page_url)

    # parses html into a soup data structure to traverse html as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()

    # finds each product from the store page
    containers = page_soup.findAll("div",{"class":"responsive_search_name_combined"})

    # name the output file to write to local disk
    out_filename = "steam_special_offers.csv"
    # headers of csv file to be written
    headers = "Title,Release_Date,Reviews,Original_Price ($),Percent_Discount (%),Discounted_Price ($)\n"

    # opens file, and writes headers
    f = open(out_filename, "w")
    f.write(headers)

    contain = containers[0]
    container = containers[0]

    # loops over each product and grabs attributes about each product
    for container in containers:

        title = container.span.text.replace(",",".")

        date_container = container.findAll("div", {"class": "col search_released responsive_secondrow"})
        release_date = date_container[0].text

        discountHolder = container.findAll("div", {"class": "col search_discount responsive_secondrow"})
        percent_discount = discountHolder[0].text.strip()

        try:
            reviews = (container.find('div', {'class': 'col search_reviewscore responsive_secondrow'}).span[
                       'data-tooltip-html'].split('<br>'))[0]
        except Exception as e:
            reviews = ''

        try:
            original_price = container.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}). \
                find('div', {'class': 'col search_price responsive_secondrow'}).text.strip()
        except Exception as e:
            try:
                original_price = container.find('div',
                                                {'class': 'col search_price_discount_combined responsive_secondrow'}). \
                    find('div', {'class': 'col search_price discounted responsive_secondrow'}).span.strike.text
            except Exception as e:
                original_price = ''

        PriceHolder = container.findAll("div", {"class": "col search_price discounted responsive_secondrow"})
        try:
             PriceHolder = PriceHolder[0].text
             PriceHolder = PriceHolder.split("$")
             discountedPrice = PriceHolder[-1]

        except IndexError:
        #     normalPrice = "Null";
             discountedPrice = original_price.strip('$')



        f.write(title + "," + release_date.replace(",", ".") + "," + reviews + "," + original_price + "," + percent_discount + "," +discountedPrice + "\n")

    f.close()  # Close the file

