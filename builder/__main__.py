"""Site commands.

uv run builder build [--drafts]       assemble the site into dist/
uv run builder check                  sanity-check dist/ (sitemap, robots, links)
uv run builder serve [--drafts] [--port N]
                                      build, then serve dist/ locally
uv run builder perf ...               Lighthouse budgets against dist/
uv run builder submit-sitemap ...     resubmit the sitemap to Google
uv run builder indexnow ...           ping IndexNow about changed pages
"""
import functools
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def serve(args: list[str]) -> int:
    from .build import build
    from .paths import DIST
    port = int(args[args.index('--port') + 1]) if '--port' in args else 8000
    build(drafts='--drafts' in args)
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(DIST))
    print(f'Serving dist/ at http://localhost:{port}/')
    ThreadingHTTPServer(('localhost', port), handler).serve_forever()
    return 0


def main() -> int:
    command, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ('', [])
    if command == 'build':
        from .build import build
        build(drafts='--drafts' in args)
        return 0
    if command == 'serve':
        return serve(args)
    modules = {'check': 'check_site', 'perf': 'perf_check',
               'submit-sitemap': 'submit_sitemap', 'indexnow': 'indexnow'}
    if command not in modules:
        print(__doc__)
        return 2
    # These modules read their own options from sys.argv.
    sys.argv = [f'builder {command}', *args]
    module = __import__(f'builder.{modules[command]}', fromlist=['main'])
    return module.main() or 0


if __name__ == '__main__':
    raise SystemExit(main())
