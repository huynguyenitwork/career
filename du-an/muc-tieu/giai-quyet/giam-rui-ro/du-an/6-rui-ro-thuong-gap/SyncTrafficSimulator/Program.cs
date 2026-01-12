using System;
using System.Collections.Generic;
using SyncTrafficSimulator.Core;
using SyncTrafficSimulator.Engine;

class Program
{
	static void Main()
	{
		var engine = new SyncEngine();

		Console.WriteLine("\n--- CREATE STORE_1 ---");
		engine.HandleEvent("STORE_1", EventType.Create);

		Console.WriteLine("\n--- DUPLICATE CREATE ---");
		engine.HandleEvent("STORE_1", EventType.Create);

		Console.WriteLine("\n--- OUT OF ORDER UPDATE ---");
		engine.HandleEvent("STORE_X", EventType.Update);

		Console.WriteLine("\n--- CONTRACT MISMATCH ---");
		engine.HandleEvent(
			"STORE_2",
			EventType.Create,
			new Dictionary<string, object> { { "invalid_contract", true } }
		);

		Console.WriteLine("\n--- DISABLE BEFORE SEND ---");
		engine.HandleEvent("STORE_3", EventType.Create);
		engine.HandleEvent("STORE_3", EventType.Disable);
		engine.HandleEvent("STORE_3", EventType.Update);

		Console.WriteLine("\n--- RANDOM ACK / VISIBILITY ---");
		for (int i = 0; i < 5; i++)
		{
			engine.HandleEvent("STORE_4", EventType.Create);
		}
	}
}
