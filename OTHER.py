import requests


token = '6587599071:AAF_Wb0gAO7Zw_pS5hANgUfOBnVAR_mH60A'
method_send = 'sendMessage'
method_updates = 'getUpdates'
tg_api_url = 'https://api.telegram.org/bot{token}/{method}'

response = requests.post(
         url=tg_api_url.format(token=token, method=method_send),
         data={'chat_id': -4077907895, 'text': 'im not skuf'}
     )

# resp = requests.get(url=tg_api_url.format(token=token, method=method_updates))


# print(resp.text)