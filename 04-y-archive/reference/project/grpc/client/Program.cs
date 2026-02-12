using grpc;
using Grpc.Net.Client;

var channel = GrpcChannel.ForAddress("https://localhost:7057");

var client = new Greeter.GreeterClient(channel);

var reply = await client.SayHelloAsync(
	new HelloRequest { Name = "Huy" });

Console.WriteLine(reply.Message);
