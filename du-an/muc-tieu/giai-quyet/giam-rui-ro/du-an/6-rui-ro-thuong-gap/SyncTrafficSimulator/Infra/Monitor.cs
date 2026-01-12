using System;

namespace SyncTrafficSimulator.Infra
{

	public class Monitor
	{
		public void Metric(string name)
		{
			Console.WriteLine($"[METRIC] {name}");
		}

		public void Log(string message)
		{
			Console.WriteLine($"[LOG] {message}");
		}
	}
}