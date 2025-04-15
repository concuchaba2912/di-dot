import aiohttp
import asyncio
from aiohttp import ClientTimeout

# Danh sách các nguồn proxy
PROXY_SOURCES = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxyscan.io/download?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
]

# File lưu proxy
OUTPUT_FILE = "proxy.txt"

# URL kiểm tra proxy hoạt động
TEST_URL = "http://httpbin.org/ip"

# Timeout cho mỗi request
TIMEOUT = 5


async def fetch_proxies(source_url):
    """Lấy proxy từ nguồn"""
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10)) as session:
            async with session.get(source_url) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        print(f"Không thể lấy proxy từ {source_url}: {e}")
    return ""


async def check_proxy(proxy):
    """Kiểm tra proxy còn sống"""
    proxies = f"http://{proxy}"
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=TIMEOUT)) as session:
            async with session.get(TEST_URL, proxy=proxies) as response:
                if response.status == 200:
                    print(f"Proxy sống: {proxy}")
                    return proxy
    except:
        pass
    return None


async def main():
    # Lấy proxy từ các nguồn
    print("Đang lấy proxy từ các nguồn...")
    all_proxies = []
    tasks = [fetch_proxies(source) for source in PROXY_SOURCES]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_proxies.extend(result.splitlines())

    print(f"Lấy được tổng cộng {len(all_proxies)} proxy từ các nguồn.")

    # Kiểm tra proxy còn sống
    print("Đang kiểm tra proxy...")
    tasks = [check_proxy(proxy) for proxy in all_proxies]
    alive_proxies = await asyncio.gather(*tasks)
    alive_proxies = [proxy for proxy in alive_proxies if proxy]

    print(f"Có {len(alive_proxies)} proxy hoạt động.")

    # Lưu proxy hoạt động vào file
    with open(OUTPUT_FILE, "w") as file:
        for proxy in alive_proxies:
            file.write(proxy + "\n")
    print(f"Proxy đã được lưu vào file {OUTPUT_FILE}.")


if __name__ == "__main__":
    asyncio.run(main())
