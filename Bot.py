import tweepy
import requests
from datetime import datetime, timedelta
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import json
import time
import random
import os

# Constants (Replace with your actual values or fetch from environment variables)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
API_KEY = os.environ.get("API_KEY")

# Append a string to a JSON file
def append_string_to_file(s, filename):
    # Check if the file exists. If not, initialize it with an empty array.
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)

    # Read the current content of the file.
    with open(filename, 'r') as file:
        content = json.load(file)

    # Append the new string to the content.
    content.append(s)

    # Write the updated content back to the file.
    with open(filename, 'w') as file:
        json.dump(content, file)

# Read date from a file
def read_date_from_file(filename):
    with open(filename, 'r') as file:
        date_str = file.readline().strip()
    return date_str

# Check if one day has passed since the given date
def has_one_day_passed(date_str):
    file_date = datetime.strptime(date_str, "%Y-%m-%d")
    current_date = datetime.now()
    return current_date - file_date > timedelta(days=1)

# Main logic to process tweets based on the date
def process_logic_based_on_date(filename):
    date_str = read_date_from_file(filename)
    
    if has_one_day_passed(date_str):
        daily_tweets = []
        print("At least one day has passed since the last recorded date!")
        print("Time to post my daily Twitter routine.")
        
        # Replace YOUR_API_KEY with your actual API key
        fetch_and_save_news("YOUR_API_KEY", "us", "news.json")
        
        with open("consecutive_days.txt", 'r') as file:
            number = int(file.readline().strip())
        
        print(f"Current consecutive days: {number}")

        # Constructing messages for tweets
        # ... [rest of your message construction code]

        # Posting tweets with images and handling exceptions
        # ... [rest of your tweet posting code]

        # Update the file with the current date
        with open(filename, 'w') as file:
            file.write(datetime.now().strftime("%Y-%m-%d"))
        
        number += 1

        # Save the incremented number back into the file
        with open("consecutive_days.txt", 'w') as file:
            file.write(str(number))
    else:
        print("Not enough time has passed since the last recorded date.")

# Create a Twitter poll
def create_poll(question, options, duration_minutes=1440):
    # Replace with your Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    # Set up OAuth1 authentication
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # API endpoint
    url = "https://api.twitter.com/2/tweets"

    # Poll data
    data = {"text": question, "poll": {"options": options, "duration_minutes": duration_minutes}}

    # Make the request
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data, auth=auth)

    # Handle the response
    if response.status_code == 201:
        tweet_id = (response.json())["data"]["id"]
        # Replace with your file paths
        append_string_to_file(tweet_id, "YOUR_FILE_PATH_1")
        append_string_to_file(tweet_id, "YOUR_FILE_PATH_2")
        append_string_to_file(tweet_id, "YOUR_FILE_PATH_3")
        print("Poll created successfully!")
    else:
        print(f"Failed to create the poll. Error: {response.text}")

# Upload media to Twitter

def upload_media(filename, auth):
    # Upload the media
    url = "https://upload.twitter.com/1.1/media/upload.json"
    with open(filename, "rb") as f:
        files = {"media": f}
        response = requests.post(url, auth=auth, files=files)

    # Handle the response and extract the media_id
    if response.status_code == 200:
        media = response.json()
        print(media)
        return media["media_id_string"]
    else:
        print("Error occurred while uploading media.")
        print(response.text)
        return None



# Post a tweet with an image
def post_tweet_with_image(tweet, image_filename):
    # Replace with your Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    auth2 = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth2.set_access_token(
        access_token,
        access_token_secret,
    )
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    # Upload the image and get the media_id
    media_id = upload_media(image_filename,auth)
    if not media_id:
        print("Failed to upload image.")
        return

    # OAuth1 authentication
    

    # Twitter API endpoint for posting a tweet with media
    url = "https://api.twitter.com/1.1/statuses/update.json"
 
   
    # Data payload
    payload = {"text": tweet,  "media": {
        "media_ids": [media_id]
    }}
    try:
        response = client.create_tweet(media_ids=[media_id], text=tweet)
        #print(response)
    except Exception as e:
        # This will catch all exceptions and print the error message.
        print(f"An error occurred: {e}")


