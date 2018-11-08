from datetime import datetime as dt
from functools import reduce

def set_id():
    cont = 1
    while True:
        yield cont
        cont += 1


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character

    def __repr__(self):
        return self.name

class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = [i for i in args]

    def __repr__(self):
        return self.title

def popular(pelis, num):
    lista = list(filter(lambda x: x.rating > num, pelis))
    return lista

def with_genres(pelis, num):
    lista = list(filter(lambda x: len(x.genres) > num, pelis))
    return lista

def tops_of_genres(generador, genero):
    generos = list(filter(lambda x: genero in x.genres, generador))
    generos.sort(key = lambda p: p.rating, reverse = True)
    if len(generos) > 10:
        return generos[:10]
    return generos

def actor_rating(cast, pelis, actor):
    act = filter(lambda x: x.name == actor, cast)
    sus_pelis = list(linea.movie for linea in act)
    ratings = list(filter(lambda x: x.title in sus_pelis, pelis))
    real = list(linea.rating for linea in ratings)
    valor = reduce(lambda x, y: x + y, real)
    return valor/len(ratings)

def compare_actors(cast, pelis, actor1, actor2):
    a = actor_rating(cast, pelis, actor1)
    b = actor_rating(cast, pelis, actor2)
    if a > b:
        print(actor1)
    else:
        print(actor2)

def movies_of(cast, actor):
    act = filter(lambda x: x.name == actor, cast)
    sus_pelis = list((linea.movie, linea.character) for linea in act)
    return sus_pelis

def from_year(pelis, ano):
    return list(filter(lambda x: x.release.year == ano, pelis))


if __name__ == "__main__":
    with open('movies.txt', 'r') as f:
        pelis = (Movie(*linea.strip().split(",")[1:]) for linea in f)
        pelis = list(pelis)

    with open('cast.txt', 'r') as n:
        cast = (Cast(*linea.strip().split(",")) for linea in n)
        cast = list(cast)


print(popular(pelis, 40))
print(with_genres(pelis, 5))
print(tops_of_genres(pelis, "Family"))
print(actor_rating(cast,pelis,"Allison Janney"))
compare_actors(cast, pelis, "Natalie Portman", "Will Smith")
print(movies_of(cast, "Allison Janney"))
print(from_year(pelis, 2015))
