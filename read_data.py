import pandas as pd
from ocr_hello import get_text_image
import requests
from bs4 import BeautifulSoup

def create_prompt(df, rownb):
    rownb= 1
    dict_info = dict(df.iloc[rownb])
    del dict_info['Image']
    image_link = "images/Picture{}.png".format(rownb+1)
    text_image = get_text_image(image_link)

    url = dict_info['Landing Page']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.body
    main_content = body.find_all("div", {"class": "main-container"})
    text_website= []
    for content in main_content:
        for el in content.stripped_strings:
            text_website.append(el)

    text_website_ = " ".join(text_website)

    prompt = "I have an ad with those informations" + str(dict_info) +"""\n I have extracted text on the associated image:
     """ + text_image +''''\n'''+"Can you first give me a matching score between 0 and 1 for matching the add to the " \
                                                            "website ? And improvement for better matching. ?" \
                                                            " Here is the landing page text scrapped: " + text_website_

    return prompt