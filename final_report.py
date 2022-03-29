#!/usr/bin/env python
# coding: utf-8

# In[364]:


import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import to_agraph 
from networkx.algorithms import bipartite
from networkx.algorithms import community
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import pygraphviz
from pylab import hist
from selenium import webdriver
from selenium.webdriver.common.by import By
import warnings
import hvplot.networkx as hvnx
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.simplefilter('ignore')


# In[135]:


link = 'https://www.allmusic.com/artist/metallica-mn0000446509/related'


# In[218]:


driver = webdriver.Chrome('C:/Users/peter/Downloads/chromedriver_win32/chromedriver')  
driver.get(link)
time.sleep(3)
base_styles = driver.find_element_by_css_selector('div.styles')
list_styles = base_styles.find_elements_by_tag_name('a')


# In[15]:


def Create_dataframe_givenURL(link):
    driver.get(link)
    time.sleep(3)
    related_base = driver.find_element_by_css_selector('section.related.influencers')
    name = driver.find_element_by_css_selector('h1.artist-name')
    lists = related_base.find_elements_by_tag_name('li')
    # GENRES
    base_styles = driver.find_element_by_css_selector('div.styles')
    list_styles = base_styles.find_elements_by_tag_name('a')
    genres = []
    for x in list_styles:
        genres.append(x.text)
    genre_list = ",".join(genres)
    liso = []
    for li in lists:
        base_element = li.find_element_by_tag_name('a')
        name_influenced = base_element.text
        linker = base_element.get_attribute('href')
        vals = np.array([name.text,name_influenced, linker, genre_list]).reshape(1,-1)
        liso.append(pd.DataFrame(vals, columns=['artist', 'influenced_by', 'link','genres']))
    df = pd.concat(liso)
    df.reset_index(inplace=True,drop=True)
    return df


# In[217]:


def Create_nodes_givenURL(link):
    base_list = []
    driver.get(link)
    time.sleep(3)
    try:
        related_base = driver.find_element_by_css_selector('section.related.influencers')
    except:
        vals = np.array(['z','z', 'z','z']).reshape(1,-1)
        return pd.DataFrame(vals, columns=['artist', 'influenced_by', 'link','genres'])
    name = driver.find_element_by_css_selector('h1.artist-name')
    lists = related_base.find_elements_by_tag_name('li')
    liso = []
    # GENRES 
    base_styles = driver.find_element_by_css_selector('div.styles')
    list_styles = base_styles.find_elements_by_tag_name('a')
    genres = []
    for x in list_styles:
        genres.append(x.text)
    genre_list = ",".join(genres)
    if (len(lists) < 10):
        for li in lists:
            base_element = li.find_element_by_tag_name('a')
            name_influenced = base_element.text
            linker = base_element.get_attribute('href')
            vals = np.array([name.text,name_influenced, linker,genre_list]).reshape(1,-1)
            liso.append(pd.DataFrame(vals, columns=['artist', 'influenced_by', 'link','genres']))
        df = pd.concat(liso)
        df.reset_index(inplace=True,drop=True)
        return df
    else:
        for li in lists[0:10]:
            base_element = li.find_element_by_tag_name('a')
            name_influenced = base_element.text
            linker = base_element.get_attribute('href')
            vals = np.array([name.text,name_influenced, linker,genre_list]).reshape(1,-1)
            liso.append(pd.DataFrame(vals, columns=['artist', 'influenced_by', 'link', 'genres']))
        df = pd.concat(liso)
        df.reset_index(inplace=True,drop=True)
        return df


# In[357]:


def GetListOfRecommendations(artist,df, G):
    c=nx.cliques_containing_node(G, nodes=artist)
    recommend = []
    artists = []
    for x in c:
        for item in x:
            if item == artist:
                continue
            else:
                if (item not in artists):
                    try:
                        genre = df[df['artist'] == item].genres.values[0]
                    except:
                        continue
                    recommend.append([item,genre])
                    artists.append(item)
    df1 = pd.DataFrame(recommend, columns=['artist','genre'])
    df1['base'] = artist
    G1 = nx.Graph()
    G1 = nx.from_pandas_edgelist(df1,source='base',target='artist')
    pos=nx.spring_layout(G1,k=0.15, iterations=20)
    return hvnx.draw_networkx(G1,pos,**options), df1


# In[ ]:


# base = pd.read_csv('./BIG_Data.csv')
# g = pd.read_csv('./Data_Final.csv')
# small_df = pd.read_csv('./Metallica_Base284.csv')


# In[17]:


df1 = Create_dataframe_givenURL(link)


# In[ ]:


node_list = []
for x,y in df1.iterrows():
    node = Create_nodes_givenURL(y['link']+'/related')
    node_list.append(node)


# In[ ]:


df = pd.concat(node_list)
df.reset_index(inplace=True,drop=True)


# In[507]:


needs = []
for x in np.unique(df['influenced_by'].values):
    if x not in np.unique(df['artist'].values):
        url = df[df['influenced_by'] == x].values[0][2] + '/related'
        print(x)
        node = Create_nodes_givenURL(url)
        needs.append(node)
            


