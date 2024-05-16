import streamlit as st
import numpy as np
import pandas as pd
df=pd.read_csv(r"C:\Users\DELL\Downloads\ex.csv")
df.dropna(inplace=True)
df=df.drop_duplicates()
l=[]
for i in df['Song-Name']:
    l.append(i)

st.header('Song Recommendation')
st.header('')
Music1 = st.selectbox("Select the songs You like :",l)
df['Album/Movie']=df['Album/Movie'].str.replace(' ','')
df['Singer/Artists']=df['Singer/Artists'].str.replace(' ','')
df['Singer/Artists']=df['Singer/Artists'].str.replace(',',' ')
df['tags']=df['Singer/Artists']+' '+df['Genre']+' '+df['Album/Movie']+' '+df['User-Rating']
new_df=df[['Song-Name','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=2000)
vectors=cv.fit_transform(new_df['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)
new_df.rename(columns={'Song-Name':'title'},inplace=True)z
def recommend(music):
    music_index=new_df[new_df['title']==music].index[0]
    distances=similarity[music_index]
    music_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    st.header("Recommendation:")
    for i in music_list:
        st.text(new_df.iloc[i[0]].title)

st.header('')
if(st.button("Click me")):recommend(Music1)
import pickle
pickle.dump(new_df,open('musicrec.pkl','wb'))
pickle.dump(similarity,open('similarities.pkl','wb'))