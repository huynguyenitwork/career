namespace SyncTrafficSimulator.Core
{

	public class Entity
	{
		public string Id { get; }
		public State? State { get; set; }
		public bool Enabled { get; private set; } = true;

		public Entity(string id)
		{
			Id = id;
		}

		public void Disable()
		{
			Enabled = false;
		}
	}
}
