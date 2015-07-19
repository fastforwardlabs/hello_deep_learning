import requests
import time
import os

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
locale = 'en-US'  # CHANGE LOCALE IF NEEDED

header = {'Authorization': 'CloudSight ' + api_key}
body = {'image_request[locale]': locale}

api_base_url = 'https://api.cloudsightapi.com'


def main():
    apple_pie_url = 'https://upload.wikimedia.org/wikipedia/commons/3/32/Apple_Pie.JPG'
    image_directory = os.path.dirname(os.path.realpath(__file__)) + '/images'

    # CloudSight's API works in two steps
    #
    #   1. Send CloudSight an image, either by sending an image url or by encoding an image in the request.
    #      CloudSight responds to this request with a token and a new url at which you can access your image.
    #
    #   2. Use the token from step 1. to retrieve the results of CloudSights analysis.
    #

    # Post a url for an image to CloudSight
    zebra_token = get_token_for_url_image(apple_pie_url)

    # Post an encoded image to CloudSight
    with open(image_directory + '/bonsai.jpg', 'rb') as bonsai:
        bonsai_token = get_token_for_encoded_image(bonsai)


    # CloudSight recommends allowing 4 seconds for the image to be analyzed on their servers
    time.sleep(4)


    # Use the tokens to get the results for each image

    zebra_results = get_results_for_token(zebra_token)
    print zebra_results

    bonsai_results = get_results_for_token(bonsai_token)
    print bonsai_results


def get_token_for_url_image(url):
    """
    :param url - a url of the image for CloudSight to analyze
    :return token - a token with which to retrieve the results from the image analysis from CloudSight
    """
    body.update({'image_request[remote_image_url]': url})
    response = requests.post(api_base_url + '/image_requests', headers=header, data=body)
    return response.json()['token']


def get_token_for_encoded_image(image):
    """
    :param image - a python file object of the image for CloudSight to analyze
    :return token - a token with which to retrieve the results from the image analysis from CloudSight
    """
    image_dict = {'image_request[image]': image}
    response = requests.post(api_base_url + '/image_requests', headers=header, data=body, files=image_dict)
    return response.json()['token']


def get_results_for_token(token):
    """
    :param token - the token for which to retrieve results from CloudSight
    :return results - results from CloudSight's analysis of the image corresponding to the provided token

    View http://cloudsight.readme.io/docs/image_responses for information about the format of CloudSight's responses.
    """
    while True:
        r = requests.get(api_base_url + '/image_responses/' + token, headers=header)

        response_content = r.json()
        if response_content['status'] != 'not completed':
            return response_content

        # If imaging processing is not complete, CloudSight recommends retrying the request after one second
        time.sleep(1)


if __name__ == '__main__':
    main()