# In[224]:


hh = pd.concat(needs)
hh.reset_index(inplace=True,drop=True)
hh.drop(hh[hh['artist'] == 'z'].index,inplace=True)
hh.reset_index(inplace=True,drop=True)


# In[226]:


base = pd.concat([df,hh])
base.reset_index(inplace=True,drop=True)


# In[ ]:


base_node_list = []
for x,y in base[base['artist'] == 'Metallica'].iterrows():
    base_node_list.append( y['influenced_by'] )


# In[480]:


G = nx.Graph()
G = nx.from_pandas_edgelist(base,source='artist',target='influenced_by')
print(nx.info(G))


# In[174]:


Gx = G.subgraph(base_node_list)
G_Base = G.subgraph(['Metallica'])


# In[ ]:


options = {
    'node_color': 'red',
    'node_size': 100,
    'edge_width': 2,
    'width': 800,
    'height': 800,
    'arrows': False,
    'arrowstyle': 'simple',
    'arrowsize':5,
    'margins': 1
}
options_base = {
    'node_color': 'blue',
    'edge_color': 'blue',
    'node_size': 100,
    'edge_width': 2,
    'width': 1000,
    'height': 1000,
    'arrows': True,
    'arrowstyle': 'simple',
    'arrowsize':5
}


# In[237]:


pos=nx.spring_layout(G,k=0.15, iterations=20)
hvnx.draw_networkx(G,pos,**options) *hvnx.draw_networkx_nodes(Gx,pos, node_color='blue', node_size = 200) *hvnx.draw_networkx_nodes(G_Base,pos, node_color='yellow', node_size=400)


# In[75]:


pos=nx.spring_layout(G,k=0.15, iterations=20)
hvnx.draw_networkx(G,pos,**options) *hvnx.draw_networkx_nodes(Gx,pos, node_color='blue', node_size = 200) *hvnx.draw_networkx_nodes(G_Base,pos, node_color='yellow', node_size=400)


# In[238]:


# CLIQUES
for n in G.nodes():
    c=nx.cliques_containing_node(G, nodes=n)
    print("%s belongs to cliques %s" %(n,c))
    
cliques=list(nx.find_cliques(G))
mapping={}
for n in G.nodes():
    if type(n)==str:
        for i,j in enumerate(cliques):
            mapping[i]="Clique of "+", ".join(j)
    if type(n)==int:
        for i,j in enumerate(cliques):
            mapping[i]="Clique of "+", ".join([str(jj) for jj in j])
            
Gclique=nx.make_max_clique_graph(G, create_using=None)
Gclique=nx.relabel_nodes(Gclique,mapping)


# In[ ]:


G1, df = GetListOfRecommendations('Metallica',base,G)


# In[518]:


all_genres = np.unique(base.genres.values).tolist()


# In[382]:


# BASE GENRES FOR METALLICA
seperated_list_genre = base.iloc[0].genres.split(",")


# In[399]:


sim_artists = []
base_artists = []
for genre in seperated_list_genre:
    for item in all_genres:
        if (genre in item):
            artist = base[base['genres'] == item].artist.values[0]
            sim_artists.append([artist,genre,item])
    


# In[414]:


ll = []
liso = []
for x in sim_artists:
    if x[0] not in ll:
        ll.append(x[0])
        liso.append( [ x[0], x[1] ])


# In[418]:


dups = pd.DataFrame(sim_artists,columns=['artist','genre','long_genre'])


# In[508]:


len(dups)


# In[509]:


len(dups[dups.duplicated(subset=['artist'])])


# In[470]:


l = []
names = []
for x in dups.artist.value_counts().keys():
    count = dups.artist.value_counts().get(x)
    if count > 1:
        l.append(count)
        names.append(x)


# In[475]:


import matplotlib.pyplot as plt
x = dups.genre.value_counts()
plt.style.use('fivethirtyeight')
labs = ['Hard Rock','Heavy Metal','Speed/Thrash Metal']
plt.bar(labs,x)
plt.title("Genre Counts")
plt.show()


# In[ ]:


G = nx.Graph()
G = nx.from_pandas_edgelist(g,source='artist',target='influenced_by')
print(nx.info(G))


# In[77]:


pos = nx.layout.spring_layout(Gclique)  
hvnx.draw_networkx(Gclique, pos, **options) 


# In[ ]:


# CLIQUES
for n in G.nodes():
    c=nx.cliques_containing_node(G, nodes=n)
    print("%s belongs to cliques %s" %(n,c))
    
cliques=list(nx.find_cliques(G))
mapping={}
for n in G.nodes():
    if type(n)==str:
        for i,j in enumerate(cliques):
            mapping[i]="Clique of "+", ".join(j)
    if type(n)==int:
        for i,j in enumerate(cliques):
            mapping[i]="Clique of "+", ".join([str(jj) for jj in j])
            
Gclique=nx.make_max_clique_graph(G, create_using=None)
Gclique=nx.relabel_nodes(Gclique,mapping)


# In[239]:


pos = nx.layout.spring_layout(Gclique)  
hvnx.draw_networkx(Gclique, pos, **options) 


# In[ ]:




