import requests
    
def fetch_movie_data(movie_id, api_key, base_url='https://api.themoviedb.org/3'):
    """Fetch movie data from TMDb API"""
    url = f"{base_url}/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'append_to_response': 'credits'  # Get cast and crew information
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie with ID {movie_id}: {e} does not exist.")
        return None

def fetch_all_movies(movie_ids, api_key):
    print(f"Fetch data for all {len(movie_ids)} movies")
    movie_ids = sorted(movie_ids)
    movies_data = []
    
    for movie_id in movie_ids:
        print(f"Fetching data for movie ID: {movie_id}")
        movie_data = fetch_movie_data(movie_id, api_key)
        
        if movie_data and 'id' in movie_data:
            movies_data.append(movie_data)
        else:
            print(f"Failed to fetch data for movie with ID: {movie_id}")
    
    return movies_data