using System;
using System.Collections.Generic;
using SyncTrafficSimulator.Core;
using SyncTrafficSimulator.Infra;

namespace SyncTrafficSimulator.Engine
{


	public class SyncEngine
	{
		private readonly Dictionary<string, Entity> _entities = new Dictionary<string, Entity>();
		private readonly HashSet<(string, EventType)> _idempotencyKeys = new HashSet<(string, EventType)>();

		private readonly Monitor _monitor = new Monitor();
		private readonly PosGateway _pos = new PosGateway();
		private readonly AutoHealer _healer = new AutoHealer();

		private static readonly Random Random = new Random();

		public void HandleEvent(string businessId, EventType eventType, Dictionary<string, object> payload = null)
		{
			var key = (businessId, eventType);

			// (1) Duplicate
			if (_idempotencyKeys.Contains(key))
			{
				_monitor.Metric("duplicate_event");
				return;
			}
			_idempotencyKeys.Add(key);

			_entities.TryGetValue(businessId, out var entity);

			// (2) Out of order
			if (eventType == EventType.Update && entity == null)
			{
				_monitor.Metric("out_of_order_event");
				return;
			}

			// CREATE
			if (eventType == EventType.Create)
			{
				entity = new Entity(businessId);
				entity.State = State.Received;
				_entities[businessId] = entity;
			}

			// DISABLE
			if (eventType == EventType.Disable && entity != null)
			{
				entity.Disable();
			}

			// (3) Precondition fail
			if (entity != null && !entity.Enabled)
			{
				_monitor.Metric("precondition_failed");
				_healer.Skip(entity, "entity_disabled");
				return;
			}

			// (6) Contract mismatch
			if (payload != null && payload.ContainsKey("invalid_contract"))
			{
				_monitor.Metric("contract_mismatch");
				if (entity != null)
				{
					entity.State = State.FailedNonRetryable;
				}
				return;
			}

			// Send to POS
			if (entity != null)
			{
				entity.State = State.Sent;
			}
			var ack = _pos.Send(entity.Id);

			// (4) No ACK
			if (ack == null)
			{
				_monitor.Metric("ack_timeout");
				_healer.Retry(entity);
				return;
			}

			entity.State = State.Acked;

			// (5) Not visible to user
			if (Random.NextDouble() < 0.2)
			{
				_monitor.Metric("not_visible");
				_healer.Retry(entity);
				return;
			}

			entity.State = State.Visible;
			_monitor.Log($"Entity {entity.Id} is visible to user");
		}
	}
}