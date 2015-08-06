# Hello, Deep Learning

This repository contains sample scripts for the following deep learning APIs:

- [MetaMind](https://www.metamind.io/)
- [Dextro](https://www.dextro.co/)
- [CloudSight](http://cloudsightapi.com/)
- [Clarifai](http://www.clarifai.com/)

It also contains an ipython notebook demonstrating simple use cases for each API.

### Summary of Capabilities

**MetaMind** contains several useful built in classifiers, and also allows you to build your own classifiers for images and text.  When asked to predict a class for an image or a text, it will return the predicted class along with a probability representing its certainty that class is correct.

**Dextro** is focused on video analysis, and can tag videos and livestreams.  It will provide a list of salient tags, as well as lists of timestamps indicating when images associated with each tag were present.  Additionally, it can limit the tags it's looking for based on user input.

**CloudSight** is just a really good image tagging API.  All it does it gives a short description of an image, and also returns 'categories' if it finds any.  It doesn't deal with probabilities, but it's usually right. 

**Clarifai** tags images and videos.  For each image, it returns a list of tags, and for each tag, it also returns a probability that the tag applies.  It treats videos as a sequence of images, and grabs a screenshot from each second of the video to analyze.

Please see the ipython notebook and the 'hello' scripts for more details!
