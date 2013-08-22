from __future__ import print_function

import re
import sys

import tornado.ioloop
import tornado.web
import tornado.log

from corsa.proxy import ProxyHandler


def run_proxy((host, port), app_path=None, debug=False):
    handler = [
        (r'/proxy/(.*)', ProxyHandler),
    ]
    if app_path:
        handler.append(
            (r'/app/(.*)', tornado.web.StaticFileHandler, {'path': app_path})
        )
    app = tornado.web.Application(handler, debug=debug)
    app.listen(port, host)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

def parse_bind_address(address, default=('localhost', 8080)):
    """
    >>> parse_bind_address('80')
    ('localhost', 80)
    >>> parse_bind_address('0.0.0.0')
    ('0.0.0.0', 8080)
    >>> parse_bind_address('0.0.0.0:8081')
    ('0.0.0.0', 8081)
    """
    if ':' in address:
        host, port = address.split(':', 1)
        port = int(port)
    elif re.match('^\d+$', address):
        host = default[0]
        port = int(address)
    else:
        host = address
        port = default[1]
    return host, port


def main():
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('--app-dir')
    parser.add_option('-b', '--bind', default='localhost:8888')
    parser.add_option('--debug', default=False, action='store_true')

    options, args = parser.parse_args()

    host, port = parse_bind_address(options.bind)

    tornado.log.enable_pretty_logging()

    print("Starting Corsa...", file=sys.stderr)
    print("  CORS proxy at http://%s:%d/proxy/" % (host, port), file=sys.stderr)

    if options.app_dir:
        print("  Hosting %s at http://%s:%d/app/" % (options.app_dir, host, port),
            file=sys.stderr)

    try:
        run_proxy((host, port), options.app_dir, debug=options.debug)
    except KeyboardInterrupt:
        print("Exiting", file=sys.stderr)


if __name__ == '__main__':
    main()