# Post a tweet
def post_tweet(tweet):
    # Replace with your Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
     # OAuth1 authentication
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Twitter API v2 endpoint for posting a tweet
    url = "https://api.twitter.com/2/tweets"

    # Split the string into two parts
    if "Source:" in tweet:
        parts = tweet.split("Source:")
        first_part = parts[0].strip()
        second_part = "Source:" + parts[1].strip()

    # Data payload
        payload = {"text": first_part}

    # Post the tweet
        response = requests.post(url, auth=auth, json=payload)

        response_json = response.json()
        try: 
            tweet_id = response_json['data']['id']
            print(tweet_id)
            time.sleep(10)
            reply_to_tweet(tweet_id, second_part)
        except Exception as e:
            print("Np")



    # Check if it was successful
        if response.status_code == 201:
            print("Tweet posted successfully!")
        else:
            print("Error occurred while posting tweet.")
            print(response.text)
    else:

        payload = {"text": tweet}

    # Post the tweet
        response = requests.post(url, auth=auth, json=payload)


    # Check if it was successful
        if response.status_code == 201:
            print("Tweet posted successfully!")
        else:
            print("Error occurred while posting tweet.")
            print(response.text)

# Reply to a tweet
def reply_to_tweet(tweet_id, reply_text):
    # Replace with your Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Form the payload
    url = "https://api.twitter.com/2/tweets"

    payload = {
        "text": reply_text,
        "reply": {
            "in_reply_to_tweet_id": tweet_id
        }
    }

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code == 201:
        print("Successfully replied to the tweet.")
        return response.json()
    else:
        print(f"Failed to reply: {response.content}")
        return None

# Fetch and save news articles
def fetch_and_save_news(api_key, country, filename):
    # Set up the API call parameters
    theme = ""
    fixed_news = []
    two_days_ago = datetime.now() - timedelta(days=1)
    formatted_date = two_days_ago.strftime('%Y-%m-%d')
    for i in range(0,2): #domains=finance.yahoo.com,coindesk.com,cointelegraph.com,newsbtc.com,bitcoinist.com
        url = f'https://newsapi.org/v2/everything?q={theme}&from={formatted_date}&apiKey={api_key}'
        # Make the API call
        response = requests.get(url)
        time.sleep(15)
        # Check the status of the request
        if response.status_code != 200:
            print(f'Error: API request unsuccessful. Status code: {response.status_code}.')
            return False
        else:
            

            # Convert the response to JSON
            data = response.json()
            #print(data)
            theme = ""
            
    random.shuffle(fixed_news)

        
    # Save the data to a file
    with open(filename, 'w') as f:
        json.dump(fixed_news, f, indent=4)

    print(f"The data has been successfully saved to '{filename}'")
    return True

# Main execution loop
dummy_counter = 2
while True:
    if dummy_counter % 3 == 0:
        file_path = 'output.json'
    else:
        file_path = 'news.json'
    
    process_logic_based_on_date("date.txt")
    
    with open(file_path, 'r') as file:
        # Parse the JSON file to a Python object
        data = json.load(file)
    
    print("Tweets left before terminating: ", len(data))
    
    if len(data) == 0 and file_path == 'output.json':
        exit("Out of tweets!")
    if len(data) == 0 and file_path == 'news.json':
        # Replace with your NewsAPI key
        api_key = "YOUR_NEWSAPI_KEY"
        fetch_and_save_news(api_key, "us", "news.json")
        continue
    
    tweet = data.pop()
    
 
      post_tweet(tweet)
        
      print("I am about to post a tweet.. ", tweet)
      with open(file_path, "w") as json_file:
          json.dump(data, json_file, indent=4)
        
      print("Tweet posted. Going to sleep for 1 hour..")
      dummy_counter += 1
      time.sleep(3600)

