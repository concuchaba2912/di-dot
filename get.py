import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

# URL của API
url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

def fetch_proxies(api_url):
    """Lấy danh sách proxy từ API."""
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            print(f"Fetched {len(proxies)} proxies.")
            return proxies
        else:
            print(f"Failed to fetch proxies. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def is_proxy_alive(proxy):
    """Kiểm tra proxy có hoạt động hay không."""
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        # Gửi yêu cầu thử nghiệm qua proxy
        response = requests.get("http://www.google.com", proxies=proxies, timeout=25)
        return True  # Proxy hoạt động
    except Exception:
        return False  # Proxy không hoạt động

def check_proxies_concurrently(proxies, max_workers=5100):
    """Kiểm tra danh sách proxy đồng thời."""
    alive_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Kiểm tra proxy song song
        results = executor.map(lambda proxy: (proxy, is_proxy_alive(proxy)), proxies)
        for proxy, alive in results:
            if alive:
                print(f"{Fore.GREEN}Proxy {proxy} is alive.{Style.RESET_ALL}")
                alive_proxies.append(proxy)
            else:
                print(f"{Fore.RED}Proxy {proxy} is dead.{Style.RESET_ALL}")
    return alive_proxies

# Lấy danh sách proxy từ API
proxy_list = fetch_proxies(url)

# Kiểm tra proxy đồng thời
alive_proxies = check_proxies_concurrently(proxy_list)

# Lưu các proxy hoạt động vào file
with open("proxies_alive.txt", "w") as file:
    file.write("\n".join(alive_proxies))
    print(f"Saved {len(alive_proxies)} working proxies to proxies_alive.txt.")
