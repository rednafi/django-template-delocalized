
<div align="center">

![logo](https://user-images.githubusercontent.com/30027932/126043848-33cbf444-89e0-4c4d-afa0-ea1bfa2e4736.png)

<strong>>> <i>Decouple Your Template Rendering From the Primary Django Application</i> <<</strong>

</div>

## What?

This repository contains the exploration of a POC that might help you decouple the template rendering part of a Django application from the main application.

Let's say you have a Django app and you want to detach the templates from it and render them in a separate app. However, you'd still want to have access to all of the models and objects of the primary app.

This is not a pip installable library, merely a janky demonstration of the core idea.

## Why?

At my workplace, we're thinking about detaching the template rendering portion of our primary Django app and delegate that to a separate app. This will enable us to develop and deploy the templates at a cadence that is different from the comparatively slower pace of the main app. Also, the loose coupling implies that the development of these two entities can go on in their separate ways.

## How?

Assume that your primary Django app is called `source` and you want to decouple and develop the templates in another Django app named `target`. The goal is to establish a seamless communication channel between the two entities so that the `target` can house the templates and render them using the *context* objects sent from the `source`.

* Both `source` and `target` will point to the same Postgres database.

* Both the entities will also use the same Redis cache backend.

* The `source` app will use [django-rest-framework]() to expose a GET API. The serializer of this API will build the *context* object required to render a particular template in the `target` app.

* When this API is called from the `target` app, it'll push the *context* to the cache. Then the API should return a key to retrieve the *context* from the cache.

* The `target` app will then use the key returned by the API to fetch the *context* object from the same cache backend.

* The `target` app will use the retrieved *context* to render the templates.

* The serialization and the deserialization of the *context* objects are taken care of by Django's built-in cache framework.


## Architecture Details

<details><summary>Click to Expand</summary>

The repository contains the code for two Django applications, the `source` and the `target` app.

**TODO:**
* Fill in the architecture details.
* Add diagrams to make the end-to-end pipeline clearer.

</details>

## Installation & Exploration

* Make sure you've got Git, Docker, and Docker Compose installed on your machine.

* Run `make run_servers` to spin up the orchestra. This will:

    * Start two instances of the `source` and the `target` Django apps.
    * Start a Postgres container that will be shared by the `source` and `target` apps.
    * Start a Redis instance that will act as the shared cache between the two apps.
    * Runs database migration from the `source` app.
    * Runs a script to fill in the Postgres database with some dummy data to render.

* The `source` uses port `4000`, and the `target` app uses port 5000.

* On your browser, go to `http://localhost:4000/api/v1/music_context/`. The `source` app is serving this API endpoint. Hitting the URL will create the *context*, send it to the cache for the `target` app to pick it up. Also, you should be able to see the following page where the endpoint returns the cache key to fetch the *context* from the other side:

![Screenshot from 2021-07-18 02-03-25](https://user-images.githubusercontent.com/30027932/126048231-a754e0aa-c686-4fc2-bef6-3458925f9c2d.png)


* On another tab, go to `http://localhost:5000/musics/`. This should give you the following result:

![Screenshot from 2021-07-18 02-04-06](https://user-images.githubusercontent.com/30027932/126048233-49fd3162-92c6-4a70-b485-636ed3c7992b.png)


Here, the *context* was passed into the cache by the `source` app, and the `target` app picks it, injects it into the template, and renders the table.


## Caveats

* Both `source` and `target` will need to have access to the same models. That means you'll have to copy over the models from `source` to `target`.

* Both `source` and `target` need to point to the same Postgres database. The only benefit the pattern gives you is—you can create and send the complex *context* objects with arbitrary queryset values from the `source` app and use those in the templates that live in the `target` application without any further modification.



<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
