import asyncio
import struct
import time
import socket
import os

ICMP_ECHO = 8

def checksum(data):
    s = 0
    for i in range(0, len(data), 2):
        w = data[i] + (data[i+1] << 8 if i+1 < len(data) else 0)
        s += w
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    return ~s & 0xffff

async def ping(host, count=4, timeout=1):
    try:
        dest = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"{host} not found")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.setblocking(False)

    for seq in range(count):
        header = struct.pack('bbHHh', ICMP_ECHO, 0, 0, os.getpid() & 0xFFFF, seq)
        payload = struct.pack('d', time.time())
        chksum = checksum(header + payload)
        header = struct.pack('bbHHh', ICMP_ECHO, 0, socket.htons(chksum), os.getpid() & 0xFFFF, seq)
        packet = header + payload

        await asyncio.get_event_loop().sock_sendall(sock, packet)
        start = time.time()

        while True:
            try:
                data, addr = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(sock, 1024), timeout)
                icmp_header = data[20:28]
                type, code, csum, pid, sequence = struct.unpack('bbHHh', icmp_header)
                if pid == (os.getpid() & 0xFFFF) and sequence == seq:
                    sent_time = struct.unpack('d', data[28:28+8])[0]
                    rtt = (time.time() - sent_time) * 1000
                    print(f"{host} reply: seq={seq} rtt={rtt:.2f} ms")
                    break
            except asyncio.TimeoutError:
                print(f"{host} request timed out")
                break
        await asyncio.sleep(0.2)
    sock.close()

async def main():
    hosts = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
    await asyncio.gather(*(ping(h) for h in hosts))

if __name__ == "__main__":
    asyncio.run(main())
