import json
import requests
import time
from datetime import datetime
from flask import Flask, jsonify, request
from pymongo import MongoClient
from static import *
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/index', methods=['GET'])
def get_index():
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    client = MongoClient(MONGO_URI)
    db = client['media-base']
    collection = db['settings'].find_one()
    print(collection['index'])
    return str(collection['index'])


@app.route('/add', methods=['GET'])
def add_to_index():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['media-base']
    db['settings'].find_one_and_update({},{"$inc": {"index": 1}})
    return 'index increased'


@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"message": f"Hello, {name}! Welcome to the API."})


def get_shops_data(link, shop_code, post_codes):
    print(link)
    full_results = []

    for post in post_codes:
        x_flow_index = int(get_index())
        add_to_index()

        x_flow_index = x_flow_index % len(x_flow_array)
        print(x_flow_index, x_flow_array[x_flow_index])
        headers['referer'] = link
        headers['x-flow-id'] = x_flow_array[x_flow_index]

        variables = '{"limit":15,"withDeliveryPromise":false,"zipCodeOrCity":"POST_CODE","productId":"SHOP_CODE","config":{"isEnabled":true,"baseDomain":"https://mediamarkt.pl","channel":"DESKTOP","isLegacyDataExcluded":false,"features":{"badges":{"isFreeShippingBadgeIncluded":false},"crossSalesLine":{"isEnabled":false,"isOutputForced":false},"onlineStatus":{"isParallelRequestsEnabled":true,"isPermanentlyNaIndexEnabled":true},"pickup":{"isStrictPickupDisplayStatusEnabled":true},"price":{"strikePriceTypes":[{"strikePriceType":"lop"},{"strikePriceType":"rrp","shouldBeStruck":false,"showDiscountBadge":false,"isLegalTextInlineAllowed":false}],"isBasePriceRequiredFlagRespected":false,"isDiscountLabelEnabled":true,"isDiscountPercentageShown":true,"isDisplayPriceWithStrikePriceRrpThemed":false,"isLongerStrikePricePrefixAllowed":true,"isPromoPriceFiltered":true,"isPromoPriceUsedAsDisplayPriceInApp":false,"isHistoryChartEnabled":false,"discountPercentageMinimum":5,"discountPercentageMinimumFractionDigits":0},"delivery":{"isDeliveryStatusByEarliestDateEnabled":false,"isLocationSourcingEnabled":true,"isLocationSourcingMarketplaceEnabled":true},"refurbishedGoods":{"isEnabled":true},"repairability":{"isEnabled":false}}}}'
        variables = variables.replace('POST_CODE', post)
        variables = variables.replace('SHOP_CODE', shop_code)
        params = {
            'operationName': 'GetClosestStoresByZipCodeOrCityWithFoundLocation',
            'variables': variables,
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"aed000a926d7a91ed636bfbde453059505a83dc3bc1f54dc7e26f5355a5b6c35"},"pwa":{"captureChannel":"DESKTOP","salesLine":"Media","country":"PL","language":"pl","globalLoyaltyProgram":true,"isOneAccountProgramActive":true,"isUsingXccCustomerComponent":true,"isCheckoutPhoneCompareActive":true}}',
        }
        response = requests.get('https://mediamarkt.pl/api/v1/graphql', params=params, cookies=cookies, headers=headers)
        data = json.loads(response.text)

        data = data['data']['closestStoresWithFoundLocation']['stores']
        result = []
        for item in data:
            shop = {}
            shop['id'] = item['cofrProductAggregate']['cofrPickupFeature']['storeId']
            shop['displayStatus'] = item['cofrProductAggregate']['cofrPickupFeature']['displayStatus']
            shop['pickupStatus'] = item['cofrProductAggregate']['cofrPickupFeature']['pickupStatus']
            fulfillmentTime = item['cofrProductAggregate']['cofrPickupFeature']['fulfillmentTime']
            times = {}
            if fulfillmentTime:
                formatted_date = datetime.fromisoformat(fulfillmentTime['earliest'].replace("Z", "+00:00")).strftime(
                    "%d %b %Y, %H:%M")
                times['earliest'] = formatted_date
                formatted_date = datetime.fromisoformat(fulfillmentTime['latest'].replace("Z", "+00:00")).strftime(
                    "%d %b %Y, %H:%M")
                times['latest'] = formatted_date
                formatted_date = datetime.fromisoformat(fulfillmentTime['validUntil'].replace("Z", "+00:00")).strftime(
                    "%d %b %Y, %H:%M")
                times['validUntil'] = formatted_date
                shop['fulfillmentTime'] = times
            address = f"{item['address']['city']} {item['address']['street']} {item['address']['zipCode']}"
            shop['address'] = address
            result.append(shop)

        print(result)
        full_results.append(result)
        time.sleep(1)
    return jsonify(full_results)


@app.route('/mediamarkt/stacjo', methods=['POST'])
def get_stacjo():
    data = request.get_json()
    link = data.get('link', 0)
    shop_code = data.get('shop_code', 0)
    post_codes = data.get("post_codes", 0)
    stationary_data = get_shops_data(link, shop_code, post_codes)
    return stationary_data

if __name__ == '__main__':
    app.run(debug=True)