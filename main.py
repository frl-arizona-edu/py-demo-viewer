import msgpack
import zmq

context = zmq.Context()

print('Connecting to flight...')
socket = context.socket(zmq.REQ)
socket.connect('tcp://10.0.2.142:5555')

for request in range(10):
    print('Sending request {} ...'.format(request))
    socket.send(b'snap')
    message = socket.recv()
    (width, height, image) = msgpack.unpackb(message, use_list=False)
    print('Received reply {} {}x{} {} {}'.format(
            request, width, height, len(image), type(image)))
    with open('/tmp/test{}.jpg'.format(request), 'wb') as f:
        f.write(bytearray(image))
