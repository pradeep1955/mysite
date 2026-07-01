import requests

url = "https://pleasurewebsite.com/mystocks/api/predict/"
data = {
    "symbol": "TCS.BO",
    "rsi": 52.4,
    "macd": 1.1,
    "signal": 1.3,
}

response = requests.post(url, json=data)
print(response.json())
