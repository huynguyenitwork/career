using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using StackExchange.Redis;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

ConnectionMultiplexer redis = ConnectionMultiplexer.Connect("redis:6379");
var db = redis.GetDatabase();

app.MapGet("/api/products", async () => {
    var cacheKey = "all_products";
    var cached = await db.StringGetAsync(cacheKey);
    if (cached.HasValue)
        return JsonSerializer.Deserialize<List<string>>(cached!);

    var products = new List<string> { "Espresso", "Latte", "Cold Brew" };
    await db.StringSetAsync(cacheKey, JsonSerializer.Serialize(products));
    return products;
});

app.MapGet("/api/suggest", async () => {
    using var http = new HttpClient();
    var res = await http.GetStringAsync("http://ai-service:8000/suggest?query=đắng");
    return res;
});

app.Run();
