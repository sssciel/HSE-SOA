import time
from concurrent import futures

import grpc

from postService.app.post_crud import PostServiceServicer
from proto import post_pb2_grpc


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_pb2_grpc.add_PostsServiceServicer_to_server(PostServiceServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC PostService run at 50051 port...")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("gRPC PostService остановлен.")


if __name__ == "__main__":
    main()
