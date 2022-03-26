# Music Recommendation Engine via Graph Network
## Abstract
Music recommendation engines are giant, lumbering programs designed to suggest
similar artists based off other artists. A straightforward approach will be taken to replace the
cumbersome calculations of a recommendation engine with that of a graph network. This
network will start with a base artist, in this case Metallica, with the nodes being those bands
which influenced Metallica and the subsequent nodes consisting of artists who influenced that
band, etc. Using simple network analysis, we will then return a list of similar artists.
##Introduction
Recommendations are complex process involving many moving parts and even more
data. Netflix, Spotify, and other steaming services all use recommendation engines on their
platforms. Netflix and other video streaming services can change the image of the content to
better align with the classification of the content. Music services on the other hand cannot change
the album cover. Because a user chooses with their eyes when they want to watch a movie or
show these streaming services can leverage the image far more than the music streaming
services. For this reason, the music streaming services must rely on other methods beyond what
the album looks like to recommend artist, songs, etc.
Algorithms have been tested time and time again to try and improve the music
recommendation process. From counting the number of unique words in a song, analyzing the
album covers and comparing attributes like beats per minutes (BPM), energy and loudness. All
these algorithms have one thing in common, they require tons of calculations. With a graph
network we can immediately see the connections between two artists without calculating
2
anything. If a medium sized graph network can return similar results to a large recommendation
engine such as Spotify, then it begs the question as to why they aren’t using graph networks.
##Literature Review
Many studies and articles have been written when it comes to the classification of music
genres, be it a binary, multi-class, or multi-label problem. The methods vary from study to study.
Some are using recurrent neural networks (RNN’s) to analyze small audio samples from songs
while others are leveraging the images of album covers with convolutional neural networks
(CNN’s). Others still are pulling together all the lyrics of the artists and using a type of RNN
called a Long Short-Term Memory network (LSTM) to try and classify music genres.
Oramas (2017) and his colleagues tied together audio, text, and image data to classify
genres. They used a CNN to classify album covers, a LSTM for the text data and then a RNN for
the audio data. They achieved incredibly accurate results but not for the data type they were
expecting. The model which used text data achieved the highest accuracy of 90%. The model for
image data achieved an accuracy of 75% while the model that used audio data had an accuracy
of 80%. The text model had twenty-five million parameters compared to six million for audio
and two million for the image model. Clearly there was more information in the text than in the
audio or images.
In the world of deep learning usually more data is always better; it prevents the
possibility of overfitting, increases the model’s robustness, and decreases its bias to a healthy
margin (Goodfellow, Bengio, and Courville, 2017). Dammann and Haugh (2017) constructed a
bag of words for each genre which consisted of unique words and the number of times they were
used. This simple yet elegant approach for classifying gernes allows the vast amount of data to
3
be usable. They also compared lyric, image, and audio data. Like Oramas and his colleagues, the
text model achieved the highest accuracy. To build a recommendation engine it seems that a lot
of ground can be covered by using the lyrics of songs for classification.
##Methods
For each artist on allmusic.com there is a subpage where one can see similar artists, who
influenced them, and what other artists follow them. Using the Selenium Python package to get
the data of the artist’s name, who they were influenced by and that artists genres. The artists
genres are a comma separated string ranging from three to ten genres. A Pandas dataframe was
then constructed to be passed into a beautiful NetworkX function which transforms a Pandas
dataframe into a graph network. The maximum number of “influenced by” records an artist can
have is ten. This means that each node going out from the starting node, which has no limits, will
have a maximum of ten nodes that connect to it. The final network, Figure 4, has 682 nodes with
1957 edges with an average degree of 5.74.
Ideally the number of connecting nodes, i.e., “influenced by”, would not have a limit but
this experiment is more of a proof of concept than anything else. Then a simple algorithm
accepts three parameters: an artist name, a Pandas dataframe and a NetworkX graph. This
algorithm returns a graph of similar artists along with a dataframe; it leverages cliques to find
clustered artists. Once these artists are found the genres are parsed to see if there are any matches
with the inputted artists genres. If there are no matches they are removed from the list, and the
list of related artists are finally returned. Three graphs were constructed starting from the base
node of Metallica. The first consisted of 284 entries, then 905 and finally 1,968 entries. These
varying sizes show how many iterations the data went through the data collection process.
4
##Results
Looking at the generated network of Figure 1 it is clear to see that some artists that
influenced Metallica have the same influences. For example, Metallica was influenced by Black
Sabbath, Iron Maiden, Deep Purple, and Led Zeppelin. Iron Maiden was also influenced by
Black Sabbath, Deep Purple, and Led Zeppelin. Already there is a hint of recommendation in this
simple example. Once we go beyond the base thirty influenced nodes of Metallica and get each
of those artists who influenced them, which is what Figure 2 represents, we go two iterations
more to get those artists who influenced them and so on, which is Figure 3. Drawing from the
largest network we can see the many outliers which are essentially the base influence for
Metallica. Comparing Figure 3 to Figure 4, which is the network of cliques one can see on the
outskirts a few cliques which predominantly consist of blues and soul artists. Using the network
clique data tied together with the list of genres allows a simple algorithm to return a list of
recommended artists.
When Metallica was chosen as the base artist to get a list of recommendations for the
algorithm returned a list of thirty artists. 65% of these artists were found in a Spotify playlist of
Metallica, labeled “Metallica Radio.” Not bad for using different genre labels. When just looking
at the genres of the network, seeing if the genres for Metallica were found in the associated
genres, it returned a list of 117 artists. Figure 5 shows the bar plot of Metallica’s three genres and
the number of artists who had that genre in their list of genres. Getting rid of duplicates, it
returned a list of 37 artists. In this list, 71% of artists were also in the Spotify playlist. There were
a lot of older Hard Rock artists that were returned in both lists which were not present in the
Spotify playlist. Attaching a popularity attribute to each node would most likely increase the
amount found in the Spotify playlist.
5
##Conclusion
One could use this network to work backwards and sideways to come up with suggested
songs based off a starting artist, in this case, Metallica. Having a network of artists who are not
similar but who influenced that artist is more important for authentic recommendations. For
when this approach is used the recommendations return possibly new artists as well as familiar
artists. Graph networks allow researchers to leverage data in simple yet elegant way to come up
with recommendations that are simply connections in the network.
Compared to giant neural networks graph network approaches might be more practical
during execution. After all, all genres of music are connected to each other in same way, shape or
form. A person familiar with music can hear the inspiration from other bands, the tone of the
guitars, the BPM’s, and the complexity of the overall song. What’s not easy to infer is who their
inspiration exactly was. Further exploration of this algorithm would be beneficial as the potential
to match or even exceed music streaming services recommendations is close. Attaching
attributes such as popularity to artists along with pulling in a similar subgenre to the network
show great promise. The next step would be to append the code to recommend songs instead of
artists
