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
to look for similar playlists and using one of Spotify's _recommendation_ endpoints seemed like cheating. In the end
what I decided to do is to make a list of all unique artists within a playlist and then search for playlists that had 
that artists name in its description. This would then give me a new set of playlists which would result in a new set of
users and their songs, then artists then new playlists and so on. I built a small Graph data structure (found [here](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/playlist_artist_graph.py)) to keep track of 
this crawling search, which has been visualised below.

[**Network Graph here soon**]

New vertices of the graph were generated dynamically as the graph was being scanned. I opted for a breadth-first
search algorithm because I wanted to explore vertices (playlists) that were closest to the initial playlist first as 
they would be closer/more relevant.

The script for the search algorthim can be found [here](https://github.com/mxury/spotify_tensorflow_recommender/blob/main/load_data.py).

## Recommender system using Tensorflow
Tensorflow has a nice library `tensorflow-recommenders` that contains many useful layers and metrics. Firstly the data 
was mostly string so it was word embedded using the `StringLookUp` and `Embedding` layers from `tf.keras`, then to score 
the potential candidates the factorised top-K metric was used and then wrapped in a `tensorflow-recommenders` Model layer 
which itself is a Keras base model with the training and testing steps taken care of.

The ranking model then takes the candidates from the retrieval model and uses the popularity rating of the song to 
suggest the most likely candidates. The loss used here is the `MeanSquaredError` metric.


## Improvements
Include more features that could inform the ranking process, or the retrieval model. However it's very important that 
the retrieval model stays quick as it has to filter out 100 songs from a dataset of over 10,000! 
This project is still very much a work in progress! 
