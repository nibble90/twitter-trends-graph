from os import getenv
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
api_bearer_token = getenv('api_bearer_token')

class CustomTwitterEndpoint:
    def __init__(self):
        pass

    def tweet_count(self, query):
        """
        Inputs:
         - query: query to refine tweet counts by [string]

        Summary of functionality:
         - Passes the query and API token to v2 of the Twitter API in order to get a dictionary returned on tweet counts on an hour by hour basis
        """
        url = "https://api.twitter.com/2/tweets/counts/recent?query={}".format(query)
        headers = {"Authorization": "Bearer {}".format(api_bearer_token)}
        r = requests.get(url=url, headers=headers).json()
        return r

class GenerateGraph:
    def __init__(self, x, y, title):
        """
        Inputs:
         - x: x axis title [string]
         - y: y axis title [string]
         - title: title of the graph [string]

        Summary of functionality:
         - Stores/initialises various variables
        """
        self.x_axis_label = x
        self.y_axis_label = y
        self.title = title
        self.x_data = []
        self.y_data = []
        self.alternate_y_data = []

    def append_data(self, x, y, alternate_y):
        """
        Inputs:
         - x: value for x axis [integer]
         - y: value for y axis on the first plot [integer]
         - alternate_y: value for the y axis on the second plot [integer]
        
        Summary of functionality:
         - Appends the parameters passed into their respective lists, ensuring that if an argument was missing no data would be added as this would mess up the graph
        """
        self.x_data.append(x)
        self.y_data.append(y)
        self.alternate_y_data.append(alternate_y)

    def generate(self):
        """
        Summary of functionality:
         - Plots the data from the aforementioned lists, plots the titles and sets the graph as visible
        """
        plt.plot(self.x_data, self.y_data, label="per hour")
        plt.plot(self.x_data, self.alternate_y_data, label="total")
        plt.xlabel(self.x_axis_label)
        plt.ylabel(self.y_axis_label)
        plt.title(self.title)
        plt.legend()
        plt.show()
    
    def parse_trends(self, data):
        """
        Inputs:
         - data: dictionary of the data returned from twitter [json]

        Summary of functionality:
         - Iterates through the data, passing data to a function to append the data to the lists defined in __init__
        """
        i = 1
        total = 0
        for datapoint in data["data"]:
            total += datapoint["tweet_count"]
            self.append_data(str(i), datapoint["tweet_count"], total)
            i += 1

class TwitterTrends:
    def __init__(self):
        pass

    def searchTweets(self, query: str):
        """
        Inputs: 
         - query: query to search twitter [preferred as string]

        Summary of functionality:
         - Queries Twitter then generates the graph
        """
        data = CustomTwitterEndpoint().tweet_count(query)
        graph = GenerateGraph("count of hours since 7 days ago", "number of tweets", "tweets per hour")
        graph.parse_trends(data)
        graph.generate()

if __name__ == "__main__":
    TwitterTrends().searchTweets(input("Topic To Return Trend Data On \n> "))
