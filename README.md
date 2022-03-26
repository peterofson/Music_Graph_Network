# Music Recommendation Engine via Graph Network
## Abstract

- Music recommendation engines are giant, lumbering programs designed to suggest
similar artists based off other artists. A straightforward approach will be taken to replace the
cumbersome calculations of a recommendation engine with that of a graph network. This
network will start with a base artist, in this case Metallica, with the nodes being those bands
which influenced Metallica and the subsequent nodes consisting of artists who influenced that
band, etc. Using simple network analysis, we will then return a list of similar artists.
## Introduction

*Recommendations are complex process involving many moving parts and even more
data. Netflix, Spotify, and other steaming services all use recommendation engines on their
platforms. Netflix and other video streaming services can change the image of the content to
better align with the classification of the content. Music services on the other hand cannot change
the album cover. Because a user chooses with their eyes when they want to watch a movie or
show these streaming services can leverage the image far more than the music streaming
services. For this reason, the music streaming services must rely on other methods beyond what
the album looks like to recommend artist, songs, etc.
 ⇥Algorithms have been tested time and time again to try and improve the music
recommendation process. From counting the number of unique words in a song, analyzing the
album covers and comparing attributes like beats per minutes (BPM), energy and loudness. All
these algorithms have one thing in common, they require tons of calculations. With a graph
network we can immediately see the connections between two artists without calculating
anything. If a medium sized graph network can return similar results to a large recommendation
engine such as Spotify, then it begs the question as to why they aren’t using graph networks.


