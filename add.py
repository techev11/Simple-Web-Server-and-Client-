#!/usr/bin/env python3
import sys
from urllib.parse import parse_qs

def main():
    # Read the POST body from stdin (your server pipes it in)
    body = sys.stdin.buffer.read().decode("utf-8", "ignore")

    # Parse application/x-www-form-urlencoded (e.g., "a=3&b=7")
    params = parse_qs(body)

    def get_number(key: str) -> float:
        if key not in params or len(params[key]) == 0:
            raise ValueError(f"Missing field: {key}")
        return float(params[key][0])

    try:
        a = get_number("a")
        b = get_number("b")
        result = a + b

        # Print HTML (your server will wrap it in HTTP headers)
        print("<!doctype html>")
        print("<html><body>")
        print(f"<h1>Result</h1>")
        print(f"<p>{a} + {b} = <b>{result}</b></p>")
        print('<p><a href="/form.html">Back</a></p>')
        print("</body></html>")

    except Exception as e:
        # Print a helpful error page
        print("<!doctype html>")
        print("<html><body>")
        print("<h1>Error</h1>")
        print(f"<pre>{e}</pre>")
        print('<p><a href="/form.html">Back</a></p>')
        print("</body></html>")

if __name__ == "__main__":
    main()