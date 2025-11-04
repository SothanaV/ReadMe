import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_addr(i):
    addr = f'192.168.28.{i}'
    try:
        r = requests.get(f'http://{addr}/cgi-bin/luci/web', timeout=3)
        is_mi = 'MiWiFi' in r.text
        return True, f"{addr} is Mi {is_mi}"
    except Exception:
        return False, f"{addr} unreachable"

def main():
    reachables = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(check_addr, i) for i in range(1, 255)]
        for future in as_completed(futures):
            reachable, text = future.result()
            print(text)
            if reachable:
                reachables.append(text)
    print(f"reachables : {reachables}")
if __name__ == "__main__":
    main()