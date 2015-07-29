import os
import pprint
from metamind.api import set_api_key, general_image_classifier, twitter_text_classifier, food_image_classifier, ClassificationModel, ClassificationData
from urls import apple_pie_url, zebra_url, salad_url, deer_url, blueberry_pie_url

'''
This is a 'hello world' script for the metamind text and image classifier API.

To get started:

    1.   Sign up at:

            https://www.metamind.io/auth/signup

    2.   Retrieve your api key here

             https://www.metamind.io/auth/my_account

    3.   Copy the 'API Key' into the script below

More information about MetaMind's API can be found here: http://docs.metamind.io/docs
'''

api_key = ''  # ENTER YOUR API KEY HERE
set_api_key(api_key)

def main():

    # MetaMind makes it simple to create custom classifiers for both text and images

    # Create and use a custom image classifier
    # This classifier classifies an image as 'food' or 'animal'
    image_classifier = create_image_classifier()
    print 'Custom image classifier predictions:'
    pprint.pprint(image_classifier.predict([
        blueberry_pie_url,
        deer_url
    ], input_type='urls'))

    # Create and use a custom text classifier
    # This classifier classifies text as 'rural' or 'urban'
    text_classifier = create_text_classifier()
    print 'Custom text classifier predictions:'
    pprint.pprint(text_classifier.predict([
        'We sheared the sheep yesterday.',
        'The traffic is loud.'
    ], input_type='text'))

    # Use builtin general image classifier
    print 'MetaMind builtin general image classifier predictions:'
    pprint.pprint(general_image_classifier.predict([apple_pie_url, zebra_url], input_type='urls'))

    # Use builtin food image classifier
    print 'MetaMind builtin food image classifier predictions:'
    pprint.pprint(food_image_classifier.predict([apple_pie_url, salad_url], input_type='urls'))

    # Use builtin twitter sentiment classifier
    # This classifier finds tweets by a given key word, and classifies each tweet as
    # 'positive', 'negative' or 'neutral'
    print 'MetaMind builtin twitter sentiment classifier:'
    pprint.pprint(twitter_text_classifier.query_and_predict('trump')[:3])

    # You can create a representation of a given classifier by passing its id into the constructor.
    # You can explore additional public classifiers here: https://www.metamind.io/vision/explore
    # You can explore your private classifiers and data here: https://www.metamind.io/my_stuff

    # You can find more details about the classifier used below here: https://www.metamind.io/classifiers/155
    print 'Public sentiment classifier with id=155:'
    pprint.pprint(ClassificationModel(id=155).predict("This is such a great, wonderful sentiment", input_type="text"))


def create_image_classifier():
    # Create a dataset on the MetaMind servers.
    # You can view your existing datasets here: https://www.metamind.io/my_stuff#my-datasets
    # Each dataset is assigned an id by the server.
    #
    # To create a local representation of any of your datasets, you can simply pass the id into the constructor:
    #
    #      ClassificationData(id=123)
    #
    training_data = ClassificationData(private=True, data_type='image', name='image_demo')

    # You can find more information about how to add data to a dataset here: http://docs.metamind.io/docs/datasets
    # There are multiple ways of adding data to both text and image datasets
    training_data.add_samples([
        (apple_pie_url, 'food'),
        (salad_url, 'food'),
        (deer_url, 'animal')
    ], input_type='urls')

    image_directory = os.path.dirname(os.path.realpath(__file__)) + '/images'
    training_data.add_samples([
        (image_directory + '/bonsai.jpg', 'animal'),
        (image_directory + '/dog.jpg', 'animal')
    ], input_type='files')

    # Each classifier is assigned an id by the server, much like a dataset.
    # As with a dataset, you can create a representation of a classifier by passing its id into the constructor:
    #
    #      ClassificationModel(id=123)
    #
    classifier = ClassificationModel(private=True, name='image_demo')
    classifier.fit(training_data)
    return classifier


def create_text_classifier():
    training_data = ClassificationData(private=True, data_type='text', name='text_demo')
    training_data.add_samples([
        ('The horse got out of the barn.', 'rural'),
        ('It is very quiet at night', 'rural'),
        ('There are 300 cattle in the field.', 'rural'),
        ('The roads are empty', 'rural'),
        ('There is so much traffic today.', 'urban'),
        ('Newer buildings are often made of glass.', 'urban'),
        ('The subways are quite loud.', 'urban'),
        ('How many skyscrapers do you see?', 'urban')
    ], input_type='text')

    classifier = ClassificationModel(private=True, name='text_demo')
    classifier.fit(training_data)
    return classifier


if __name__ == '__main__':
    main()
