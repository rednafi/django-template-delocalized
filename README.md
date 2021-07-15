![My Post](https://user-images.githubusercontent.com/30027932/125779260-dfbc313f-284f-4440-9ac8-62fd602b0d5b.png)


<div align="center">

<strong>>> <i>Decouple Your Django Templates From the Primary Monolith</i> <<</strong>

&nbsp;

</div>


## Preface

The idea is simple. Let's say you have a Django app and you want to decouple the templates from it and render them from a separate app. However, you'd still like to have access to all of the models and objects of the primary app. To do so, let's assume your primary app is called `source` and the decoupled templates lives in another app named `target`.

* The `source` app will have a redis cache backend.
* The `source` app will use django-rest-framework to expose a GET API.
* The `target` app will also point to the same Redis cache backend as the `source`.
* The `target` app will call the GET API exposed by the `source`.
* When the `target` app makes the API call, the `source` will serialize and push the context object required to render the templates into the cache. Then the API should return a key to retrive the context from the cache.
* The `target` app will then use the key returned by the API to fetch the context object from the same cache backend.
* The `target` app will deserialize the context object and use that to render the templates.


## Caveats

* Both `source` and `target` will need to have access to the same models.



<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
