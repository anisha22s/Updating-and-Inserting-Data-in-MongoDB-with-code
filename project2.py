# -*- coding: utf-8 -*-
"""Untitled11.ipynb


"""


#################Regular Webscraping#################
#  program that searches on yellowpages.com for the top 30 “Pizzeria” in San Francisco.  Save each search result page to disk, “sf_pizzeria_search_page.htm”.

def X4():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
        'HTTP_CONNECTION':"keep-alive",
        'HTTP_ACCEPT':'*/*',
        'HTTP_ACCEPT_ENCODING':'gzip, deflate',
        'HTTP_HOST':'MyVeryOwnHost'}
    
    url= 'https://www.yellowpages.com/search?search_terms=pizzeria&geo_location_terms=San+Francisco%2C+CA'
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # save search result page to disk
    with open('sfS_pizzeria_search_page.htm', 'w') as f:
        f.write(response.text)
    
X4() 

# code that opens the search result page saved above and parses out all shop information (search rank, name, linked URL [this store’s 
#YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, 
#number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities
#IIE).  We will skip all “Ad” results.

# read in saved HTML file
def X5():
    with open('sfS_pizzeria_search_page.htm', 'r') as f:
        html = f.read()
    
    
    soup = BeautifulSoup(html, 'html.parser')
    
    shop_information =[]
    
    
    for shop in soup.find_all('div', class_='v-card'):
            ad_pill = shop.find('span', class_='ad-pill') #all ads have span with class ad-pill. condition to skip this shop if it has an ad-pill span
            if ad_pill is not None:
                continue
            link = shop.select_one('a.business-name')['href']
            link = 'https://www.yellowpages.com' + link
            rank = shop.select_one('h2.n').text.strip('.')
            rank_number = rank.split('.')[0]
            
            name = shop.select_one('a.business-name').text
            
            star_rating = shop.select_one('div.result-rating')
            if star_rating:
              star_rating = star_rating['class'][1]
            else:
              star_rating = None
            
            num_reviews = shop.select_one('span.count')
            if num_reviews:
              num_reviews = num_reviews.text
            else:
              num_reviews = None
              
            tripadvratingw= shop.select_one('div[data-tripadvisor]')  #data-tripadvisor attribute
            if tripadvratingw:
                 tripadvrating = json.loads(tripadvratingw['data-tripadvisor']) #the rating and count of TA are located in a JSON string
                 Ta_rating = tripadvrating.get('rating')

            else:
                  Ta_rating = None

              
            tripadvratingw= shop.select_one('div[data-tripadvisor]')  
            if tripadvratingw:
                 tripadvrating = json.loads(tripadvratingw['data-tripadvisor']) #the rating and count of TA are located in a JSON string
                 TA_rating_count = tripadvrating.get('count')
            else:                 
                  TA_rating_count = None
            

              
            pricerange = shop.select_one('div.price-range')
            if pricerange:
                pricerange = pricerange.text
            else:
                pricerange= None
                
            yrsinbusiness = shop.select_one('div.years-in-business')
            if yrsinbusiness:
                yrsinbusiness = yrsinbusiness.text
            else:
                yrsinbusiness= None
                
            review = shop.select_one('p.body.with-avatar')
            if review:
               review = review.text
            else:
                review= None
                
            amenities = shop.select_one('div.amenities-info')
            if amenities:
               amenities = amenities.text
            else:
                amenities= None
             
            shop_information.append({
             'rank': rank_number,        
             'link': link,
             'name': name,
             'star_rating': star_rating,
             'num_reviews': num_reviews,
             'tripadvrating' :Ta_rating,
             'TA_rating_count' : TA_rating_count,
             'pricerange': pricerange,
             'yrsinbusiness' : yrsinbusiness,
             'review' : review,
             'amenities' : amenities
           
             })
    print(shop_information)
    print(len(shop_information))
X5()


