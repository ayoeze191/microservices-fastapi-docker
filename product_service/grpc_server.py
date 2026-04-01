import grpc
import time
from concurrent import futures
import product_pb2
import product_pb2_grpc

products = [
    {"id": 1, "name": "Laptop", "price": 999},
    {"id": 2, "name": "Smartphone", "price": 499}
]

class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        print(f"gRPC request for product_id: {request.product_id}", flush=True)

        product = next(
            (p for p in products if p["id"] == request.product_id), None
        )

        if product:
            return product_pb2.ProductResponse(
                id=product["id"],
                name=product["name"],
                price=product["price"],
                found=True
            )
        return product_pb2.ProductResponse(found=False)

def serve():
    print("Starting gRPC server on port 50051...", flush=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running! ✅", flush=True)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()