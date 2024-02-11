import socket
import os

class IrisSub:
    def __init__(self, path_to_image_folder='images'):
        self.path_to_image_folder = path_to_image_folder

    def take_picture(self):
        """
        send a request to IRIS to take a picture and save it to the image folder
        """
        if not os.path.exists(self.path_to_image_folder):
            os.mkdirs(self.path_to_image_folder)

    def get_picture(self, picture_name=None):
        """
        get picture_name picture from the image folder, 
        if no name is specified, get the most recent image
        """
        pass

def main():
    """
    this should be named something else later
    Create a TCP server that listens for requests for the IRIS subsystem
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections, look at this later
    server_socket.listen(1)
    print('Server listening on {}:{}'.format(*server_address))

    iris_sub = IrisSub()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('Accepted connection from {}:{}'.format(*client_address))

            request = client_socket.recv(1024).decode('utf-8')
            print('Received request: {}'.format(request))

            response = None
            if request == 'take_picture':
                iris_sub.take_picture()
                response = f'Picture taken and saved to {IrisSub.path_to_image_folder}'
            elif request == 'get_picture':
                iris_sub.get_picture()
                response = f'Picture retrieved from {IrisSub.path_to_image_folder}'
            elif request == 'stop':
                client_socket.close()
                response = 'Closed connection from {}:{}'.format(*client_address)
                break
            else:
                response = 'Invalid request'

            client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(e)
        response = e
        client_socket.sendall(response.encode('utf-8'))
        server_socket.close()
