# prompt wbs + todolist cho dev (quan sát & quản lý task)

## prompt wbs
"hãy viết wbs cho task sau với góc nhìn senior dev:
- chỉ giữ đúng các hạng mục tôi nêu, không mở rộng
- mỗi task gồm:
  - <task chính> (<hành động / chi tiết thực thi>) [điều kiện | phạm vi | giả định] <effort giờ thuận-nghịch>
- ước lượng thời gian thực tế cho mỗi task với effort số giờ cần thực hiện
- định dạng markdown, bullet '-', lowercase, ngắn gọn, không giải thích thêm"

## quy ước chung
quy tắc loại nhanh:
- cái gì phải làm → () : hành động sẽ thực thi
- cái gì có thể có / giới hạn → [] : điều kiện hoặc phạm vi áp dụng
- cái gì chưa biết, cần điền → <> : placeholder bắt buộc thay
- cái gì đã là thực tế → không ngoặc : tên thật, trạng thái hiện hữu

## áp dụng với app todolist
- mỗi bullet wbs = 1 task trong todolist (copy nguyên dòng, không sửa)
- tên task = <task chính> + effort giờ
- phần () đưa vào description để theo dõi hành động thực thi
- phần [] đưa vào note để làm tiêu chí loại hoặc giới hạn
- phần <> bắt buộc điền trước khi chuyển task sang trạng thái "doing"
- không dùng subtask nếu không giúp loại sớm hoặc giảm effort
- chỉ có 3 trạng thái: todo / doing / done
- chỉ cho phép tối đa 1 task ở trạng thái doing (não single-core)
- task chưa rõ <> hoặc [] mơ hồ → giữ ở todo, không làm
- task vượt effort dự kiến >30% → stop, ghi nhận, tạo task mới
- mỗi ngày chỉ xem danh sách doing + 3 task todo tiếp theo
