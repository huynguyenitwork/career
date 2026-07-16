using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/users", () => new { message = "Danh sách user (demo)" });
app.MapPost("/api/users", () => new { message = "Tạo user thành công" });

app.Run();
