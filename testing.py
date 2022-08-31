import requests

headers = {
    'authority': 'www.mwave.com.au',
    'method': 'GET',
    'path': '/desktop-computers/mwave-computers',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'SLI4_512033937=1661908965874; SLIBeacon_512033937=1D619C272501496195A85C187734DFD; _gid=GA1.3.806811543.1661908967; ASP.NET_SessionId=fgiovx34gzf2wnurxaexbnaf; __cfruid=caf00089ab96e8af13bb4283a0061ad503e8a111-1661929180; __cf_bm=LainhRUAGeLJe55LBw1c3hjKpWW_cquO_vx.7oJ2iyg-1661931808-0-ATjTgZzsy0zYMlm+59ETzHq9n6j38PQ/H+FI27SK8H2p6lMqfODr8SMN6HA0ngn4uDndSBNQ9kqS0gVvR4rDHQampPMVBNkMA8MBIg8ty7nbyfZkhCIQBbNFVmKYToN8o54Bgi++eambZxnAR4yIeeP1sqgA4I1YUSVkx/Y/Xvb8; _ga_PM4J9J5MCL=GS1.1.1661931809.5.1.1661931869.0.0.0; _ga=GA1.3.1425815938.1661908967; _gat_UA-992540-1=1; High_Sierra=1D619C272501496195A85C187734DFD.1661908965874.7.0; SLI1_512033937=1D619C272501496195A85C187734DFD.1661908965874.7.0; SLI2_512033937=1D619C272501496195A85C187734DFD.1661908965874.7.0; cto_bundle=GNX5gF9uJTJCcVg5ZEhuUHdFSHlaVDNwaVU3dlhMemYzcVZVeFA5R24xRkxXcHh4UFFsWSUyQnAzRkVyNWNpY25Kb2Z0a2dOcHpPTGNpWUl2VCUyRnNwYWVOV2JYamNNWUpuNyUyQnFWYlhsYkZwJTJCWUw1ZWJoSmdZS2dCOFglMkJDNGsxRCUyRldHTlFMR0FIUVRmdU5JMDYwN0wzcVolMkZzQ1VpZllBJTNEJTNE',
    'dnt': '1',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

response = requests.get('https://www.mwave.com.au/desktop-computers/mwave-computers', headers=headers)
print(response)
print(response.headers)