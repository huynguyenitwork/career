public static class TimeUtil
{
    public static string ToIsoUtc(string input)
    {
        if (string.IsNullOrWhiteSpace(input))
            return null;

        // parse ưu tiên datetimeoffset để giữ timezone
        if (DateTimeOffset.TryParse(input, out var dto))
            return dto.UtcDateTime.ToString("O"); // iso 8601 utc

        throw new FormatException("invalid time format");
    }
}

// test runner
var testCases = new Dictionary<string, string>
{
    { "2026-02-10T10:00:00Z", "2026-02-10T10:00:00.0000000Z" },
    { "2026-02-10T10:00:00+07:00", "2026-02-10T03:00:00.0000000Z" },
    {
        "2026-02-10 10:00:00",
        DateTimeOffset.Parse("2026-02-10 10:00:00").UtcDateTime.ToString("O")
    },
    {
        "02/10/2026 10:00:00 AM",
        DateTimeOffset.Parse("02/10/2026 10:00:00 AM").UtcDateTime.ToString("O")
    },
    { "", null },
};

foreach (var tc in testCases)
{
    var actual = TimeUtil.ToIsoUtc(tc.Key);

    if (actual != tc.Value)
        throw new Exception($"FAIL input={tc.Key} expected={tc.Value} actual={actual}");

    Console.WriteLine($"PASS {tc.Key} -> {actual}");
}
