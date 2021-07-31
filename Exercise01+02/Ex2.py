'''
Write a program to shorten an input URL by using an external API. You could
consider to use this API: https://cleanuri.com/api/v1/shorten.
'''

import requests
import pandas as pd

def shorten(URL):
    url = 'https://cleanuri.com/api/v1/shorten'
    response = requests.post(url, data = {'url': URL})
    data = response.json()
    print(data)

if __name__ == '__main__':
    shorten(URL= 'https://flask.palletsprojects.com/en/2.0.x/#user-s-guide')
