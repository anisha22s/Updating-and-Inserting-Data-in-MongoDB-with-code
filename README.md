# **Updating and Inserting Data in MongoDB with Webscraping and API Integration**

This project demonstrates how to extract data using webscraping, store it in a MongoDB collection and update it using an external API. We will be parsing the top 30 "Pizzeria" shops in San Francisco on Yellow Pages and storing them in a MongoDB collection.

## **Dependencies**

BeautifulSoup  
Requests  
pymongo  
json  

## **Usage**

- Clone the repository and navigate to the project directory  
- Install the dependencies using pip install -r requirements.txt  
- Run the Python script main.py using python main.py

The code first extracts shop information from the search results of Yellow Pages using webscraping. Then the extracted data is stored into a MongoDB collection, with one document for each shop. Finally, we use the positionstack API to update our MongoDB collection with latitude and longitude information for each shop.

You can view the extracted data and updated MongoDB collection by accessing the main.py file.
