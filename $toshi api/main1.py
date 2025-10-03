from fastapi import FastAPI
import requests 
app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "Welcome to the $Toshi API!"}

@app.get("/toshi-price")
def get_toshi_price():
    # Step 4a: fetch USD price
    url_price = "https://api.coingecko.com/api/v3/simple/price"
    params_price = {"ids": "toshi", "vs_currencies": "usd"}
    response_price = requests.get(url_price, params=params_price)
    data_price = response_price.json()
    price_usd = data_price.get("toshi", {}).get("usd", None)

    # Step 4b: fetch USD→JPY exchange rate
    url_fx = "https://api.exchangerate.host/latest?base=USD&symbols=JPY"
    response_fx = requests.get(url_fx)
    rate_jpy = response_fx.json()['rates']['JPY']

    # Step 4c: calculate JPY price
    price_jpy = price_usd * rate_jpy if price_usd is not None else None

    # Step 4d: return JSON
    return {"usd": price_usd, "jpy": price_jpy}
