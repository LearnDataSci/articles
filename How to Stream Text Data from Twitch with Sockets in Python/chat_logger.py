import socket
import logging
from emoji import demojize

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])


"""
Get token here: https://twitchapps.com/tmi/
"""

server = 'irc.chat.twitch.tv'
port = 6667
nickname = '<YOUR_USERNAME>'
token = '<YOUR_TOKEN>'
channel = '<CHANNEL>'


def main():
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                logging.info(demojize(resp))

    except KeyboardInterrupt:
        sock.close()
        exit()

if __name__ == '__main__':
    main()
