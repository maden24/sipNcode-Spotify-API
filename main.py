import os
import json
import base64
from requests import post, get
import pandas as pd

##Client_id and secret provided by the app
client_id="XXXXXXX"
client_secret="XXXXXXX"

#have to convert client id and secret to binary for the get request
def get_token():
    auth_string=client_id + ":" + client_secret
    auth_bytes= auth_string.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes), "utf-8")
    ##endpoint for api
    url= "https://accounts.spotify.com/api/token"

    headers={
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={"grant_type": "client_credentials"}
    result= post(url, headers=headers, data=data)
    #store the access token in json to make it easier to use
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

#return's the token's header to be used in other functions
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    #endpoint 
    url= "https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    #query that specifies what we're looking for, what type it is, and how many values we want to return
    query=f"?q={artist_name}&type=artist&limit=1"

    query_url= url + query
    result= get(query_url, headers=headers)
    json_result= json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print("No artist with this name exists...")
        return None
    else:
        return json_result[0]


def get_songs_by_artist(token, artist_id):
    #endpoint
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers=get_auth_header(token)
    result=get(url, headers=headers)
    json_result=json.loads(result.content)["tracks"]
    return json_result

def get_related_artist(token, artist_id):
    #endpoint
    url=f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers=get_auth_header(token)
    result=get(url, headers=headers)
    json_result=json.loads(result.content)["artists"]
    return json_result




token=get_token()
result= search_for_artist(token, "Drake")
artist_id= result["id"]
songs=get_songs_by_artist(token,artist_id)
related_artists=get_related_artist(token,artist_id)

for idx, song in enumerate(songs):
    print(f"{idx+1}.{song['name']}")

for idx, artist in enumerate(related_artists):
    print(f"{idx+1}.{artist['name']}")

