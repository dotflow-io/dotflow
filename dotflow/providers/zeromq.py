# """ZeroMQ module"""

# import asyncio

# from typing import Callable

# from zmq import Context as ContextClient, PUSH, PULL, POLLIN  # type: ignore
# from zmq.asyncio import Context as ContextServer, Poller  # type: ignore

# from dotflow.abc.tcp import TCPClient, TCPServer


# class ZeroMQClient(TCPClient):

#     def __init__(self, url: str):
#         self.url = url
#         self.context = ContextClient.instance()

#     def sender(self, content: dict) -> None:
#         push = self.context.socket(PUSH)
#         push.bind(self.url)
#         push.send_json(content)


# class ZeroMQServer(TCPServer):

#     def __init__(self, url: str, handler: Callable):
#         self.url = url
#         self.handler = handler
#         self.context = ContextServer.instance()

#     async def receiver(self) -> None:
#         pull = self.context.socket(PULL)
#         pull.connect(self.url)

#         poller = Poller()
#         poller.register(pull, POLLIN)

#         while True:
#             events = await poller.poll()

#             if pull in dict(events):
#                 content = await pull.recv_json()
#                 self.handler(content, content=content)

#     async def run(self) -> None:
#         await asyncio.wait(
#             [asyncio.create_task(self.receiver())]
#         )
