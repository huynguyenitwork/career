using System;
using SyncTrafficSimulator.Core;

namespace SyncTrafficSimulator.Engine
{
	public class AutoHealer
	{
		public void Retry(Entity entity)
		{
			Console.WriteLine($"[HEAL] Retry entity={entity.Id}");
			entity.State = State.FailedRetryable;
		}

		public void Skip(Entity entity, string reason)
		{
			Console.WriteLine($"[HEAL] Skip entity={entity.Id} reason={reason}");
			entity.State = State.Skipped;
		}
	}
}
