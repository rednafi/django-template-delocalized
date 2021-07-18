
<div align="center">

![logo](https://user-images.githubusercontent.com/30027932/126043848-33cbf444-89e0-4c4d-afa0-ea1bfa2e4736.png)

<strong>>> <i>Decouple Your Template Rendering From the Primary Django Application</i> <<</strong>

</div>

## What?

This repository contains the exploration of a POC that was conceived in an attempt to decouple the template rendering part of a Django application from the primary application.

Let's say you have a Django app and you want to detach the templates from it and render them in a separate app. However, you'd still want to have access to all of the models and objects of the primary app.

*This is not a pip installable library, merely a janky demonstration of the core idea.*

## Why?

At my workplace, we were thinking about detaching the template rendering portion of our primary Django app and delegate that to a separate app. This will enable us to develop and deploy the templates at a cadence that is different from the comparatively slower development pace of the main app. Also, the loose coupling implies that the development of these two entities can go on in their separate ways.

## How?

Assume that your primary Django app is called `source` and you want to decouple and develop the templates in another Django app named `target`. The goal is to establish a seamless communication channel between the two entities so that the `target` can house the templates and render them using the `context` objects sent from the `source`.

* Both `source` and `target` will point to the same Postgres database.

* Both the entities will also use the same Redis cache backend.

* The `source` app will use django-rest-framework to expose a GET API. The `view` class of this API will build the `context` object required to render a particular template in the `target` app.

* When this API is called from the `target` app, the corresponding `view` class will push the `context` to the cache. Then the API should return a key to retrieve the `context` from the cache.

* The `target` app will then use the key returned by the API to fetch the `context` object from the same cache backend.

* The `target` app will use the retrieved `context` to render the templates.

* The serialization and the deserialization of the `context` objects are taken care of by Django's built-in cache framework.


## Architecture Details

<details><summary>Click to Expand</summary>

The repository contains the code for two Django applications, the `source` and the `target` app.

### Source App


The `source` app looks like any other Django application. In this demonstration, most of the modules in the `source` app are empty. It uses the Postgres database as its primary data container and Redis for caching purposes. You can find the details in `source/source/settings.py` file.

It contains a single sub app named `app`. In the `app`, there are two models—`Musician` and `Album`. An `Album` has a foreign key relationship with a `Musician`.

```python
# source/app/models.py

from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(
        Musician,
        on_delete=models.SET_NULL,
        null=True,
        related_name="albums",
    )
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

```

Now, if you look into the `source/app/apis.py` file, you'll see that's where the magic happens.

```python

from uuid import uuid4

from django.core.cache import cache
from rest_framework import serializers, views
from rest_framework.response import Response

from .models import Album, Musician


class MusicContextSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    key = serializers.CharField()


class MusicContextAPIView(views.APIView):
    """Returns the cache record key that contains the music context object."""

    def get(self, request):
        # Getting the object querysets.
        musicians = Musician.objects.all()
        albums = Album.objects.all()

        # Generating key to store the context against.
        music_context_key = str(uuid4())

        # Building the context required to render the html.
        music_context_val = {
            "musicians": musicians,
            "albums": albums,
        }

        # Storing the context in the shared cache.
        cache.set(music_context_key, music_context_val)

        # Returning the key to get the context from the other app.
        data = {"key": music_context_key}
        results = MusicContextSerializer(data).data

        return Response(results)
```

Here, we're exposing a GET API that is accessible from `http://localhost:4000/api/v1/music_context`. Notice how the `get` method first queries the database to build the `musicians` and `albums` queryset. Then it constructs the `context` and sends it to the cache with a random UUID key. The API then returns the key and it will later be used by the `target` app to retrieve the `context` object and render the template.


### Target App

The directory structure of the `target` app mimics that of the `source` app. Here, too, the sub app is called `app`. Notice that the `app` folder contains a `templates` directory. The `target` app uses the `context` sent by the `source` and the `templates/index.html` template retrieves the data from the Postgres database using the querysets from the `context`.

In the `target` app, interesting things only happen in the `target/app/views.py` module and the `target/templates/index.html` file.

```python
from __future__ import annotations

import typing
from dataclasses import dataclass
from http import HTTPStatus as http_status

import httpx
from django.core.cache import cache
from django.shortcuts import render
from django.views import View

if typing.TYPE_CHECKING:
    from django.db.models import QuerySet

    from target.app import models as target_models


@dataclass
class MusicContextShape:
    """This is going to be the shape of the retrieved context."""

    musicians: QuerySet[target_models.Musician]
    albums: QuerySet[target_models.Album]


class MusicView(View):
    def get(self, request):
        with httpx.Client(http2=True) as session:
            res = session.get("http://source:4000/api/v1/music_context")
            if res.status_code == http_status.OK:
                key = res.json()["key"]
            else:
                raise httpx.ConnectError("cannot connect to server")

        context = cache.get(key)
        print(context["albums"][0].artist)
        if context.keys() == MusicContextShape.__dataclass_fields__.keys():

            return render(request, "index.html", context)
        else:
            raise ValueError("unexpected context shape")
```

Here, the dataclass `MusicContextShape` is used to validate the expected `context` shape from the cache. Notice that inside the `get` method of the `MusicView` class, `httpx` library was used to make a get API call to the API exposed by the `source` app.

The API returns the cache key where the `context` lives inside the Redis database. The retrieved `context` is then injected into the template. If you take a look at the template, you'll see how it uses the queryset objects inside the `context` to display data. Here's the core content of the template:

```html
...

<div class="container">
  &nbsp;
  <div align="center">
  <h2>Discography</h2>
  </div>
  &nbsp;
  <table class="table">
    <thead class="thead-dark">
      <tr>
        <th>Artist Name</th>
        <th>Preferred Instrument</th>
        <th>Album Name</th>
        <th>Album Released</th>
        <th>Album Rating</th>
      </tr>
    </thead>
    <tbody>
    {% for album in albums %}
      <tr>
        <td>{{album.artist.first_name}} {{album.artist.last_name}}</td>
        <td>{{album.artist.instrument}}</td>
        <td>{{album.name}}</td>
        <td>{{album.release_date}}</td>
        <td>{{album.num_stars}}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

...

```

### Orchestration & Containerization

This demonstration uses Docker and Docker Compose to orchestrate the different entities required for it to work. The 4 primary building blocks of the POC are:

* A `source` app instance which can be regarded as the primary application.

* A `target` app instance which renders the template using the data sent by the `source` app.

* Postgres database as the primary data container. Both the `source` and the `target` app points to this. However, the `target` app never migrates or mutates the database. It has a read-only relationship with the main DB.

* Redis database as the shared cache channel between `source` and `target`.

The simplified topology diagram looks roughly like this:

![topology](https://user-images.githubusercontent.com/30027932/126051355-af1faae6-0a30-4f80-91ea-cfe30cd30fc7.png)


The `docker-compose.yml` file orchestrates them in a stateless fashion. That means data is created and destroyed every time you spin up and put down the containers.

**Migration and mutation of the primary database only happens in the `source` app. The `target` app isn't supposed to migrate or change the DB.**



</details>

## Installation & Exploration

* Make sure you've got Git, Docker, and Docker Compose installed on your machine.

* Clone the repository and head over to the root directory.

* In the root directory, `make run_servers` on your terminal to spin up the orchestra. This will:

    * Start two instances of the `source` and the `target` Django apps.
    * Start a Postgres container that will be shared by the `source` and `target` apps.
    * Start a Redis instance that will act as the shared cache between the two apps.
    * Runs database migration from the `source` app.
    * Runs a script to fill in the Postgres database with some dummy data to render.

* The `source` uses port `4000`, and the `target` app uses port `5000`.

* On your browser, go to `http://localhost:4000/api/v1/music_context/`. The `source` app is serving this API endpoint. Hitting the URL will create the `context`, send it to the cache for the `target` app to pick it up. Also, you should be able to see the following page where the endpoint returns the cache key to fetch the `context` from the other side:

![Screenshot from 2021-07-18 02-03-25](https://user-images.githubusercontent.com/30027932/126048231-a754e0aa-c686-4fc2-bef6-3458925f9c2d.png)


* On another tab, go to `http://localhost:5000/musics/`. This should give you the following result:

![Screenshot from 2021-07-18 02-04-06](https://user-images.githubusercontent.com/30027932/126048233-49fd3162-92c6-4a70-b485-636ed3c7992b.png)


Here, the `context` was passed into the cache by the `source` app. The `target` app then picks it up, injects it into the template, and renders the table.

* Once you're done fooling around with it you can run the following command to shut down and clean up everything.

    ```
    make stop_servers
    ```


## Caveats

* Both `source` and `target` will need to have access to the same models. That means you'll have to copy over the models from `source` to `target`.

* Both `source` and `target` need to point to the same Postgres database. The only benefit the pattern gives you is—you can create and send the complex `context` objects with arbitrary queryset values from the `source` app and use those in the templates that live in the `target` application without any further modification.



<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
