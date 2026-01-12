namespace SyncTrafficSimulator.Core
{
	public enum State
	{
		Received,
		Validated,
		Sent,
		Acked,
		Visible,
		FailedRetryable,
		FailedNonRetryable,
		Skipped
	}
}