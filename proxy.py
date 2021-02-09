#!/usr/bin/python3

# version 1.0.0
# Python proxy with socket module
# Project: Increment data storage with SQL and data analysis.
# browsing time by link/url, blacklist, time counter, setc...

import socket,threading,sys

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != None:
            ip = str(sys.argv[1])
        else:
            ip= '127.0.0.1'
        if sys.argv[2] != None:
            port = int(sys.argv[2])
        else:
            port = 8080
    else:
        ip = '127.0.0.1'
        port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen()

    while True:
        (sSocket, sAddr) = s.accept()
        sData = sSocket.recv(8196)
        t = threading.Thread(target = data_treat, args=(sSocket,sData,sAddr))
        t.start()

    s.close()

def data_treat(sSocket,sData, sAddr):
    try:
        url = sData.split(b" ")[1]
    except Exception:
        return()

    if len(url) < 3:
        print("[-] Url not found")
        return()

    if url.find(b"://") <= 0:
        spUrl = url
    else:
        spUrl = url[(url.find(b"://")+3):]

    portdot = spUrl.find(b":")
    print(spUrl)

    point = spUrl.find(b"/")
    if point == -1:
        point = len(spUrl)
    if portdot == -1:
        port = 80
        proxyUrl = spUrl[:spUrl.find(b"/")]
    else: 
        port = int( (spUrl[(portdot+1):][:point]) )
        proxyUrl = spUrl[:portdot]

    if port == 443:
        print("443 port")
        return()

    print("[+] ",proxyUrl.decode('utf-8'))
    send_proxy(proxyUrl, port, sSocket, sData)

def send_proxy(ip, port, connection, sData):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    s.connect((ip, port))

    s.send(sData)
    while True:
        try:
            reply = s.recv(4098)
        except:

            break

        if len(reply) > 0:
            connection.send(reply)

        else:
            break
    s.close() 
    connection.close()

main()