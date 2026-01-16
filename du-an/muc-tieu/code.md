# extension

## vscode
- favories path: D:\dcorp\skytransfer\.favorites.json

##vs
- favories path: D:\dcorp\skytransfer\SkyTransfer.favdoc.user

# lưu ý
- c# phiên bản là max 7.3 nên không hỗ trợ kiểm tra null 
- phần mềm dùng trong thị trường việt nam
- thực hiện code với tối đa trước, không lỗi => tối ưu sau
- hỏi đúng người đúng vai trò (nghe hiểu)
- các thuộc tính **created, updated** liên quan đến ngày tạo thì tạo sau trong các bảng chính promotion
- hiểu tới đâu nói tới đó để mọi người hiểu cùng không chờ, **không cần chuẩn bị nhiều**

# dotnet
- update database
dotnet ef database update --project AppServer.csproj --verbose

- cài/gỡ ef
dotnet tool install --global dotnet-ef --version 2.1.0
dotnet tool uninstall --global dotnet-ef --version 2.1.0
- xuất model từ database (lệnh này không có dataannotation)
dotnet ef dbcontext scaffold --project AppServer.csproj "Server=localhost,1433;Database=RK7_INT;User Id=sa; Password=YourStrong!Passw0rd;" Microsoft.EntityFrameworkCore.SqlServer --output-dir Models --context-dir Models/DbContext --context EcomPromotionDbContext --table EcomPromotion --table EcomPromotionApplicableTime --table EcomPromotionExcludedDate --model-namespace Models.Entities --data-annotations --force --verbose

# tiếp cận database first
không migration
không seed mẫu
bảng tạo tay
dữ liệu test = data thật từ ecom
lấy file input đúng hệ thống → map và process

# luồng xử lý

## có sẵn

	- payload
	- trường mô tả (loại, ràng buộc, mô tả)
	- kịch bản
	- controller của price-sync
## cách thực hiện

### 1. xử lý với scheme đầu tiên

- gọi api thực hiện web-hook
	+ đầu vào request (ok)
	+ thực hiện test và gọi api (ok)
- validate model
- xử lý đầu vào và lưu trữ
	+ tạo service
		+ đăng ký service (ok)
		+ khởi tạo response object 
			+ tạo bảng trong database dựa trên request => scaffold tạo model với data-annotations hoặc dùng extension "ef core power tools" (done)

		+ chạy task async (ok)
		+ chuyển đổi dto → entity <promotion> [tạo class EcomPromotionDtoMapper, EcomPromotionApplicableTimeDtoMapper, EcomPromotionExcludedDateDtoMapper] (ok)
		+ thêm promotion vào database và đăng ký chúng với Startup AddScoped[thêm các quản lý repository như EcomPromotionDataManage] (ok)
		+ duyệt qua từng **ExcludedDates** và **ApplicableTimes** (ok)
		+ gán PromotionId cho mỗi item (**ExcludedDates** và **ApplicableTimes**) (ok)
		+ chuyển đổi dto → entity (item) (ok)
		+ thêm item vào database (ok)
		+ gán dữ liệu vào response (ok)
		+ đánh dấu sự kiện thay đổi 
		+ xử lý exception nếu có lỗi (ok)
		+ trả về response (ok)
- ngoại lệ 500 nếu không thực thi (ok)
- kiểm thử thủ công (ok)

# tham khảo
price-sync
addscope service có tác dụng gì?

# code

## subfix
-Selection,Type: string
-Combos,Products,Variants,Ids ...: list
-Count: int
## mapping

## request
-liststring=>string
-listitem=>item