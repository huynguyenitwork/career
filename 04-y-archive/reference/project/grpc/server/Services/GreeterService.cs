using grpc;
using Grpc.Core;

namespace server.Services
{
	public class GreeterService : Greeter.GreeterBase
	{
		public override async Task<HelloReply> SayHello(
			HelloRequest request,
			ServerCallContext context)
		{
			await Task.Delay(100);

			return new HelloReply
			{
				Message = $"Hello {request.Name}"
			};
		}
	}
}
