# design-pattern và các vấn đề thực tế

## mục tiêu
- hiểu pattern tồn tại để chữa đau gì
- dùng khi gặp bài toán mới, không học thuộc tên
- coi pattern là ngôn ngữ chung, không phải thần dược

## nguyên lý lõi
- pattern = đặt tên cho giải pháp đã dùng từ lâu
- khác dự án/ngôn ngữ, bản chất không đổi
- nói tên pattern = rút ngắn giao tiếp trong team

## 3 nhóm gốc (không thoát ly)
- creational: tạo object linh hoạt
- structural: ghép nối, tổ chức cấu trúc
- behavioral: điều phối hành vi, giao tiếp

## creational – đau vì tạo object
- factory: chọn loại object lúc runtime, tránh new trực tiếp
- builder: object nhiều tham số, constructor rối
- singleton: chỉ 1 instance (nguy cơ biến global)

## structural – đau vì hệ thống rối
- adapter: interface không khớp nhưng phải dùng chung
- facade: api/phần trong quá phức tạp
- decorator: thêm hành vi, không sửa code gốc

## behavioral – đau vì tương tác
- observer: 1 đổi, nhiều thằng cần biết
- strategy: nhiều thuật toán, đổi lúc runtime
- command: đóng gói hành động để queue/undo/retry

## job system nhìn bằng pattern
- job = command
- queue = invoker
- worker = executor
- callback/event = observer
- job factory = factory

## 20/80 áp dụng nhanh
- factory: tạo linh hoạt
- builder: build phức tạp
- facade: che phức tạp
- adapter: nối không khớp
- observer: phản ứng sự kiện
- strategy: đổi thuật toán
- command: gói hành động

## kết luận
- đừng tìm pattern trước
- tìm nỗi đau thực tế cần giải
- pattern chỉ là tên gắn sau cho giải pháp
