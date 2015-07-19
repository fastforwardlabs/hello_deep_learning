from clarifai.client import ClarifaiApi
import os
import pprint

'''
This is a 'hello world' script for the Clarifai tagging API for images and videos.

To get started:

    1.   Sign up at:

             https://developer.clarifai.com/accounts/signup/


    2.   Check your email to verify your account


    3.   Sign in with your email and password at:

            https://developer.clarifai.com/accounts/login/


    4.   Sign up for a free subscription at:

            https://developer.clarifai.com/payments/subscriptions


    5.   Create a new Clarifai 'application' at:

            https://developer.clarifai.com/applications/


    6.   Copy the 'Client ID' and 'Client Secret' from that application into the script below

More information about Clarifai's API can be found here: https://developer.clarifai.com/docs/
'''

client_id = ''  # ENTER YOUR CLIENT ID HERE
client_secret = ''  # ENTER YOU CLIENT SECRET HERE
clarifai_api = ClarifaiApi(client_id, client_secret)


def main():

    zebra_url = 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Zebra_standing_alone_crop.jpg'
    apple_pie_url = 'https://upload.wikimedia.org/wikipedia/commons/3/32/Apple_Pie.JPG'
    video_url = 'https://s3.amazonaws.com/clarifai-tmp/demo-videos/GoPro+Dolomites+2013-SD.mp4'


    # Clarifai's tag endpoint returns tags for the image/video along with the probabilities that those tags are correct
    # For videos, Clarifai provides a list of tags and their respective probabilities for each second of the video

    # Tag images by url:
    #
    #   - Pass a list of urls of images to the tag_image_urls function on clarifai's python client
    #
    url_image_results = clarifai_api.tag_image_urls([zebra_url, apple_pie_url])
    print 'Results for zebra and apple pie images:'
    pprint.pprint(summarize_tag_results(url_image_results))

    # Tag video by url
    url_video_results = clarifai_api.tag_image_urls(video_url)
    print 'Results for video:'
    pprint.pprint(summarize_tag_results(url_video_results))


    # Tag images by encoding:
    #
    # - Pass a list of python file objects to the tag_images function on clarifai's python client
    #
    image_directory = os.path.dirname(os.path.realpath(__file__)) + '/images'
    with open(image_directory + '/bonsai.jpg') as bonsai, open(image_directory + '/dog.jpg') as dog:
        encoded_image_results = clarifai_api.tag_images([bonsai, dog])
    print 'Results for bonsai and puppy images:'
    pprint.pprint(summarize_tag_results(encoded_image_results))


    # The Feedback endpoint allows you to add tags for images/videos and give other feedback
    # This helps improve future results

    # Feedback on image via url
    feedback_response = clarifai_api.feedback(urls=apple_pie_url, add_tags=['apple', 'pie'])
    print 'Results from feedback:'
    pprint.pprint(feedback_response)


def summarize_tag_results(tag_results):
    """
    :param tag_results - dict from clarifai python client's tag methods
    :returns result_summary - a summary of the tags, excluding results metadata

        for images: [
                        [(class, probability),...], # image 1
                        [(class, probability),...], # image 2
                        [('error', error_msg)],     # error case
                        ...
                    ]

        for videos: [
                        [  # video 1
                            (timestamp1, [(class, probability),...]), # tags for timestamp1
                            (timestamp2, [(class, probability),...]), # tags for timestamp2
                            ...
                        ],
                        ...
                    ]
    """
    results_summary = []
    for result in tag_results['results']:
        if 'error' in result['result']:
            results_summary.append([('error', result['result']['error'])])

        else:
            results_summary.append(_summarize_tags(result))

    return results_summary


def _summarize_tags(result):
    tags = result['result']['tag']

    if 'timestamps' in tags:
        grouped_tags = map(lambda x: zip(x[0], x[1]), zip(tags['classes'], tags['probs']))
        return zip(tags['timestamps'], grouped_tags)

    return zip(tags['classes'], tags['probs'])


if __name__ == "__main__":
    main()
