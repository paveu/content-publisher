# import json
# import requests
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer 3e5cac39-7e38-4139-8fd6-30adc06a61bd',
# }

# data = {
#     "notifyUrl": "https://your.eshop.com/notify",
#     "customerIp": "127.0.0.1",
#     "merchantPosId": "145227",
#     "description": "RTV market",
#     "currencyCode": "PLN",
#     "totalAmount": "21000",
#     "products": [
#         {
#             "name": "Wireless Mouse for Laptop",
#             "unitPrice": "15000",
#             "quantity": "1"
#         },
#         {
#              "name": "HDMI cable",
#              "unitPrice": "6000",
#              "quantity": "1"
#         }
#     ]
# }

# resp = requests.post('https://secure.payu.com/api/v2_1/orders', headers=headers, json=data, allow_redirects=False)
# jsonOut = resp.json()
# print(jsonOut)
# # {u'orderId': u'GW133GJL5H160429GUEST000P01', u'status': {u'statusCode': u'SUCCESS'}, u'redirectUri': u'https://secure.payu.com/pl/standard/co/summary?sessionId=pnVk4Im7esr7P482LcH9029iQL50flvx&merchantPosId=145227&timeStamp=1461957143749&showLoginDialog=false&apiToken=9801cba94b7e3af2906f38bdb8859b8054a76750bacab29f33300c006ecb3130'} 
# print(jsonOut['status'])

# jsonOutput = resp.json())
# print(jsonOutput.loads())

PAYU_VALIDITY_TIME = ''
