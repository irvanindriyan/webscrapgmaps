#pip install googlemaps
#pip install win10toast
#pip install pandas
#pip install selenium
#run run.py

browserPath = r'chromedriver'
logFile = 'mapscrapping.log'
dataLen = 21
textPlace = 'Toko Besi & Toko Bangunan'
textRegion = 'Kota Semarang'
baseUrl = 'http://www.google.com/maps/search/'
headers = [
    'Nama', 'Alamat', 'Kota / Kabupaten', 'Provinsi',
    'Kode POS', 'Telepon', 'Mobile Phone', 'Website', 'Rating', 'Review'
]
waitTime = 3
timeOut = 2

placeName = '//*[@id="pane"]/div/div[1]/div/div/div[2]/' \
    'div[1]/div[1]/div[1]/h1/span[1]'
placeAddress = 'place_gm_blue_24dp'
placeCode = 'ic_plus_code'
placeContact = 'phone_gm_blue_24dp'
placeWebsite = 'public_gm_blue_24dp'
placeRating = '//*[@id=\"pane\"]/div/div[1]/div/div/div[2]/div[1]/' \
    'div[1]/div[2]/div/div[1]/div[2]/span/span/span'
placeReview = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/' \
    'div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button'

firstResult = '//*[@id="pane"]/div/div[1]/div/div/div[last()]/' \
    'div[1]/div[3]/div/a'
bottomPane = '//*[@id="bottom-pane"]/div/div[1]/' \
    'div/div[1]/div/div/div/div[2]/div[2]/div'
nextPane = '//*[@id="bottom-pane"]/div/div[1]/' \
    'div/div[1]/div/div/div/button[2]'
nextPage = '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/' \
    'div[last()]/div[2]/div/div[1]/div/button[2]'
backButton = '//*[@id="omnibox-singlebox"]/div[1]/div[1]/button'
