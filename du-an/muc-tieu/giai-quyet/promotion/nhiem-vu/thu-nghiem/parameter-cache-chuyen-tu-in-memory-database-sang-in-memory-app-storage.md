# tài liệu kỹ thuật

## chuyển từ in-memory database sang in-memory app storage

### 1. bối cảnh

hệ thống hiện tại sử dụng:

* `parameter` entity
* `parameterservices` đọc dữ liệu qua `iparameterrepository`
* repository ban đầu trỏ vào database (hoặc ef in-memory database)

mục tiêu:

* **không dùng database**
* **không dùng ef in-memory**
* dữ liệu chỉ tồn tại **trong bộ nhớ của application**
* giữ nguyên service, interface, cache, luồng gọi hiện tại

---

### 2. so sánh nhanh hai cách tiếp cận

#### in-memory database (ef in-memory)

* vẫn cần dbcontext
* vẫn có lifecycle kiểu database
* phức tạp hơn cho test logic
* dễ lệch hành vi so với production

#### in-memory app storage (cách mới)

* dữ liệu lưu bằng `list<T>` / `dictionary`
* không dbcontext
* không ef
* kiểm soát hoàn toàn dữ liệu
* phù hợp test, dev, poc

→ **mục tiêu tài liệu này là cách thứ hai**

---

### 3. nguyên tắc thiết kế

* service **không biết** dữ liệu nằm ở đâu
* storage chỉ là implementation của repository
* repository có thể:

  * db
  * in-memory app
* đổi storage = đổi dependency injection, không đổi code nghiệp vụ

---

### 4. kiến trúc sau khi chuyển

```
controller
   ↓
parameterservices
   ↓
iparameterrepository
   ↓
inmemoryparameterrepository (list trong ram)
```

cache vẫn nằm **trên service**, không thay đổi.

---

### 5. interface giữ nguyên

#### service

```csharp
public interface IParameterServices
{
    IEnumerable<Parameter> Get(
        Expression<Func<Parameter, bool>> filter = null,
        Func<IQueryable<Parameter>, IOrderedQueryable<Parameter>> orderBy = null
    );
    Parameter GetByParam(string paramName);
}
```

#### repository

```csharp
public interface IParameterRepository
{
    IEnumerable<Parameter> Get(
        Expression<Func<Parameter, bool>> filter = null,
        Func<IQueryable<Parameter>, IOrderedQueryable<Parameter>> orderBy = null
    );
}
```

---

### 6. triển khai in-memory app repository

```csharp
public class InMemoryParameterRepository : IParameterRepository
{
    public static readonly List<Parameter> _store = new List<Parameter>
	{
		new Parameter
		{
			Id = 1,
			Name = "Sky Cloud Server",
			Status = 4,
			ParentId = 0,
			Description = null,
			ParamName = "SkyCloudServer",
			IntVal = 0,
			StrVal = "https://api-dev.dcorp.com.vn/"
		},
		new Parameter
		{
			Id = 2,
			Name = "Sky Cloud Organization",
			Status = 4,
			ParentId = 0,
			Description = null,
			ParamName = "SkyCloudOrganization",
			IntVal = 0,
			StrVal = "MH | QSR"
		},
		new Parameter
		{
			Id = 3,
			Name = "Sky Cloud Api Suffix CRM",
			Status = 4,
			ParentId = 0,
			Description = null,
			ParamName = "SkyCloudApiSuffixCRM",
			IntVal = 0,
			StrVal = "crm/"
		},
		new Parameter
		{
			Id = 4,
			Name = "Sky Cloud Api Suffix MasterData",
			Status = 4,
			ParentId = 0,
			Description = null,
			ParamName = "SkyCloudApiSuffixMasterData",
			IntVal = 0,
			StrVal = "masterdata/"
		}
	};

    public IEnumerable<Parameter> Get(
        Expression<Func<Parameter, bool>> filter = null,
        Func<IQueryable<Parameter>, IOrderedQueryable<Parameter>> orderBy = null
    )
    {
        IQueryable<Parameter> query = _store.AsQueryable();

        if (filter != null)
            query = query.Where(filter);

        if (orderBy != null)
            query = orderBy(query);

        return query.ToList();
    }
}
```

đặc điểm kỹ thuật:

* dữ liệu sống trong ram của process
* restart app là mất data
* thread-safe ở mức cơ bản (phù hợp test/dev)
* không phụ thuộc database hay ef

---

### 7. service sử dụng in-memory app storage

service **không thay đổi logic**, chỉ nhận repository qua constructor.

```csharp
public class ParameterServices : IParameterServices
{
    private readonly IParameterRepository _parameters;
    private readonly ICacheProvider _cache;

    public ParameterServices(
        IParameterRepository paramRepository,
        ICacheProvider cacheProvider
    )
    {
        _parameters = paramRepository;
        _cache = cacheProvider;
    }

    public IEnumerable<Parameter> Get(
        Expression<Func<Parameter, bool>> filter = null,
        Func<IQueryable<Parameter>, IOrderedQueryable<Parameter>> orderBy = null
    )
    {
        var cached =
            _cache.GetFromCache<IEnumerable<Parameter>>(Constants.Cache.Parameters);

        if (cached != null)
        {
            var query = cached.AsQueryable();

            if (filter != null)
                query = query.Where(filter);

            if (orderBy != null)
                return orderBy(query).ToList();

            return query.ToList();
        }

        var data = _parameters.Get(filter, orderBy).ToList();
        _cache.SetCache(Constants.Cache.Parameters, data);

        return data;
    }
	
	public Parameter GetByParam(string paramName)
	{
		var parameters = _cache.GetFromCache<IEnumerable<Parameter>>(Constants.Cache.Parameters);

		if (parameters != null)
			return parameters.Where(i => i.ParamName == paramName).FirstOrDefault();

		return _parameters.Get(i => i.ParamName == paramName).FirstOrDefault();
	}
}
```

---

### 8. cấu hình dependency injection

#### dùng in-memory app storage (test / dev)

```csharp
services.AddSingleton<IParameterRepository, InMemoryParameterRepository>();
services.AddScoped<IParameterServices, ParameterServices>();
```

#### quay lại database (production)

```csharp
services.AddScoped<IParameterRepository, ParameterRepository>();
services.AddScoped<IParameterServices, ParameterServices>();
```

---

### 9. lợi ích đạt được

* bỏ hoàn toàn database cho parameter
* test nhanh, không setup môi trường
* service và controller không đổi
* cache vẫn hoạt động
* rollback cực nhanh

---

### 10. giới hạn cần lưu ý

* dữ liệu không persistence
* không phù hợp multi-instance
* không dùng cho production nếu parameter cần lưu lâu dài

---

### 11. kết luận

chuyển từ **in-memory database** sang **in-memory app storage** thực chất là:

> bỏ dbcontext
> giữ repository
> thay cách lưu dữ liệu bằng list trong ram
> service không biết và không cần biết

đây là cách **đơn giản, kiểm soát tốt, ít rủi ro**, rất phù hợp cho test, dev và spike kỹ thuật.

nếu cần, bước nâng cấp tiếp theo hợp lý là:

* preload parameter khi startup
* dùng immutable collection
* hoặc ghép memory → redis → db theo tầng ưu tiên
