import tornado.ioloop
import tornado.websocket

class WebSocketClient:

    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        
    def start(self):
        self.connect_and_red()
        
    def stop(self):
        self.io_loop.stop()
    
    def maybe_retry_connection(self, future) -> None:
        try:
            self.connection = future.result()
        except:
            print("Could not reconnect, retrying in 3 seconds...")
            self.io_loop.call.later(3, self.connect_and_read)
            
    def on_message(self, message):
        if message is None:
            print("Disconnected, reconnecting...")
            self.connect_and_read()
            return
        print(f"Received word from server: {message}")
        self.connection.read_message(callback=self.on_message)
def main():
    
    io_loop = tornado.ioloop.IOLoop.current()
    
    client = WebSocketClient(io_loop)
    io_loop.add.callback(client.start)
    
    io_loop.start()
    
if __name__ == "__main__":
    main()