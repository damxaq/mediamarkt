import json
import requests
import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    with open("settings.json") as feedsjson:
        feeds = json.load(feedsjson)
    new_feeds = {"index": feeds["index"] + 1}
    with open("settings.json", mode='w') as f:
        f.write(json.dumps(new_feeds, indent=2))
    return jsonify(feeds)

@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"message": f"Hello, {name}! Welcome to the API."})


def get_shops_data(link, shop_code, post_codes):
    print(link)
    x_flow_array = ['83ab02c8-23fc-4b28-b3e4-984e5629d596', '75281cbd-3c4b-4137-9802-0190aa9c4f36',
                    'b871fedb-5802-4511-b4ec-35a6f70ecc78', '2ec80b1f-d494-451f-ad21-a1cbc50bb99f',
                    'e3c932c5-f6ad-4c6c-9de3-1e904d2c6cf8', 'ead66edd-80f7-4adb-9f42-150137fd103b',
                    '09daabab-934a-4d28-9b5f-9b7c24a4f7a1', '4253dd01-ca3a-4d8d-9871-93a680595c20']
    cookies = {
        'optid': '88c6159e-a5d0-4b06-82d3-fd4a4e5aff8b',
        'ea_uuid': '202508251458155701206176',
        '_cs_c': '1',
        '_ga': 'GA1.1.900782610.1781624811',
        '_fbp': 'fb.1.1781624811144.689952777121146447',
        '_fpid': '900782610.1781624811',
        'BVBRANDID': '8bc15deb-3e41-4ee6-baf4-1cba9f25be6d',
        '_gcl_au': '1.1.1412056462.1789473500',
        'FPAU': '1.1.1412056462.1789473500',
        't_fpd': 'true',
        'pwaconsent': 'v:1.1&id:0bea1b16a538a75c552c88ed3ae0d8944221e471&createdMs:1793179406356~required:1&clf:1,cli:1,gfb:1,gtm:1,mms:1,ocx:1|comfort:1&aic:1,aid:1,baz:1,cne:1,con:1,fix:1,gfa:1,goa:1,gom:1,grc:1,ice:1,kod:1,lob:1,loq:1,opt:1,ore:1,pcl:1,sen:1,spe:1,sst:1,sth:1,swo:1,tal:1,usw:1,usz:1,woo:1,yte:1,zwi:1|marketing:1&adj:1,cen:1,clm:1,cri:1,fab:1,fcm:1,gad:1,gam:1,gcl:1,gcm:1,gdv:1,gos:1,gse:1,msb:1,omp:1,ras:1,rtb:1,tkt:1,trd:1,unl:1,wpx:1|',
        'tc_id': '0c31dc74058f0a52cde9e23b77fc9b917ceffc5f',
        '_tt_enable_cookie': '1',
        '_ttp': 'null.tt.1',
        'dtm_token': 'AQALDEOExqLLbAEBAQEAAQBNRgEBAQEBAQEBAQEBAKCA01O-',
        'a': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im8yc2lnbiJ9.eyJzdWIiOiI0ZDYzMzY2Ni1hNjBiLTRhMTgtYWEwYS1hMzYxMGU1OTkxNWIiLCJpc3MiOiJtbXNlIiwiaWF0IjoxNzkzMTkxNDA2LCJleHAiOjE3OTQ0MDEwMDYsImF1ZCI6IndlYm1vYmlsZSIsInQiOiJ1IiwibyI6MTIwN30.GyIbJ-266u96ft--s6e50cJ5qfUmxCix2bRLKGeEYmW9w6nwUqw0Qun1LA5Qfr9OiEQlRmfzP8REtFLHarAsOZxyDJOA54dtHaDlLCBLVEuYJM6hzyCy4FLQU687VK5J_03-y0ugP_0grstR8KyDjak9k1a5wrVFF3IuQnOBSXq-fK46teHR6I41Gp7HbIhA7cx7U_2kZA6a6KyYFuvk87UB0631DiFbnxOdKEI6lORtWMnLf76d7cRqRWfhtOJWe57OGNeyVgSnUNUljuOCdB2Ml8EUpdkNr8CM-JZwdq8iGFJndJwd5zY_yw7DDUWxG14M-bM4iKVwX_ws_g5Giw',
        'cf_clearance': '1xHp6gq2OxPUneavtIWFv4IMBwf_Z3Thuz0nbEI5lwU-1793195656-1.2.1.1-0ElRDmLs6zLlca2It.jOO06520EoyZWC1NW9jDVuG0MAn9p9VftTun4lI7Y9ef7yqGDrxby67ilJHHL8ZrGWbX7047RBWSIvKTCF2eDxbF0XxVbU_LAY6zribh4snZKhZGAagyrjjMRH7kXeU70XxR6h.b07x.8WU6VlZYah5RyIfjgf1IG641EAFd8eoTtF_kdcfpGV9ilsJkJO8v0z94jd2SOzyfdqZIn5F45X2i_4JJm9I2fG60iRTO7Olqe52gM1DaX4y4C55rdWkrXIHQmBCL63AvpdjP2b0DkFYo08G7BpIrgSLQX6n.taJoqMLVjIAjWDfsfitxuYy3JPDU8fDA7mQM63rv4deWPUudc',
        '_uetvid': 'e0e33810ab5111f0acec29d8b21a3fa3',
        'ts_id': '2f388dcf-74d2-4a05-add6-f1ccecb13183',
        '__cf_bm': 'LZSU.rGRMojF4wcq4AskDdx0Nta51cig3go_lPQuyco-1793298467.1396995-1.0.1.1-d6YN4olPDQTGTlJyMlknVjKMFGWOA8qWqKS5Nt6jSVVZ1c0aeJGZhV4kEiNrHgzBslwvnJigWjowxKSlxEsQli2PkKau9tNjHxdjuHA2mLP.Db4Jrat.NVpCaNIQfOBu',
        'lux_uid': '179329846788311163',
        '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22ca816EoKnqibf6mcmwRS%22%2C%22expiryDate%22%3A%222027-10-29T18%3A27%3A50.795Z%22%7D',
        'FPGSID': '1.1793298470.1793298470.G-4JZR222EHK.S_hYVupsYUHRofo1oEB4ew',
        'ttcsid_CGLA2N3C77UFNT4O2L5G': '1793298471824::ZE2x66wzdXiAgXxQ8zwz.5.1793298471837.1',
        'ats_ri': 'ri=202508251458155701206176&model=202508251458155701206176&models=eyJhdHNfcmkiOiIyMDI1MDgyNTE0NTgxNTU3MDEyMDYxNzYiLCJzcmMiOiJndSJ9&ttl_ms=3600000&expires_ms=1793302072136&version=1793298471.68&fs=519c',
        '_cs_id': '056fe0ce-0c54-a437-bc99-a7463e33d252.1781624810.111.1793298476.1793298468.1.1815788810780.1.x',
        '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22expiryDate%22%3A%222027-10-29T18%3A27%3A56.841Z%22%7D',
        '_ga_N6GKZYX63W': 'GS2.1.s1793298469$o28$g0$t1793298476$j53$l0$h0',
        'dtm_token_sc': 'AQAI94dPeRs_rwFLYbJjAQBNRgABAQCggNNTAgEBAKCJ6jCS',
        '_ga_4JZR222EHK': 'GS2.1.s1793298470$o28$g0$t1793298479$j51$l0$h1511214226',
        '_msbps': '99',
        'ttcsid': '1793298485130::Hm-m3DvmzmAU_07-G4qP.6.1793298485130.0',
    }
    full_results = []

    for post in post_codes:
        with open("settings.json") as settings:
            x_flow_index = json.load(settings)
        # new_settings = {"index": x_flow_index["index"] + 1}
        # with open("settings.json", mode='w') as f:
        #     f.write(json.dumps(new_settings, indent=2))

        x_flow_index = x_flow_index["index"] % len(x_flow_array)
        print(x_flow_index, x_flow_array[x_flow_index])
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,pl;q=0.8',
            'apollographql-client-name': 'pwa-client-pqm',
            'apollographql-client-version': '8.522.0',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': link,
            'sec-ch-ua': '"Chromium";v="155", "Not(A:Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"155.0.8059.84"',
            'sec-ch-ua-full-version-list': '"Chromium";v="155.0.8059.84", "Not(A:Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36',
            'x-cacheable': 'true',
            'x-flow-id': x_flow_array[x_flow_index],
            'x-mms-country': 'PL',
            'x-mms-language': 'pl',
            'x-mms-salesline': 'Media',
            'x-operation': 'GetClosestStoresByZipCodeOrCityWithFoundLocation',
        }

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