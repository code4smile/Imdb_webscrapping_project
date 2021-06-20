# Web-Scrapping of Imdb website to get top 250 Movies list

# Importing required Modules
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Downloading imdb top 250 movie and parsing using Beautifulsoup
top_250_movie_url = 'http://www.imdb.com/chart/top'
response = requests.get(top_250_movie_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Parsing movie title, Year, Url, Crew details and movie ratings
movie_title = [" " .join(tag.text.split()[1:-1]) for tag in soup.find_all('td',{'class':'titleColumn'})]
year = [int(tag.text.split()[-1][1:-1]) for tag in soup.find_all('td',{'class':'titleColumn'})]
urls = ['http://www.imdb.com'+ a.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
movie_ratings = [round(float(a.attrs.get('data-value')),2) for a in soup.select('td.posterColumn span[name=ir]')]

# Parsing the awards won or nominated by each movie using the above parsed url list
awards = []
for url in urls:
    next_page = requests.get(url)
    another_soup = BeautifulSoup(next_page.text,'html.parser')
    award_got = []
    for a in another_soup.find('span',{'class':'awards-blurb'}):
        a = a.string.split()
        if a:
            award_got.append(a)
        else:
            award_got.append(0)
    if len(award_got)==3:
        awards.append(" ".join(award_got[1]))
    elif len(award_got)==1:
        awards.append(" ".join(award_got[0]))
    print(awards)
print(awards)

    #if award_got:
    #    awards.append(' '.join(award_got[1]))

#print(awards)


# Getting the no. of top movies in each year through counter
no_of_top_movies_in_year = Counter(year)

#Release year of movies in which maximum movies hit the chart and its graph
s = no_of_top_movies_in_year.most_common(20)
df = pd.DataFrame(s, columns=['year', 'count'])
ax = df.plot.bar(x='year', y='count', rot=60)
plt.show()

#No. of movies in top_chart of director
director = [d.split(',')[0][:-7] for d in crew]
no_of_movies_of_each_director = Counter(director)
most_movies = no_of_movies_of_each_director.most_common(20)
d_m = pd.DataFrame(most_movies, columns=['director', 'count'])
ax2 = d_m.plot.bar(x='director', y='count', rot=90)
plt.show()

#movie-stars
movie_stars = [' '.join(s.split(',')[1:]) for s in crew]
print(movie_stars)

#Pandas dataframe showing the concised table of movies and its details
data = pd.DataFrame({'movie_title':movie_title,
                     'Year' : year,
                     'Director':director,
                     'Ratings':movie_ratings,
                     'crew': crew,
                     'Awards': awards,
                     'Url' : urls })


#print(data.head())
print(tabulate(data, headers = 'keys', tablefmt = 'psql'))

#Data types of dataframe
print(data.dtypes)
