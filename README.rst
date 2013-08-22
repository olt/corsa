Corsa
=====

Corsa proxies HTTP requests, adds `CORS headers <http://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_ and can also serve your static web application.

Features:

- proxy requests for ``/proxy/http://host/path`` to ``http://host/path``
- set ``Access-Control-Allow-Origin`` headers
- support for CORS preflight requests
- support for GET, HEAD, POST, PUT, DELETE, OPTIONS
- serve static content from ``/app/`` (``--app-dir``)
- limit proxy hosts (``--allow-proxy``)
- limit origin (``--allow-origin``)


Corsa is powered by Python and Tornado and is licensed under the MIT license.


Example
-------

You have a static web app in ``./mywebapp`` that loads images from ``http://imagesource.example`` and stores them in a local CouchDB?
Due to the cross-domain restrictions of all modern browsers, you won't be able to access the image data and you won't be able to access the CouchDB.
Cross-origin resource sharing (CORS) is a mechanism to work around that and Corsa will set the appropriate CORS headers for you.

Start Corsa::

    % corsa --app-dir ./mywebapp --allow-proxy http://imagesource.example,http://localhost:5984

Configure your web app to use ``/proxy/http://imagesource.example`` as the image source and ``/proxy/http://localhost:5984`` as your CouchDB URL and go to ``http://localhost:8888/app/index.html``.


If you application is allready running at ``http://localhost:8080``::

    % corsa --allow-proxy http://imagesource.example,http://localhost:5984 --allow-origin http://localhost:8080


Options
-------

To proxy specific URLs::

    % corsa --allow-proxy http://httpbin.org --allow-origin ALL

    % curl http://localhost:8888/proxy/http://httpbin.org/get -D -
    HTTP/1.1 200 OK
    Access-Control-Allow-Origin: *
    [...]


You can restrict proxying to specific origins. Origin should be the host where your requests to Corsa comes from.

::

    % corsa --allow-proxy http://httpbin.org --allow-origin http://myexample

    % curl http://localhost:8888/proxy/http://httpbin.org/get -H 'Origin: http://myexample' -D -
    HTTP/1.1 200 OK
    Access-Control-Allow-Origin: http://myexample
    [...]

    % curl http://localhost:8888/proxy/http://httpbin.org/get -H 'Origin: http://otherdomain' -D -
    HTTP/1.1 403 Forbidden
    [...]



You can also host a static web app with Corsa::

    % mkdir app
    % echo 'hello' >> app/index.html
    % corsa --app-dir app

    % curl http://localhost:8888/app/index.html -D -
    HTTP/1.1 200 OK
    Content-Length: 6
    [...]
    Content-Type: text/html

    hello

``--allow-origin`` defaults to ``SELF`` which is an alias for the URL of the Corsa server. This way your web app is able to make requests to all ``--allow-proxy`` hosts by default.

You can permit all origins and proxy hosts with the ``ALL`` alias::

    % corsa --allow-proxy ALL --allow-origin ALL

    % curl http://localhost:8888/proxy/https://github.com/ -D -
    HTTP/1.1 200 OK
    [...]


Corsa listens to http://localhost:8888 by default, but you can change that with the ``--bind`` option::

        % corsa --bind :9999
        % corsa --bind 0.0.0.0
        % corsa --bind 0.0.0.0:9090


Installation
------------

Corsa is written in Python and requires `Tornado <http://www.tornadoweb.org/>`_.
It was tested with Python 2.7/3.3 and Tornado 3.1.

Corsa is `hosted on pypi <http://pypi.python.org/pypi/corsa>`_ so you can install it with::

    pip install corsa