################# MongoDB#################
# Modifing the code to create a MongoDB collection called
# “sf_pizzerias” that stores all the extracted shop information, one document for each 
#shop.

def X6():

    # connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/') 
    db = client['sf_pizzerias'] #creating a database
    pizzacollection = db['sf_pizzerias'] #collection inside database 
    
    # read in saved HTML file
    with open('sfS_pizzeria_search_page.htm', 'r') as f:
        html = f.read()
    
    
    soup = BeautifulSoup(html, 'html.parser')
    
    for shop in soup.find_all('div', class_='v-card'):
            ad_pill = shop.find('span', class_='ad-pill') #all ads have span with class ad-pill. condition to skip this shop if it has an ad-pill span
            if ad_pill is not None:
                continue
            link = shop.select_one('a.business-name')['href']
            link = 'https://www.yellowpages.com' + link
            rank = shop.select_one('h2.n').text.strip('.')
            rank_number = rank.split('.')[0]
            
            name = shop.select_one('a.business-name').text
            
            star_rating = shop.select_one('div.result-rating')
            if star_rating:
              star_rating = star_rating['class'][1]
            else:
              star_rating = None
            
            num_reviews = shop.select_one('span.count')
            if num_reviews:
              num_reviews = num_reviews.text
            else:
              num_reviews = None
            
            tripadvratingw= shop.select_one('div[data-tripadvisor]')  #data-tripadvisor attribute
            if tripadvratingw:
                 tripadvrating = json.loads(tripadvratingw['data-tripadvisor']) #the rating and count of TA are located in a JSON string
                 Ta_rating = tripadvrating.get('rating')
            
            else:
                  Ta_rating = None
            
              
            tripadvratingw= shop.select_one('div[data-tripadvisor]')  
            if tripadvratingw:
                 tripadvrating = json.loads(tripadvratingw['data-tripadvisor']) #the rating and count of TA are located in a JSON string
                 TA_rating_count = tripadvrating.get('count')
            else:                 
                  TA_rating_count = None
              
            pricerange = shop.select_one('div.price-range')
            if pricerange:
                pricerange = pricerange.text
            else:
                pricerange= None
                
            yrsinbusiness = shop.select_one('div.years-in-business')
            if yrsinbusiness:
                yrsinbusiness = yrsinbusiness.text
            else:
                yrsinbusiness= None
                
            review = shop.select_one('p.body.with-avatar')
            if review:
               review = review.text
            else:
                review= None
                
            amenities = shop.select_one('div.amenities-info')
            if amenities:
               amenities = amenities.text
            else:
                amenities= None
             
            shop_information={
             'rank': rank_number,        
             'link': link,
             'name': name,
             'star_rating': star_rating,
             'num_reviews': num_reviews,
             'tripadvrating' :Ta_rating,
             'TA_rating_count' : TA_rating_count,
             'pricerange': pricerange,
             'yrsinbusiness' : yrsinbusiness,
             'review' : review,
             'amenities' : amenities
             
           
             }
            print(shop_information)
            
            # insert the shop information into the MongoDB collection
            pizzacollection.insert_one(shop_information)
X6()            
################# Parsing#################
##code that reads all URLs stored in “sf_pizzerias” and download each shop page.  
#Store the page to disk, “sf_pizzerias_[SR].htm” (replace [SR] with the search rank).


def X7():
    with open('sfS_pizzeria_search_page.htm', 'r') as f:
        html = f.read()
    
    
    soup = BeautifulSoup(html, 'html.parser')
    
    
    #we will create a list of each search result pizzeria page url
    link = []
    
    #loop through the list and append links to the list
    for i in soup.select('a.business-name'):
            href = i['href']
            link.append('https://www.yellowpages.com' + href)
      
       
    print(link)
    len(link)
    #on further inspection, looks like this is capturing 33 links instead of 30. the extra 3 are featured pizzerias. The first and the last 2 links are features
    #lets modify that
    new_link = link[1:31]
    
    print(new_link)
    len(new_link)
    
    for i in range(0,30):
        url = new_link[i]
        response = requests.get(url)
        filename = 'SFS_pizzerias_' + str(i+1) + '.htm'
        with open(filename, 'wb') as f:
            f.write(response.content)
        time.sleep(5) #delay between requests
