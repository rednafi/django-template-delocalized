from __future__ import annotations

import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "source.settings"
django.setup()

import typing
from datetime import datetime

from django.db import models

from .. import models as app_models

if typing.TYPE_CHECKING:
    from typing import Iterable

    from django.db.models import QuerySet


def create_musicians(
    *,
    first_names: Iterable[str],
    last_names: Iterable[str],
    instruments: Iterable[str],
) -> None:

    app_models.Musician.objects.bulk_create(
        [
            app_models.Musician(
                first_name=first_name, last_name=last_name, instrument=instrument
            )
            for first_name, last_name, instrument in zip(
                first_names, last_names, instruments
            )
        ]
    )


def create_albums(
    *,
    artists: QuerySet[app_models.Musician],
    names: Iterable[str],
    release_dates: Iterable[models.Datefield],
    num_stars_seq: Iterable[int],
) -> None:

    app_models.Album.objects.bulk_create(
        [
            app_models.Album(
                artist=artist, name=name, release_date=release_date, num_stars=num_stars
            )
            for artist, name, release_date, num_stars in zip(
                artists, names, release_dates, num_stars_seq
            )
        ]
    )


print("Creating musicians...")

first_names = [
    "Santiago",
    "Winston",
    "Aubree",
    "Brynlee",
    "Maximillian",
    "Kameron",
    "Areli",
    "Robert",
    "Triston",
    "Matthias",
]

last_names = [
    "Hammond",
    "Harrell",
    "Conrad",
    "Anderson",
    "Griffin",
    "Turner",
    "Atkinson",
    "Lucas",
    "Jacobs",
    "Douglas",
]

instruments = [
    "Electric Guitar",
    "Keyboard",
    "Piano",
    "Guitar",
    "Drums",
    "Violin",
    "Saxophone",
    "Flute",
    "Cello",
    "Clarinet",
]

create_musicians(
    first_names=first_names,
    last_names=last_names,
    instruments=instruments,
)

print("Creating albums...")
artists = app_models.Musician.objects.all()
names = [
    "Level",
    "Undesirable",
    "Awake",
    "Underwear",
    "Hissing",
    "Legal",
    "Hungry",
    "Street",
    "Vein",
    "Sun",
]
release_dates = [
    datetime(year, month, day)
    for year, month, day in zip(range(2010, 2020), range(1, 13), range(10, 20))
]
num_stars_seq = list(range(1, 10))

create_albums(
    artists=artists,
    names=names,
    release_dates=release_dates,
    num_stars_seq=num_stars_seq,
)
