import json

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

def save_album(al_data):
    first_name = al_data["first_name"]
    last_name = al_data["last_name"]
    filename = "{}-{}.json".format(first_name, last_name)

    with open(filename, "w") as fd:
        json.dump(al_data, fd)
    return filename

@route("/albums", method="POST")
def artist():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")
    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        res = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        res = HTTPError(409, str(err))
    else:
        res = "Альбом сохранен"
    return res

    resource_path = save_album(al_data)
    print("User saved at: ", resource_path)

    return "Данные успешно сохранены"


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result1 = "<h1 align='center'>Количество альбомов у {} {}</h1>".format(artist, str(len(album_names)))
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
        return result1, result
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)