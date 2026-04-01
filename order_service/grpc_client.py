import grpc
import product_pb2
import product_pb2_grpc

def get_product_via_grpc(product_id: int):
    # 👇 Change product-service to grpc-server!
    channel = grpc.insecure_channel('grpc-server:50051')
    stub = product_pb2_grpc.ProductServiceStub(channel)

    try:
        response = stub.GetProduct(
            product_pb2.ProductRequest(product_id=product_id)
        )
        if response.found:
            return {
                "id": response.id,
                "name": response.name,
                "price": response.price
            }
        return None
    except grpc.RpcError as e:
        print(f"gRPC error: {e}", flush=True)
        return None