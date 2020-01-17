from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

bd_sidia = create_engine('sqlite:///sidia.db')
app = Flask(__name__)
api = Api(app)

class moviesCategory(Resource):
    def get(self, category):

        conn = bd_sidia.connect()
        query = conn.execute("""
                                SELECT
                                    titles.tconst,
                                    titles.primaryTitle,
                                    titles.originalTitle,
                                    titles.startYear,
                                    ratings.averageRating,
                                    ratings.numVotes
                                FROM
                                    titles
                                INNER JOIN ratings ON ratings.tconst = titles.tconst
                                INNER JOIN genres ON titles.tconst = genres.tconst
                                AND
                                    titles.titleType = "movie"
                                AND
                                    titles.isAdult = 0
                                AND
                                    ratings.averageRating >= 6
                                AND
                                    genres.genres = ?
                                ;""",(category))
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return jsonify(result)



class topMoviesYear(Resource):
    def get(self, year):
        conn = bd_sidia.connect()

        query = conn.execute("""
                                SELECT
                                    titles.tconst,
                                    titles.primaryTitle,
                                    titles.originalTitle,
                                    titles.startYear,
                                    ratings.averageRating,
                                    ratings.numVotes
                                FROM
                                    titles
                                INNER JOIN ratings ON ratings.tconst = titles.tconst
                                INNER JOIN genres ON titles.tconst = genres.tconst
                                AND
                                    titles.titleType = "movie"
                                AND
                                    titles.isAdult = 0
                                AND
                                    ratings.averageRating >= 6
                                AND
                                    titles.startYear = ?
                                ORDER BY
                                    ratings.averageRating DESC, ratings.numVotes DESC
                                LIMIT 10;""",(year))

        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return jsonify(result)

class topMovies(Resource):
    def get(self):
        conn = bd_sidia.connect()

        query = conn.execute("""
                                SELECT
                                    titles.tconst,
                                    titles.primaryTitle,
                                    titles.originalTitle,
                                    titles.startYear,
                                    ratings.averageRating,
                                    ratings.numVotes
                                FROM
                                    titles
                                INNER JOIN ratings ON ratings.tconst = titles.tconst
                                INNER JOIN genres ON titles.tconst = genres.tconst
                                AND
                                    titles.titleType = "movie"
                                AND
                                    titles.isAdult = 0
                                AND
                                    ratings.averageRating >= 6
                                ORDER BY
                                    ratings.averageRating DESC, ratings.numVotes DESC
                                ;""")
        result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
        return jsonify(result)



api.add_resource(topMovies, '/ranking')
api.add_resource(topMoviesYear, '/ranking/<year>')
api.add_resource(moviesCategory, '/movies/<category>')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port="5000")
