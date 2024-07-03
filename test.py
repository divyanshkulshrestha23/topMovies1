import requests
name = "The+Matrix"
API_KEY = "9639f68375987d780c45f15ccd55d5a4"
url = f"https://api.themoviedb.org/3/search/movie?query={name}&api_key={API_KEY}"

API_READ_ACCESS_TOKEN = ("eyJhbGciOiJIUzI1NiJ9"
                         ".eyJhdWQiOiI5NjM5ZjY4Mzc1OTg3ZDc4MGM0NWYxNWNjZDU1ZDVhNCI"
                         "sIm5iZiI6MTcxOTk1MTE0NS43NTMwOTksInN1YiI6IjY2ODQ1ZTNjN"
                         "TZiMDdhMzY3NTFlNmJhMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW"
                         "9uIjoxfQ.K4NmRFY-a7eb3mNYYr1AdiKue_RSS6AztpDjDPMk-Dw")

params = {"query": "The Matrix"}
movieID = 603
url = f"https://api.themoviedb.org/3/movie/{movieID}"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NjM5ZjY4Mzc1OTg3ZDc4MGM0NWYxNWNjZDU1ZDVhNCIsIm5iZiI6MTcxOTk1MjE5NC44NDA5NTYsInN1YiI6IjY2ODQ1ZTNjNTZiMDdhMzY3NTFlNmJhMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sntVCxXxkqmCPfJxqGRGtSEyeb6CFEe66as0wPtOJTg"
}
r = requests.get(url, headers=headers)
data = r.json()['original_title']
print(data)