from parserCarPlatform.dromClass import dromClass


objectPlatform = {
    "drom" : dromClass()
}

proxies = {
    "http" : '51.79.249.253:8080',
    "socks4" : "101.51.121.35:4153",
    "socks5" : "98.162.96.52:4145"
}

headerUserAgent = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0', 'accept' : '*/*'
}