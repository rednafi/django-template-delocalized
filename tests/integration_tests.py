"""
These integration tests assume that all the docker containers are running.
The tests are not meant to be run outside of a docker container.

To execute the tests, run:

make start_tests

"""

from http import HTTPStatus

import httpx
from redis.client import Redis

redis = Redis(host="redis", port=6380, db=1)


def call_music_context_api() -> httpx.Response:
    """Calling the music context API running on the 'source' app instance."""
    with httpx.Client() as session:
        response = session.get("http://source:4000/api/v1/music_context")
        return response


def test_music_context_api() -> None:
    """Tests whether the 'Music Context API' returns the proper payload.
    This test runs against the 'source' app instance."""

    response = call_music_context_api()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()["key"], str)


def test_cache_injection() -> None:
    """Tests whether the 'Music Context API' has injected the context in the
    Redis cache. This test runs against the 'source' app instance."""

    response = call_music_context_api()
    key = response.json()["key"]

    # Underneath Django adds ':1:' prefix before the key since the payload lives
    # in Redis DB 1.
    context_raw = redis.get(f":1:{key}")
    assert isinstance(context_raw, bytes)


def test_musics_page() -> None:
    """Tests whether the 'Musics' page loads properly.
    This test runs against the 'target' app instance."""

    with httpx.Client() as session:
        response = session.get("http://target:5000/musics")
        assert response.status_code == HTTPStatus.OK
