from mapsscrapping import GoogleMapsScraper
from win10toast import ToastNotifier
import app

searchPlace = input('Input place: ')
searchRegion = input('Input region: ')
search = (searchPlace+' IN '+searchRegion)
searchName = searchPlace+' '+searchRegion
searchText = search.replace(' ', '+')
queryLen = int(input('Number of result(s): '))
fileName = searchName+'.csv'

with GoogleMapsScraper(debug=True) as bot:
    bot.search_query(searchText)
    bot.write_data(app.headers, fileName)
    url = bot.identify_url()
    if url == 'place':
        bot.get_place_data(fileName)
    elif url == 'search':
        bot.get_places_data(fileName, queryLen)

toaster = ToastNotifier()
toaster.show_toast('Google Maps Scraper', 'Scrapping Google Maps '+searchName+' Complete')