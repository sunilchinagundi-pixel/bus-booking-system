import urllib.request, json
url = 'http://localhost:8001/api/buses/search'
data = json.dumps({
    'source': 'Bangalore',
    'destination': 'Bijapur',
    'travel_date': '2026-04-21T00:00:00',
    'limit': 50
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    print(resp.status)
    print(resp.read().decode('utf-8'))
