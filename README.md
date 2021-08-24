# Video Clustering Algorithm 


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=mastering)](https://travis-ci.org/joemccann/dillinger)

The algorithm is part of a series of repositories for a Machine Learning-based video recomendation system for a web applications users. The three fundamental purposes of this algorithm are:
1. To create a set of video clusters based on the AWS Rekognition tags for the videos using a unsupervised machine learning algorithm.
2. To create a cluster classifier for new (out of training) videos using a esemble learning model.
3. To create a bit-wise dataframe to perform quick and efficient vertorized operations.

## Features

- Import a csv file with the videos tags
- Export the model and results to a S3 bucket
- Write the video clusters in a Postgress SQL database



## Installation

for thesting purposes we porpose using python 3.8.* with a 64-bits machine. 

Clone the repository and Install the dependencies 

```sh
git clone/git pull
pip3 install -r requirements.txt
```

## Development

Want to contribute? Great!


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
