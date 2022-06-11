from websocket import create_connection
import simplejson as json
from secret import Secret


class Stream_Data:

    def __init__(self) -> None:
        self.url = 'wss://stream.data.alpaca.markets/v1beta1/crypto?exchanges=CBSE'

    def bar_data(self):
        
    
        ws = create_connection(self.url)
        # print(json.loads(ws.recv())) # print the connection message

        auth_message = {"action":"auth","key": Secret.paper_api_key, "secret": Secret.paper_secret_key}
        ws.send(json.dumps(auth_message))


        subscription = {"action":"subscribe","bars":["ETHUSD"]}
        ws.send(json.dumps(subscription))
        # print(json.loads(ws.recv())) # print the authentication message

        while True:
            data = json.loads(ws.recv())

            # return a generator that we will loop through
            yield data[0]
            # print(data)

    