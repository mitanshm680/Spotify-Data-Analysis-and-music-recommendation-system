import requests

# Your Client ID and Client Secret
CLIENT_ID = 'YOUR CLIENT_ID'
CLIENT_SECRET = 'YOUR CLIENT_SECRET'

# Function to get an access token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(
        url,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to get access token: ' + response.text)

# Get the access token
access_token = get_access_token()
print(f'Access Token: {access_token}')
