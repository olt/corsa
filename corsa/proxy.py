import urlparse

import tornado.httpclient
import tornado.web

# headers to remove as of HTTP 1.1 RFC2616
# http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html
hop_by_hop_headers = set([
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade',
])

class ProxyHandler(tornado.web.RequestHandler):
    def response_handler(self, response):
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            self.set_status(500)
            self.write('Internal server error:\n' + str(response.error))
            self.finish()
            return

        self.set_status(response.code)
        # copy all but hop-by-hop headers
        for header, v in response.headers.iteritems():
            if header.lower() not in hop_by_hop_headers:
                self.set_header(header, v)
        self.set_header(' Access-Control-Allow-Origin', '*')
        if response.body:
            self.write(response.body)
        self.finish()

    @tornado.web.asynchronous
    def request_handler(self, url):
        url_parts = urlparse.urlparse(url)
        self.request.headers['Host'] = url_parts.netloc

        req = tornado.httpclient.HTTPRequest(
            url=url,
            method=self.request.method,
            body=self.request.body,
            headers=self.request.headers,
            follow_redirects=False,
            allow_nonstandard_methods=True,
        )

        client = tornado.httpclient.AsyncHTTPClient()
        try:
            client.fetch(req, self.response_handler)
        except tornado.httpclient.HTTPError as e:
            # pass regular HTTP errors from server to client
            if hasattr(e, 'response') and e.response:
                self.response_handler(e.response)
            else:
                raise

    # alias HTTP methods to generic request handler
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
    get = request_handler
    post = request_handler
    put = request_handler
    delete = request_handler
    head = request_handler
