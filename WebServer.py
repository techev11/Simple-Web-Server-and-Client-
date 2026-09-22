#import socket module
from socket import *
from threading import *
import sys # In order to terminate the program
import os
import subprocess
from urllib.parse import unquote

def safePath(filePath):
    WEB_ROOT = os.path.abspath(".")

    if not filePath or not filePath.startswith("/"):
        return None
    
    #print(filePath)
    filePath = filePath.split("?", 1)[0].split("#", 1)[0]
    #print(filePath)
    filePath = unquote(filePath)
    #print(filePath)
    relativePath = filePath.lstrip("/")

    if relativePath == "":
        return ""

    candidate = os.path.abspath(os.path.normpath(os.path.join(WEB_ROOT, relativePath)))
    #print(WEB_ROOT)
    #print(candidate)
    if os.path.commonpath([WEB_ROOT, candidate]) != WEB_ROOT:
        return None

    return candidate


def processConnection(connectionSocket, ip, client_port):
    try: 
        message = "" #Fill in start 

        while "\r\n\r\n" not in message:
            chunk = connectionSocket.recv(1024).decode()
            if not chunk:
                break   
            message += chunk

        lines = message.splitlines()
        if not lines:
            connectionSocket.send(b"HTTP/1.0 400 Bad Request\r\n\r\n")
            return
        request_line = lines[0]
        parts = request_line.split()

        if len(parts) < 2:
            connectionSocket.send(b"HTTP/1.0 400 Bad Request\r\n\r\n")
            return

        method = parts[0]
        filename = parts[1]

        # Only allow GET and POST (reject everything else)
        if method not in ("GET", "POST"):
            connectionSocket.send(b"HTTP/1.0 405 Method Not Allowed\r\n\r\n")
            return

        #Fill in end

        safeFile = safePath(filename)

        if safeFile is None:
            connectionSocket.send("HTTP/1.0 403 Forbidden\r\n\r\n".encode())
            return

        if method == "GET":
            try:
                f = open(safeFile)
                outputdata = f.read() #Fill in start #Fill in end
                f.close()
            

                #Send one HTTP header line into socket
                #Fill in start
                connectionSocket.sendall(
                    b"HTTP/1.0 200 OK\r\n"
                    b"Content-Length: " + str(len(outputdata)).encode() + b"\r\n"
                    b"\r\n" 
                )
                #Fill in end
                #Send the content of the requested file to the client

                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())


            except IOError:
                #Send response message for file not found
                #Fill in start 
                connectionSocket.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
                #Fill in end
                #Close client socket
        
        else: # method == "POST"
            headers_part, _, body_part = message.partition("\r\n\r\n")

            content_length = 0
            for line in headers_part.split("\r\n")[1:]:
                if line.lower().startswith("content-length:"):
                    try:
                        content_length = int(line.split(":", 1)[1].strip())
                    except ValueError:
                        content_length = 0

            # body_part might already contain some/all of the POST body
            body_bytes = body_part.encode("utf-8", "ignore")

            # Read remaining bytes if needed
            while len(body_bytes) < content_length:
                more = connectionSocket.recv(1024)
                if not more:
                    break
                body_bytes += more

            try:
                if (not os.path.isfile(safeFile)):
                    connectionSocket.send(b"HTTP/1.0 404 Not Found\r\n\r\n")
                    return

                if (not os.access(safeFile, os.X_OK)):
                    connectionSocket.send(b"HTTP/1.0 403 Forbidden\r\n\r\n")
                    return
                
                proc = subprocess.Popen(
                    [safeFile],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                stdout_data, stderr_data = proc.communicate(input=body_bytes)

                if proc.returncode != 0:
                    print("Script error:", stderr_data.decode())
                    connectionSocket.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
                    return

                response_body = stdout_data

                headers = (
                    b"HTTP/1.0 200 OK\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Content-Length: " + str(len(response_body)).encode() + b"\r\n"
                    b"Connection: close\r\n"
                    b"\r\n"
                )

                connectionSocket.sendall(headers + response_body)

            except Exception:
                connectionSocket.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
                return


    except IOError:
        #Send response message for file not found
        #Fill in start 
        connectionSocket.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
        #Fill in end
        #Close client socket
    #Fill in start
    finally:
        print(f"Connection from {ip}:{client_port} ended.")
        connectionSocket.close()
    #Fill in end


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a sever socket
    #Fill in start
    port = 6789
    try:
        serverSocket.bind(('', port))
        serverSocket.listen(10)
    except OSError:
        print(f"Sorry, I could not bind on port {port}")

    print(f"Listening on {port}")

    #Fill in end
    while True:
        #Establish the connection
        print('Ready to serve...')
        (connectionSocket, (ip, client_port)) = serverSocket.accept() #Fill in start #Fill in end
        print(f"Got a connection from {ip}:{client_port}")
        t = Thread(target=processConnection, args=(connectionSocket, ip, client_port), daemon=True)
        t.start()
        
    serverSocket.close()
    sys.exit()#Terminate the program after sending the corresponding data 

if __name__ == "__main__":
    main()