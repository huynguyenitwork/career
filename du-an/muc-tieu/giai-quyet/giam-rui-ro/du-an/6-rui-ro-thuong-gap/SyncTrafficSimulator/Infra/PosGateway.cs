using System;

namespace SyncTrafficSimulator.Infra
{
	public class PosGateway
	{
		private static readonly Random Random = new Random();

		public string Send(string entityId)
		{
			// 20% chance không ACK
			return Random.NextDouble() < 0.2
				? null
				: "ACK";
		}
	}
}
