import asyncio

import grpc

from postService.app.db.core import Base, engine
from postService.app.servicer import PostServiceServicer
from proto import post_pb2_grpc


async def serve():
    server = grpc.aio.server()
    post_pb2_grpc.add_PostsServiceServicer_to_server(PostServiceServicer(), server)
    server.add_insecure_port("[::]:50051")

    # Создаем таблицы перед запуском сервера
    await create_tables(engine)

    await server.start()
    print("gRPC PostService run at 50051 port...")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        print("gRPC PostService остановлен.", flush=True)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(serve())
