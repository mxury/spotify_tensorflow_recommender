# Building a Spotify track recommender using Tensorflow

---

### Motivation
Music inhibits most of my waking hours, without it my life would certainly be less colourful. Hence I decided to create
my own recommender machine learning model using data from the [Spotify Web API](https://developer.spotify.com/). 
This was my first foray into this sub-discipline of machine learning (my only other interaction occured
in the Andrew Ng ML course on Coursera). I used tensorflow mainly to enhance my understanding of its
inner workings and partly because I enjoy playing around with neural networks. I used the 
Matrix Factorisation model containing retrieval and ranking parts. The former of which selects an initial set of 
candidates from the whole pool. The latter model will then rank the output of the retrieval model from 
which we can create a playlist of new recommendations. 

## Generating data 
The model compares selections/playlists of users and then tries to utilise that information to recommend new songs, 
i.e. user A listens to song 1 and song 2, while user B listens to song 2 and song 3, then the model might recommend 
song 3 to user A and song 1 to user B. Therefore I aimed to collate a dataset where the main features would be `user` 
and `song`. 

However few issues were encountered. While I could obviously read my own playlist and recover the songs within it, there 
was no trivial way to find users who also listened to those tracks, and better yet find a range of songs that one 
particular user listened to. My idea was then to associate a public playlist as a list of tracks that user listens to, 
so then the job was to find new playlists that ideally shared some connection with other playlists in the dataset. This
proved more difficult than one might expect as even though Spotify API contains a _search_ endpoint it's not clear how 
to look for similar playlists and using one of Spotify's _recommendation_ endpoints seemed like cheating. 
In the end the data gathering strategy was as follows: 
1. From a playlist (initial playlist is my own) list all the songs
2. Find the artist of each song 
3. Using Spotify's Web API search for playlists which feature the artists' name in the description 
4. Start again over at 1.

To facilitate this I built a small Graph data structure (found [here](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/playlist_artist_graph.py)) to keep track of 
this crawling search, which has been visualised below.

![Visualisation of graph](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/figs/graph_vis.png)

New vertices of the graph were generated dynamically as the graph was being scanned. I opted for a breadth-first
search algorithm because I wanted to explore vertices (playlists) that were closest to the initial playlist first as 
they would be closer/more relevant.

The script for the search algorthim can be found [here](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/load_data.py).

## Recommender system using Tensorflow
Using the `tensorflow-recommenders` library we utilise a matrix factorisation technique within a two tower model of 
both the Retrieval and Ranking models. For negative candidates we use in-batch negative sampling.  

The Retrieval model consists of a query(user) and a candidate(song) tower. 
The former uses an `Embedding` layer to convert the user string into a vector with an embedding dimension of 32, with 
a stack of dense layers on top. 
The latter while utilises audio features from the Spotify Web API to create a richer representation of each song. 
The loss used is the `CategoricalCrossEntropy` and the metric with which the model is evaluated is TopK Accuracy, 
which denotes whether a users song that was previously listened to is within the top K song 
computed by the model for that specific user.  


The ranking model is also a two tower model which takes the candidates from the retrieval model
and uses the popularity rating of the song to suggest the most likely candidates. The loss used 
here is the `MeanSquaredError` metric.

The most advanced implementation of the retrieval task can be found in 
[retrieval_w_audio_features.ipynb](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/retrieval_w_audio_features.ipynb).

## Improvements
Include more features that could inform the ranking process. However, it's very important that 
the retrieval model stays quick as it has to filter out 100 songs from a dataset of over 10,000! 
This project is still very much a work in progress! 
