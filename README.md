## bitget-python-connector-with-heroku
`2022.12 將 tradingview 策略的訊號自動發送至 bitget 交易所`
`2023.04.27 將bitget-python-connector加入`
 
### bitget-python-connector
> 請參考[bitget-python-connector](https://github.com/parker178912/bitget-python-connector)中的 example 選擇自己所需的函數做使用

### requirements
> 使用heroku當作雲端站台時所需要的子項目

### example
> 開平倉程式碼範例

* 於交易所創建api後填入
```
    api_key = ""        # put your api_key
    secret_key = ""     # put your secret_key
    passphrase = ""     # put your passphrase
```
### tradingview_msg_example
在tradingview alert中訊息欄所放置之訊息，可藉由快訊提取自己所需的部分在程式中使用

![image](https://user-images.githubusercontent.com/87221772/234738295-507d31e7-6455-47ea-af0d-04b0fa376892.png)

打開 webhook 並填入 heroku 主機 url

![image](https://user-images.githubusercontent.com/87221772/234738448-f5bd5626-08f4-4712-8bd5-c54eebe6c7f0.png)

### 運行
1. 在 command 中輸入 flask run 以在本地端進行測試
2. 測試訊息可使用 tradingview alert 傳出之訊息
3. 使用 insomnia 將訊號 post 至本地端 http://localhost:5000/normal
4. 確認沒問題即可將程式推上[雲端主機](https://dashboard.heroku.com/apps)進行運行
5. 將主機之 url 放至策略 webhook url
