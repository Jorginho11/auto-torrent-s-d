from transmissionrpc import Client
from transmissionrpc.error import TransmissionError
import os

class transmission_client:

    def __init__(self,host,port,username,password):
        self.client = Client(host, port=port, user=username, password=password)
        self.torrent = os.path.join(os.path.expanduser('~'), 'Downloads', 'E5340FB5C061E4E53618F41B48D7E1CEA445BB02.torrent')
        print(self.torrent)

    def download(self):
        try:
            self.client.add_torrent(self.torrent, download_dir='/home/goku/Documents')
            print('Add torrent into the download queue, the file will be saved at ')
        except ImportError:
            pass

