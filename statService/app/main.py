import asyncio

import grpc

from statService.app.consumer import start_consumer
from statService.app.servicer import StatsServiceServicer
from proto import stat_pb2_grpc


async def serve() -> None:
    server = grpc.aio.server()
    stat_pb2_grpc.add_StatsServiceServicer_to_server(
        StatsServiceServicer(), server
    )
    server.add_insecure_port("[::]:50052")

    start_consumer()

    await server.start()
    print("gRPC StatsService run at 50052 port...")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        print("gRPC StatsService stopped.", flush=True)


if __name__ == "__main__":
    asyncio.run(serve())
