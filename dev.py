from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd

client_id = "dec967d105634e55942f249a600780f1"
client_secret = "33524391083f4259a50bb489370a48a6"
username = "31nfsp7vapk4zh24xzvw3lkavx5e"
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'
import requests
from datetime import datetime
from typing import List
import spotipy
import spotipy.util as util
from os import listdir
import pandas as pd

client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_api_id(track_name,artist):
   
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + 
    'BQCJ0uPWrjyfgc16bHtXR88A0UY8_h3Zz4coFXJ0H6zKr5wtwotgn4AxvWDPyHWk79UsQNj74AqCBlvihGH29LIXv7rV33_UhFQCVAxTl9TVX3kX3ozP5Koiqxe3WQq2_dUExDkZQopfq5Q7vaBa5zUEUov7pwqsXHB93yKn6JcAyUoyDfWokjftura7jZTSwQIZ1GSRAPj8ZtW68vANtQFNgaBsi6nwNbLsA2i3K1fg5UJf4a-IzENjrUDXz-KUKHP-D-JRWoRxwFMLwsRZ87Gh'
    }
    
    params = [
    ('q', track_name),
    ('type', 'track'),
    ]
    
    if artist: 
        params.append(('artist', artist))
        
    try:
        response = requests.get('https://api.spotify.com/v1/search', 
                    headers = headers, params = params, timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None
tr=get_api_id("Althea","Grateful Dead")
print(tr)
features = sp.audio_features(tracks=[tr])
#print(features)
df_dic1={}

d=pd.read_json('./MyData/StreamingHistory0.json')

#d.to_csv('streamingHistory0.csv',index=False)

for i in range(9000,10000):
   tr_=get_api_id(d.iloc[i]["trackName"],d.iloc[i]["artistName"])
   features=sp.audio_features(tracks=[tr_])
   df=pd.DataFrame.from_dict(features)
   df["track"]=d.iloc[i]["trackName"]
   df["artist"]=d.iloc[i]["artistName"]
   df["msPlayed"]=d.iloc[i]["msPlayed"]
   df['datetime'] =   datetime.strptime(d.iloc[i]['endTime'], '%Y-%m-%d %H:%M')    
   df_dic1[i]=df
df_list=[]
for i in range(9000,10000):
  df_list.append(df_dic1[i])

whole=pd.concat(df_list)
whole.to_csv("streaming0_11.csv")
   