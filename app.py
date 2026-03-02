import os

from apputil import Genius


def main():
    access_token = os.getenv("GENIUS_ACCESS_TOKEN")

    genius = Genius(access_token)

    artists = [
        "Audioslave",
        "Nirvana",
        "Red Hot Chili Peppers",
        "System of a Down",
    ]

    df = genius.get_artists(artists)

    print(df)


if __name__ == "__main__":
    main()