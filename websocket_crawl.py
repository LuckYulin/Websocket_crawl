# -*- coding: utf-8 -*-
from websocket import WebSocketApp, enableTrace
import ssl
import json
import time
from threading import Thread


class WskData():    # 类中的使用静态方法，否则会报缺失位置参数
    @staticmethod
    def on_message(ws, message):        # message 是收到的信息
        msg = json.loads(message)
        print(msg)
        return msg

    @staticmethod
    def on_error(ws, error):
        print('error', error)

    @staticmethod
    def on_close(ws):
        print("closed...")

    @staticmethod
    def on_open(ws):
        def run(*args):
            while True:
                msg = json.dumps({"type": "detail", "room_id": "B3533162", "is_pc": "1"})
                ws.send(msg)
                time.sleep(2)

        Thread(target=run, name='run', args=()).start()       # 新开一个线程，启动run函数,给网站发送msg，保持信息推送回来。

    def crawl_start(self, url, ws_headers):
        enableTrace(False)          # 参数是True时，会显示发送的msg
        ws = WebSocketApp(url=url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, header=ws_headers)
        ws.on_open = self.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  # 忽略认证


headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
        "Host": "push.tisai.com:37272",
        "Origin": "http://www.10pan.cc",
        "Pragma": "no-cache",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "m0cExR3c60/NSojh1T9EIg==",
        "Sec-WebSocket-Version": "13",
        "Upgrade": "websocket",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}
url = 'wss://push.tisai.com:37272/'
qs = WskData()
qs.crawl_start(url, headers)
