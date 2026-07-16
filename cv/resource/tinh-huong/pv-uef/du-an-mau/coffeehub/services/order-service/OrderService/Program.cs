using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/orders", () => new { message = "Danh sách order (demo)" });
app.MapPost("/api/orders", () => new { message = "Tạo đơn hàng thành công" });

app.Run();
