import requests
import pandas as pd

def crawl_movie_quote():
    url = 'https://movie-quote-api.herokuapp.com/v1/quote/'
    response = requests.get(url)
    data = response.json()
    return data

if __name__ == '__main__':
    quotes_list = []
    for i in range(100):
        quote = crawl_movie_quote()
        quotes_list.append(quote)
    quotes_df = pd.DataFrame(quotes_list)
    quotes_df.drop_duplicates(keep=False,inplace=True)
    quotes_df.to_csv('Quotes_.csv', index =False)
    

