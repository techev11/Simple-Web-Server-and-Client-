# Simple Python Web Server and Client

A lightweight HTTP web server and client implemented in Python using TCP sockets.

The project demonstrates the fundamentals of HTTP communication, socket programming, multithreading, file serving, and basic server-side script execution without relying on a web framework.

## Features

### Web Server

The server:

* Uses TCP sockets to listen for incoming HTTP connections.
* Listens on port `6789`.
* Supports `GET` and `POST` requests.
* Handles multiple clients concurrently using Python threads.
* Serves files from the server's current working directory.
* Returns standard HTTP status codes such as:

  * `200 OK`
  * `400 Bad Request`
  * `403 Forbidden`
  * `404 Not Found`
  * `405 Method Not Allowed`
  * `500 Internal Server Error`
* Protects against directory traversal using path validation.
* Decodes URL-encoded paths.
* Executes executable files for `POST` requests.
* Passes the POST request body to the executable through standard input.
* Returns the executable's standard output to the client.

### HTTP Client

The client:

* Connects to a specified server and port using TCP.
* Supports both `GET` and `POST`.
* Constructs HTTP/1.0 requests manually.
* Accepts POST data either directly from the command line or from a file.
* Reads the complete HTTP response from the server.
* Displays the server response in the terminal.

## Requirements

* Python 3
* No external Python packages are required.

The project uses only Python standard-library modules, including:

```text
socket
threading
sys
os
subprocess
urllib.parse
```

## Project Structure

```text
project/
├── server.py
├── client.py
├── index.html
└── ...
```

`server.py` contains the multithreaded HTTP server, while `client.py` provides a command-line HTTP client.

Files that should be accessible through GET requests can be placed in the directory where the server is started.

## Running the Server

Start the server with:

```bash
python3 server.py
```

The server listens on port `6789`:

```text
Listening on 6789
Ready to serve...
```

When a client connects, the server prints the client's IP address and port.

## Using the Client

The general client syntax is:

```bash
python3 client.py <server_host> <server_port> <path>
```

### GET Request

To request a file from a server running locally:

```bash
python3 client.py localhost 6789 /index.html
```

The client generates a request similar to:

```http
GET /index.html HTTP/1.0
Host: localhost
```

If the file exists, the server responds with `200 OK` and the contents of the file.

Example:

```text
HTTP/1.0 200 OK
Content-Length: 125

<html>
...
</html>
```

### POST Request

POST requests use the `--post` option:

```bash
python3 client.py localhost 6789 /script.py --post "name=John&message=Hello"
```

The client sends an HTTP request containing:

```http
POST /script.py HTTP/1.0
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
```

The request body is passed to the executable file through standard input.

POST data can also be loaded from a file:

```bash
python3 client.py localhost 6789 /script.py --post data.txt
```

If the argument after `--post` is an existing file, the client reads its contents and uses them as the POST body. Otherwise, the argument itself is used as the request body.

## POST Script Execution

For a POST request, the requested path must point to an existing executable file.

For example:

```bash
chmod +x script.py
```

A simple executable Python script could look like:

```python
#!/usr/bin/env python3

import sys

data = sys.stdin.read()

print("<html>")
print("<body>")
print("<h1>POST Request Received</h1>")
print(f"<p>{data}</p>")
print("</body>")
print("</html>")
```

The server executes the program and sends its standard output back as the HTTP response body.

If the requested file does not exist, the server returns:

```text
HTTP/1.0 404 Not Found
```

If the file exists but is not executable, the server returns:

```text
HTTP/1.0 403 Forbidden
```

If the executable terminates with an error, the server returns:

```text
HTTP/1.0 500 Internal Server Error
```

## Path Security

The server validates requested paths before accessing files.

The `safePath()` function:

1. Removes query strings and URL fragments.
2. Decodes URL-encoded characters.
3. Converts the requested path into an absolute filesystem path.
4. Normalizes the path.
5. Verifies that the resulting path remains inside the server's web root.

This prevents requests such as:

```text
/../../../etc/passwd
```

from escaping the server's working directory.

Invalid paths receive:

```text
HTTP/1.0 403 Forbidden
```

## Multithreading

Each incoming connection is handled in a separate thread:

```python
t = Thread(
    target=processConnection,
    args=(connectionSocket, ip, client_port),
    daemon=True
)
t.start()
```

This allows the server to process multiple client connections concurrently rather than waiting for one request to finish before accepting another.

## How It Works

The basic communication flow is:

```text
Client
   |
   |  TCP Connection
   v
Server
   |
   |  Accept Connection
   v
New Thread
   |
   |  Read HTTP Request
   v
Parse Method + Path
   |
   +-------- GET --------> Read File
   |                         |
   |                         v
   |                     HTTP Response
   |
   +-------- POST -------> Execute File
                             |
                             v
                       Pass POST Body
                         through stdin
                             |
                             v
                       Capture stdout
                             |
                             v
                        HTTP Response
```

For a GET request, the server reads the requested file and returns its contents. For a POST request, the server executes the requested program, passes the request body through `stdin`, captures the program's `stdout`, and sends that output back to the client.

## Purpose

This project is intended as a learning exercise for understanding:

* TCP socket programming
* Client-server architecture
* HTTP request and response formatting
* HTTP GET and POST methods
* Multithreaded servers
* File handling
* URL and filesystem path validation
* Process execution and standard input/output
* Basic web-server security concepts

Rather than using a framework such as Flask or Django, the HTTP communication is implemented directly on top of Python sockets to demonstrate what happens at a lower level.

## Limitations

This is a simple educational web server and is not intended for production use. It implements only a small subset of HTTP functionality and does not include features expected from production web servers, such as HTTPS, comprehensive HTTP parsing, MIME-type detection, persistent connections, authentication, or advanced request validation.