X7()

#code that reads the 30 shop pages saved in (7) and parses each shop’s address, 
#phone number, and website.
def X8():
    for i in range(0, 30):
        filename = 'SFS_pizzerias_' + str(i+1) + '.htm'  #loop through each 30 files
        with open(filename, 'r') as f:
           
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(f, 'html.parser')
            name = soup.find('h1', {'class': 'business-name'}).text
            address = soup.find('span', {'class': 'address'}).text
            # Add a space before "San" in the address 
            address = re.sub(r"(San)", r" \1", address)
            phone = soup.find('p', {'class': 'phone'}).text
            website = soup.find('p', {'class': 'website'})
            if website:
                website = website.find('a')['href'] 
            else:
                website= None        
            #website = soup.find('a')['href']
            #print(f'Pizzeria {i+1}: {name} - {address}- {phone}- {website}')
            print({"rank":i+1,"name": name, "address": address, "phone": phone, "website": website})
                     
X8()

################# API#################
# We will Sign up for a free account with https://positionstack.com/ 
#The we will Copy above  code and  Modify the code to query each shop address’ geolocation (long, lat).  
#Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, 
#phone number, website, and geolocation.


def X9():
    client = MongoClient('mongodb://localhost:27017/')
    db = client["sf_pizzerias"]
    collection = db["sf_pizzerias"]      
    for i in range(0, 30):
        filename = 'SFS_pizzerias_' + str(i+1) + '.htm'  #loop through each 30 files
        with open(filename, 'r') as f:
           
            # Parse HTML with BeautifulSouphttps://www.google.com/url?q=https://www.google.com/chrome/?hl%3Den%26brand%3DMACD%26utm_source%3Dmacos%26utm_medium%3Dmaterial-callout%26utm_campaign%3Dgmail%26utm_content%3Dgoogle_recommends_search&source=hpp&id=19030389&ct=7&usg=AOvVaw0SwBkZsQxNRpQnrqnwIEzp&authuser=1
            url = 'http://api.positionstack.com/v1/forward'
            access_key = '49064c11a6b01718b6849e8bea4a854b'
            soup = BeautifulSoup(f, 'html.parser')
            rank = i+1
            name = soup.find('h1', {'class': 'business-name'}).text
            address = soup.find('span', {'class': 'address'}).text
            # Add a space before "San" in the address othersie the lattitude and longitude is coming wrong
            address = re.sub(r"(San)", r" \1", address)
            phone = soup.find('p', {'class': 'phone'}).text
            website = soup.find('p', {'class': 'website'})
            if website:
                website = website.find('a')['href'] 
            else:
                website= None
            params = {'access_key': access_key, 'query': address,  "country" :'US', 'region' : 'California' }
            response = requests.get(url, params=params)
            #json_response = response.json()
            #print(json.dumps(json_response, indent=2))  # print JSON response for debugging
            #latitude = response.json()['data'][0]['latitude'] 
            #longitude = response.json()['data'][0]['longitude']
            response_data = response.json()['data']
            for data in response_data:
                latitude = data['latitude']
                longitude = data['longitude']
                # do something with latitude and longitude

    
            print({"rank":str(rank),"name": name, "address": address, "latitude": latitude, "longitude": longitude})
            collection.update_one({'rank': str(rank)}, {'$set': {'address': address, 'phone': phone, 'website': website, 'latitude': latitude, 'longitude': longitude}})
            #key = {"name": name} #matching key
            #new_values = {"$set": {"address": address,"phone": phone,"website": website,"latitude": latitude,"longitude": longitude}}
            #collection.update_one(key, new_values)
X9()
