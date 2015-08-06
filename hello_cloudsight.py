import requests
import time
import os
from urls import apple_pie_url

'''
This is a 'hello world' script for the CloudSight image recognition API.

To get started:

    1.   Sign up at:

            http://cloudsightapi.com/api_client_users/new

    2.   Create a new CloudSight 'project' at:

             http://cloudsightapi.com/dashboard

    3.   Copy the 'API Key' into the script below

More information about CloudSight's API can be found here: http://cloudsight.readme.io/v1.0/docs
'''

api_key = ''  # ENTER YOUR API KEY HERE

api_base_url = 'https://api.cloudsightapi.com'

def main():
    image_directory = os.path.dirname(os.path.realpath(__file__)) + '/images'

    # CloudSight's API works in two steps
    #
    #   1. Send CloudSight an image, either by sending an image url or by encoding an image in the request.
    #      CloudSight responds to this request with a token and a new url at which you can access your image.
    #
    #   2. Use the token from step 1. to retrieve the results of CloudSights analysis.
    #

    # Post a url for an image to CloudSight
    pie_token = get_token_for_url_image(apple_pie_url, api_key)

    # Post an encoded image to CloudSight
    with open(image_directory + '/bonsai.jpg', 'rb') as bonsai:
        bonsai_token = get_token_for_encoded_image(bonsai, api_key)


    # CloudSight recommends allowing 4 seconds for the image to be analyzed on their servers
    time.sleep(4)


    # Use the tokens to get the results for each image
    pie_results = get_results_for_token(pie_token, api_key)
    print pie_results

    bonsai_results = get_results_for_token(bonsai_token, api_key)
    print bonsai_results


def get_token_for_url_image(url, api_key, locale='en-US'):
    """
    :param url - a url of the image for CloudSight to analyze
    :return token - a token with which to retrieve the results from the image analysis from CloudSight
    """
    body = _locale(locale)
    body.update({'image_request[remote_image_url]': url})
    response = requests.post(api_base_url + '/image_requests', headers=_auth_header(api_key), data=body)
    return response.json()['token']


def get_token_for_encoded_image(image, api_key, locale='en-US'):
    """
    :param image - a python file object of the image for CloudSight to analyze
    :return token - a token with which to retrieve the results from the image analysis from CloudSight
    """
    url = api_base_url + '/image_requests'
    files = {'image_request[image]': image}
    response = requests.post(url, headers=_auth_header(api_key), data=_locale(locale), files=files)
    return response.json()['token']


def get_results_for_token(token, api_key):
    """
    :param token - the token for which to retrieve results from CloudSight
    :return results - results from CloudSight's analysis of the image corresponding to the provided token

    View http://cloudsight.readme.io/docs/image_responses for information about the format of CloudSight's responses.
    """
    while True:
        r = requests.get(api_base_url + '/image_responses/' + token, headers=_auth_header(api_key))

        response_content = r.json()
        if response_content['status'] != 'not completed':
            return response_content

        # If imaging processing is not complete, CloudSight recommends retrying the request after one second
        time.sleep(1)


def _auth_header(api_key):
    return {'Authorization': 'CloudSight ' + api_key}


def _locale(locale):
    return {'image_request[locale]': locale}


if __name__ == '__main__':
    main()
