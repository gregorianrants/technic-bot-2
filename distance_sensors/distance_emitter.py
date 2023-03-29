import asyncio
import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()

from event_emitter_asyncio.EventEmitter import EventEmitter


class DistanceClient(EventEmitter):
    def __init__(self):
        super().__init__()
        self.sock = ctx.socket(zmq.SUB)
        self.sock.connect("ipc://distance")
        self.sock.setsockopt(zmq.SUBSCRIBE,"".encode('utf-8'))

    async def start(self):
        while True:
          msg = await self.sock.recv_pyobj()
          self.emit(msg['sensor'],msg['value'])
        

distance_emitter = DistanceClient()



