import jinja2
import re
import os
import urllib
import webapp2
import webbrowser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)


class Movie():
    """
    A class Movie to wrap up all of the attributes of movie objects and
    to play their Youtube trailers in the webbrowser.
    """
    def __init__(self, movie_title, release_year, movie_storyline, poster_image, trailer_youtube):
        self.title = movie_title
        self.release_year = release_year
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)


# A single movie entry HTML template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
    <h4>Released in {release_year}</h4>
</div>
'''


def create_movie_tiles_content(movies):
    # A function that dynamically generates HTML content using the single movie HTML template
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            release_year=movie.release_year,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

# Create individual movie objects for the web page using the class Movie
ratatouille = Movie(
                    "Ratatouille", "2007", "A rat is a chef in Paris", 
                    "https://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg",
                    "https://www.youtube.com/watch?v=c3sBBRxDAqk")

the_fifth_element = Movie(
                    "The Fifth Element", "1997","A taxi driver and an alien girl save the world",
                    "https://upload.wikimedia.org/wikipedia/en/6/65/Fifth_element_poster_%281997%29.jpg",
                    "https://www.youtube.com/watch?v=VkX7dHjL-aY")

casino_royale = Movie(
                    "Casino Royale", "2006", "James Bond defeats a terrorist financier",
                    "https://upload.wikimedia.org/wikipedia/en/1/15/Casino_Royale_2_-_UK_cinema_poster.jpg",
                    "https://www.youtube.com/watch?v=fl5WHj0bZ2Q")

jurassic_park = Movie(
                    "Jurassic Park", "1993", "A bioengineer breeds dinos from fossil DNA",
                    "https://upload.wikimedia.org/wikipedia/en/e/e7/Jurassic_Park_poster.jpg",
                    "https://www.youtube.com/watch?v=lc0UehYemQA")

the_silence_of_the_lambs = Movie(
                    "The Silence of the Lambs", "1991", "An FBI trainee captures a serial killer",
                    "https://upload.wikimedia.org/wikipedia/en/8/86/The_Silence_of_the_Lambs_poster.jpg",
                    "https://www.youtube.com/watch?v=ZWCAf-xLV2k")

the_matrix = Movie(
                    "The Matrix", "1999", "A computer programmer hacks into the real world",
                    "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
                    "https://www.youtube.com/watch?v=m8e-FF8MsqU")

# Create a list of all the instances of the class Movie to be rendered
movies = [ratatouille, the_fifth_element, casino_royale, jurassic_park,
                    the_silence_of_the_lambs, the_matrix]

# Dynamically generate HTML for the web application from the movie list and the function
movie_tiles=create_movie_tiles_content(movies)

# Render the web page using the jinja template
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('Movies.html')
        self.response.write(template.render(movie_tiles = movie_tiles))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)