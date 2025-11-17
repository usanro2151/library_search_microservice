Media Library Search & Filter Microservice

This microservice allows clients to search and filter movies in a user’s media library by title, genre, and
rating, returning results in JSON format.
Communication Contract
- Primary Platform: Microsoft Teams for all communication, file sharing, and coordination.
- Response Time: Team members will respond within 24 hours.
- Weekly and Daily Check-Ins: Short check-ins will happen weekly or daily if needed to share progress, ask questions, and stay
aligned.
- Team Culture: We will be respectful, supportive, and inclusive. This agreement will not be changed
after being set.

Base URL:
"https://movies-478502.uc.r.appspot.com"

Requesting Data From the Microservice
GET /movies
Returns all movies OR filters them using optional query parameters.
Query Parameters
- title — search by title substring
- genre — filter by genre
- rating — filter by minimum rating
You may combine them:
/movies?title=in&genre;=Sci-Fi&rating;=8

Example Request (Search by title)
curl -X GET "https://movies-478502.uc.r.appspot.com/movies?title=inception"

Example Request (Filter by genre)
curl -X GET "https://movies-478502.uc.r.appspot.com/movies?genre=Action" 

Example Request (Filter by rating ≥ 8)
curl -X GET "https://movies-478502.uc.r.appspot.com/movies?rating=8"
Receiving Data From the Microservice
Example Response:
[
{
"id": 101,
"title": "Inception",
"genre": "Sci-Fi",
"rating": 8.8
},
{
"id": 102,
"title": "Interstellar",
"genre": "Sci-Fi",
"rating": 8.6
}
]
Running the Microservice
pip install -r requirements.txt
python main.py

Example Client Integration:
import requests
response = requests.get("https://movies-478502.uc.r.appspot.com/movies?genre=Sci-Fi")
movies = response.json()
print(movies)
