import streamlit as st

import pandas as pd
import tweepy as tw
import joblib
import numpy as np

from credentials import *

CURRENT_THEME = "blue"
IS_DARK_THEME = True
EXPANDER_TEXT = """
    This is a custom theme. You can enable it by copying the following code
    to `.streamlit/config.toml`:
    ```python
    [theme]
    primaryColor = "#E694FF"
    backgroundColor = "#00172B"
    secondaryBackgroundColor = "#0083B8"
    textColor = "#C6CDD4"
    font = "sans-serif"
    ```
    """

# Function for retrieving data
def query_search(query, pages=1):
    '''Returns a DataFrame with users' data for a query.
    
       Parameters:
       query (str): Query to search for
       pages (int): Number of pages with results to retrieve 
                    (1 page = 20 users)
    '''
    results = pd.DataFrame()
    for n in [n + 1 for n in range(pages)]:   
        users_raw = api.search_users(query, page=n)
        for user in users_raw:
            userdata = {
            'query': "",
            'id': user.id,
            'name': user.name,
            'screen_name': user.screen_name,
            'friends': user.friends_count,
            'followers': user.followers_count,
            'description': user.description,
            'prediction': np.NaN}
            results = results.append([userdata], ignore_index=True)
    return results
 
   
# Load the classifier
clf = joblib.load("rfc_86.pkl")

# Set up Tweepy

# Authorize and set access to the API
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Call the API
api = tw.API(auth)

# simple_streamlit_app.py

st.image("graphics/logo.png")

"demo description"

# Declare a form and call methods directly on the returned object
form = st.form(key='my_form')
query = form.text_input('Search for Twitter profiles', "oncologist")
submit_button = form.form_submit_button(label='Search')

if submit_button:
   # Get users
   df = query_search(query)
   
   # Preprocessing
   # Change NaN to arbitrary string - improves performance
   df.description = df.description.fillna('arbitraryemptydescription')
   # Concatenate name and description
   X = df.name + " " + df.description
   
   # Predict labels and change to text
   df.prediction = [clf.predict(pd.Series(profile))[0] for profile in X]
   df.prediction = df.prediction.map({1: 'HCP', 0: 'non-HCP'})
   
   
   # Green text for predicted HCPs
   def color_hcp(val):
       """
       Takes a scalar and returns a string with
       the css property `'color: red'` for negative
       strings, black otherwise.
       """
       color = '#00a569' if val == 'HCP' else 'grey'
       return 'color: %s' % color
   
   # Start index from 1
   df.index += 1
   
   # Subset relevant columns and stylize
   columns = ['name', 'followers', 'description', 'prediction']
   subset = df[columns].style.applymap(color_hcp)
   
   # Display dataframe
   st.table(subset)
