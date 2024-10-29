import requests
import json
import time

# Single access token
access_token = 'YOUR_ACCESS_TOKEN_HERE'

# Load data from JSON file
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load the dataset (only one file)
data_0 = load_json_file("StreamingHistory_music_0.json")

# Dictionary to cache audio features for tracks already processed
audio_features_cache = {}

def should_update_features(item):
    return (
        item.get('danceability') is None or
        item.get('energy') is None or
        item.get('valence') is None or
        item.get('loudness') is None or
        item.get('instrumentalness') is None
    )

# Preload cache from existing data in data_0 to reuse processed tracks' features
def preload_cache(data):
    for item in data:
        # If the song already has values, store it in the cache
        if not should_update_features(item):
            song_key = f"{item['trackName']} by {item['artistName']}"
            audio_features_cache[song_key] = {
                'danceability': item.get('danceability'),
                'energy': item.get('energy'),
                'valence': item.get('valence'),
                'loudness': item.get('loudness'),
                'instrumentalness': item.get('instrumentalness')
            }

# Preload from StreamingHistory_music_0.json
preload_cache(data_0)

def get_audio_features(track_name, artist_name):
    search_url = f'https://api.spotify.com/v1/search?q=track:{track_name} artist:{artist_name}&type=track'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        search_results = response.json()
        tracks = search_results.get('tracks', {}).get('items', [])

        if tracks:
            track_id = tracks[0]['id']
            audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            audio_features_response = requests.get(audio_features_url, headers=headers)

            if audio_features_response.status_code == 200:
                return audio_features_response.json()
    elif response.status_code == 429:
        # Rate limit handling: wait and then retry
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limit reached. Waiting for {retry_after} seconds...")
        time.sleep(retry_after)
        return get_audio_features(track_name, artist_name)
    else:
        print(f"Error retrieving audio features for {track_name} by {artist_name}: {response.status_code}")
    
    return {}

def add_features_to_data(data):
    for index, item in enumerate(data):
        track_name = item['trackName']
        artist_name = item['artistName']
        
        # Generate a unique key for the song
        song_key = f"{track_name} by {artist_name}"
        
        # Check if the song is already in the cache
        if song_key in audio_features_cache:
            # Copy features from the cache if already processed
            cached_features = audio_features_cache[song_key]
            item.update(cached_features)
        elif should_update_features(item):
            # Fetch new audio features from the API
            audio_features = get_audio_features(track_name, artist_name)

            # Store specified audio features in a dictionary
            features = {
                'danceability': audio_features.get('danceability'),
                'energy': audio_features.get('energy'),
                'valence': audio_features.get('valence'),
                'loudness': audio_features.get('loudness'),
                'instrumentalness': audio_features.get('instrumentalness')
            }

            # Cache the features using song_key
            audio_features_cache[song_key] = features

            # Update the item with the new features
            item.update(features)

            # Print progress
            if (index + 1) % 100 == 0:
                print(f"Processed {index + 1} out of {len(data)} tracks...")

            # Save data after every 100 tracks
            if (index + 1) % 100 == 0:
                save_json_file("StreamingHistory_music_0.json", data)

    return data

# Save updated data back to JSON file
def save_json_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Failed to save data: {e}")

# Add features to your data_0 using preloaded cache
updated_data = add_features_to_data(data_0)

# Final save after all processing is complete
save_json_file("StreamingHistory_music_0.json", updated_data)

print("Finished updating data with audio features.")
