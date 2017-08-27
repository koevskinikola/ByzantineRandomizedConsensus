from base.broadcast import Broadcast
import json, threading, socket


class BestEffortBroadcast(Broadcast):

    SERVER_QUEUE = 10

    def __init__(self, host_port, peer_list):
        super().__init__(peer_list)
        self.port = host_port

    def _broadcast_listener(self):
        """
        A TCP socket server for listening to incomming messages

        :return:
        """

        server_listening = True

        host = socket.gethostname()
        broadcast_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast_server.bind(host, self.port)
        broadcast_server.listen(self.SERVER_QUEUE)

        # do accepts in separate thread
        while server_listening:
            client, address = broadcast_server.accept()
            message = client.recv(Broadcast.BUFFER_SIZE)
            if not message:
                print("Message was empty")
            dict_msg = json.loads(message)

            # for local testing
            peer_address = address[0] + ":" + address[1]
            # for general use
            # peer_address = address[0]

    def broadcast_listener(self):
        threading.Thread(target=self._broadcast_listener).start()

    def deliver(self, sender, message):
        pass