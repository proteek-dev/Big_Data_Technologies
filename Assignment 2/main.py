import re
import json

TWEETS = "10000 tweets 1.json"
CLEANED_TWEETS = "cleaned_10000_tweets.json"
DESIRED_TWEETS = "formatted_10000_tweets.json"

def replace_functions(match) :
    value = match.group(1) 
    return f'"{value}"'

def remove_replace_patterns(file_name):
    
    # Define the regex patterns for /* 1 */, /* 2 */, etc.
    pattern = r'/\* (\d+) \*/'
    pattern_to_remove = r'(\/\* 10000 Tweets \*\/)'

    # Read the content of the file
    with open(file_name, "r") as file:
        content = file.read()

    # Remove /* 10000 Tweets */
    content = re.sub(pattern_to_remove, "", content)
    # Replace /* 1 */ with "[", /* 2 */ with ",", and remove other /* */ comments
    content = re.sub(pattern, lambda m: "[" if m.group(1) == "1" else ",", content)

    # Close the JSON array at the end of the file
    content = content.strip() + "]"

    # Write the modified content back to the file
    with open(file_name, "w") as file:
        file.write(content)

    print("Comments replaced and file updated.")


def get_cleaned_tweets(tweets=TWEETS, clearned_tweets=CLEANED_TWEETS):
    
    # Define a regular expression pattern to match ObjectId() and NumberLong ()
    pattern_object_id = r'ObjectId\("([^"]+)"\)'
    pattern_number_long = r'NumberLong\((\d+)\)'

    # Read in the text file
    with open(tweets, 'r', encoding= 'utf-8') as file:
        text = file.read()

    # Replace ObjectId() and NumberLong() with string values
    text = re.sub(pattern_object_id, replace_functions, text)
    text = re.sub(pattern_number_long, replace_functions, text)

    # Write the modified text back to a new file
    with open(clearned_tweets, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    remove_replace_patterns(clearned_tweets)

    print(" 10000_tweets.json file processed and saved as '10000_cleaned_tweets.json'")


def get_desired_tweets(clearned_tweets=CLEANED_TWEETS, desired_tweets=DESIRED_TWEETS):

    try:
        with open(clearned_tweets, "r") as file:
            data = json.load(file)

        desired_data = []

        for tweet in data:
            desired_data.append({
                "id": tweet["id"],
                "postedTime": tweet["actor"]["postedTime"],
                "text": tweet["text"],
                "twitter_lang": tweet["twitter_lang"],
                "retweetCount": tweet["retweetCount"],
                "favoritesCount": tweet["favoritesCount"],
                "verb": tweet["verb"],
                "generator": {
                    "displayName": tweet["generator"]["displayName"],
                    "link": tweet["generator"]["link"]
                },
                "actor": {
                    "id": tweet["actor"]["id"],
                    "displayName": tweet["actor"]["displayName"],
                    "preferredUsername": tweet["actor"]["preferredUsername"],
                    "url": tweet["link"],
                    "description": tweet["actor"]["summary"]
                },
                "link": tweet["link"],
                "twitter_entities": {
                    "hashtags": tweet["twitter_entities"]["hashtags"],
                    "urls": tweet["twitter_entities"]["urls"],
                    "user_mentions": tweet["twitter_entities"]["user_mentions"]
                },
                "object": tweet["object"],
            })

        with open(desired_tweets, "w", encoding='utf-8') as file:
            json.dump(desired_data, file, indent=4)

        print(" 10000_cleaned_tweets.json file processed and saved as '10000_desired_tweets.json'")

    except FileNotFoundError:
        print("Cleaned File not found.")

if __name__ == "__main__":
    get_cleaned_tweets()
    get_desired_tweets()
    