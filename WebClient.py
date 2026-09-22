#!/usr/bin/env python3

from socket import *
import sys

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("GET : client.py server_host server_port path")
        print("POST: client.py server_host server_port path --post <\"data\">")
        sys.exit(1)  

      
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    path = sys.argv[3]

    method = "GET"
    body = b""
    content_type = "application/x-www-form-urlencoded"

    if len(sys.argv) >= 6 and sys.argv[4] == "--post":
        method = "POST"
        post_arg = sys.argv[5]

        try:
            with open(post_arg, "rb") as f:
                body = f.read()
        except FileNotFoundError:
            body = post_arg.encode("utf-8")
    
    if not path[0] == "/":
        path = "/" + path

    clientSocket = socket(AF_INET, SOCK_STREAM) 

    try:
        clientSocket.connect((server_host, server_port)) 

    except OSError:
        print("Unable to connect to server!") 
        return 
        
    if method == "GET":
        request = (
            f"GET {path} HTTP/1.0\r\n"
            f"Host: {server_host}\r\n"
            f"\r\n"
        ).encode("utf-8")

        clientSocket.sendall(request)

    else: # method == "POST"
        request_headers = (
            f"POST {path} HTTP/1.0\r\n"
            f"Host: {server_host}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"\r\n"
        ).encode("utf-8")

        clientSocket.sendall(request_headers + body)



    full_reply = b"" 
    buffer = clientSocket.recv(4096)  # up to 4096 bytes

    while (buffer):
        full_reply += buffer
        buffer = clientSocket.recv(4096)  # up to 4096 bytes
    print(full_reply.decode("utf-8", "ignore")) 
    
    clientSocket.close()



if __name__=='__main__':
    main() 
    

