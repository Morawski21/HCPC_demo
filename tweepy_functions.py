import tweepy as tw
import pandas as pd

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
            'description': user.description}
            results = results.append([userdata], ignore_index=True)
    return results


def get_followers(user, n_followers = 20):
    '''Returns a DataFrame with followers' data for one profile.
    
       Parameters:
       user (str): Username of the Twitter profile
       n_followers (int): Number of followers to return
    '''
    
    results = pd.DataFrame()  
    followers_raw = tw.Cursor(api.followers, user).items(n_followers)
    for follower in followers_raw:
        userdata = {
        'query': "",
        'id': follower.id,
        'name': follower.name,
        'screen_name': follower.screen_name,
        'friends': follower.friends_count,
        'followers': follower.followers_count,
        'description': follower.description}
        results = results.append([userdata], ignore_index=True)
    return results