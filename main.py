from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

API_KEY = os.environ.get("TMDB_KEY")
API_READ_ACCESS_TOKEN = ("eyJhbGciOiJIUzI1NiJ9"
                         ".eyJhdWQiOiI5NjM5ZjY4Mzc1OTg3ZDc4MGM0NWYxNWNjZDU1ZDVhNCI"
                         "sIm5iZiI6MTcxOTk1MTE0NS43NTMwOTksInN1YiI6IjY2ODQ1ZTNjN"
                         "TZiMDdhMzY3NTFlNmJhMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW"
                         "9uIjoxfQ.K4NmRFY-a7eb3mNYYr1AdiKue_RSS6AztpDjDPMk-Dw")


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///posts.db")
db.init_app(app)


# CREATE DB
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# CREATE FORM
class MovieForm(FlaskForm):
    Rating = StringField("Your Rating e.g. 7.5", validators=[DataRequired()])
    Review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


# CREATE FORM 2
class AddMovieForm(FlaskForm):
    movieTitle = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movies).order_by(Movies.rating.desc()))
    allMovies = movies.scalars().all()  # convert ScalarResult to Python List
    rank = 1
    for movie in allMovies:
        movie.ranking = rank
        rank += 1
    db.session.commit()
    return render_template("index.html", movieList=allMovies)


@app.route("/edit", methods=['GET', 'POST'])
def update():
    form = MovieForm()
    movieID = request.args.get('id')
    movieSelected = db.get_or_404(Movies, movieID)
    if form.validate_on_submit():
        movieSelected.rating = form.Rating.data
        movieSelected.review = form.Review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movieSelected, form=form)


@app.route("/delete")
def delete():
    movieID = request.args.get('id')
    movieDeleted = db.get_or_404(Movies, movieID)
    db.session.delete(movieDeleted)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movieName = str(form.movieTitle.data)
        url = f"https://api.themoviedb.org/3/search/movie?query={movieName.replace(" ", "+")}&api_key={API_KEY}"
        r = requests.get(url)
        data = r.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/find")
def find():
    movieID = request.args.get('id')
    if movieID:
        url = f"https://api.themoviedb.org/3/movie/{movieID}?api_key={API_KEY}"
        r = requests.get(url)
        data = r.json()
        imageURL = "https://image.tmdb.org/t/p/w780"
        movieAdded = Movies(
            title=data["original_title"],
            year=int(data["release_date"][:4]),
            description= data["overview"],
            img_url=f"https://image.tmdb.org/t/p/w780/{data["poster_path"]}"
        )
        db.session.add(movieAdded)
        db.session.commit()
        return redirect(url_for("update", id=movieAdded.id))


if __name__ == '__main__':
    app.run(debug=False)
