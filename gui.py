import cv2
import msgpack
import zmq

cv2.namedWindow('left')
cv2.namedWindow('right')
context = zmq.Context()

print('Connecting to flight...')
socket = context.socket(zmq.REQ)
socket.connect('tcp://10.0.2.142:5555')

for request in range(1000):
    if request % 2 == 0:
        camera = 'left'
    else:
        camera = 'right'

    print('Sending request {} ...'.format(request))
    socket.send(b'snap')
    message = socket.recv()
    (width, height, image) = msgpack.unpackb(message, use_list=False)
    print('Received reply {} {}x{} {} {}'.format(
            request, width, height, len(image), type(image)))

    with open('/tmp/test.jpg', 'wb') as f:
        f.write(bytearray(image))

    mat = cv2.imread('/tmp/test.jpg')
    thumbnail = cv2.resize(mat, (0,0), fx=0.15, fy=0.15)
    cv2.imshow(camera, thumbnail)

    ch = cv2.waitKey(30)
    if ch == 0x1b:
        cv2.destroyWindow('left')
        cv2.destroyWindow('right')
        sys.exit(0)
