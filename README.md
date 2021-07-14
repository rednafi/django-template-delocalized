<div align="center">

<h1>Django Template Delocalized</h1>
<strong>>> <i>Decouple Your Django Templates From the Primary Monolith</i> <<</strong>

&nbsp;

</div>

![img](https://user-images.githubusercontent.com/30027932/122619075-6a87b700-d0b1-11eb-9d6b-355446910cc1.png)



## Preface

The idea is simple. Let's say you have a Django app and you want to decouple the templates from it and render them from a separate app. However, you'd still like to have access to all of the models and objects of the primary app. To do so, let's assume your primary app is called `source` and the decoupled templates lives in another app named `target`.

* The `source` app will have a redis cache backend.
* The `source` app will use django-rest-framework to expose a GET API.
* The `target` app will also point to the same Redis cache backend as the `source`.
* The `target` app will call the GET API exposed by the `source`.
* When the `target` app makes the API call, the `source` will serialize and push the context object required to render the templates into the cache. Then the API should return a key to retrive the context from the cache.
* The `target` app will then use the key returned by the API to fetch the context object from the same cache backend.
* The `target` app will deserialize the context object and use that to render the templates.

## Installation

Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.


## Exploration

It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).


<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
