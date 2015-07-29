import requests
import pprint
from urls import video_url

'''
This is a 'hello world' script for the Dextro video analysis API.

To get started:

    1.   Sign up at:

            https://www.dextro.co/#signup

    2.   Copy your api key into the script below.

    3.   Build an endpoint of your own to handle Dextro's callbacks, and enter that URL into the script below.

More information about Dextro's API can be found here: https://www.dextro.co/api
'''

api_key = ''  # ENTER YOUR API KEY HERE

# Dextro POSTs the results of its video analysis to a url provided with the original request.
# We've set up a little heroku webapp accepts the results and serves them back up.
# NOTE: This is a very lightweight webapp and is not intended for use in production or for sensitive materials.
callback_url = 'https://fflabs-dextro-callback.herokuapp.com/request'


def main():
    ## Categories

    # This endpoint returns all the categories that Dextro currently supports along with their IDs.
    # These categories can be used as inputs to guide video analysis in the Custom Video Categorization endpoint.
    r = requests.get('http://api.dextro.co/v1/categories', data={'api_key': api_key})
    pprint.pprint(r.json())


    ## General Video Categorization

    response = categorize_video(video_url)
    print 'General video categorization:'
    print_video_categorization_response(response)


    ## Custom Video Categorization

    # This is a selection of categories returned from the categories endpoint above.
    category_ids = [
        987,  # Winter Sport
        982,  # Nature
        878,  # its_getting_dark
        867,  # great_outdoor
        853,  # person_wearing_beanie
        839,  # foot_selfie
        584   # outdoor
    ]

    response = custom_categorize_video(video_url, category_ids)
    print 'Custom video categorization:'
    print_video_categorization_response(response)


def categorize_video(video_url):
    """
    :param video_url: The URL of the video to be sent to Dextro for analysis
    :return: A python dict representing Dextro's JSON response to the request.
    """
    request_data = {
        'api_key': api_key,
        'video_url': video_url,
        'callback_url': callback_url
    }

    video_categorization = 'http://api.dextro.co/v1/video/categorize_async'
    r = requests.post(video_categorization, data=request_data)
    return r.json()

def custom_categorize_video(video_url, category_ids):
    """
    :param video_url: The URL of the video to be sent to Dextro for analysis
    :param category_ids: A list of ints or strings representing Dextro categories.
    :return: A python dict representing Dextro's JSON response to the request.
    """
    request_data = {
        'api_key': api_key,
        'video_url': video_url,
        'callback_url': callback_url,
        'category_ids': ','.join(map(str, category_ids))
    }

    custom_video_categorization = 'http://api.dextro.co/v1/video/detect_async'
    r = requests.post(custom_video_categorization, data=request_data)
    return r.json()

def print_video_categorization_response(response):
    print 'Response from Dextro: ', response
    if 'request_id' in response and 'eta' in response:
        print 'Results will be available at ' + callback_url + '/' + response['request_id']
        print 'Dextro predicts that they will arive in ' + str(response['eta']) + ' seconds.\n'

if __name__ == "__main__":
    main()
