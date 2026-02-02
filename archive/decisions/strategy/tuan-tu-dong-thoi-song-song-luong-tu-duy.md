# tuần tự – đồng thời – song song

## mục tiêu dùng tài liệu
- phân biệt đúng 3 mô hình xử lý và ví dụ đời thường
- chọn nhanh mô hình theo bản chất công việc
- tránh tối ưu sai ngay từ đầu

## câu hỏi khóa trước mọi quyết định
- hệ thống đang nghẽn cpu hay đang chờ io?
- chưa trả lời được → dừng, không tối ưu

## bản chất từng mô hình

- tuần tự
  - làm 1 việc tại 1 thời điểm
  - không chờ, không chia nhỏ
  - phù hợp việc đơn giản, ít tải

- đồng thời (concurrency)
  - nhiều việc cùng tồn tại nhưng không chạy cùng lúc
  - có thời gian chờ (đợi người khác, hệ thống khác)
  - tận dụng thời gian rảnh trong lúc chờ

- song song (parallel)
  - nhiều việc chạy thật sự cùng lúc
  - chia tải nặng ra cho nhiều nguồn lực
  - mục tiêu là rút ngắn tổng thời gian

## ví dụ đời thường để khóa khái niệm

- tuần tự
  - nấu cơm → ăn → rửa chén
  - chạy xong cuốc xe này mới nhận cuốc khác
  - làm việc nào xong mới được làm việc kế

- đồng thời
  - nấu cơm xong đợi chín → tranh thủ dọn nhà
  - nhắn tin xong → đợi trả lời → làm việc khác
  - việc chưa xong nhưng mình không bị chiếm dụng

- song song
  - 4 người cùng dọn 1 căn phòng
  - chia việc nặng cho nhiều người làm cùng lúc
  - mỗi người làm một phần độc lập

## luồng tư duy quyết định (loại sớm)

- có chờ → nghĩ tới đồng thời
- không chờ, chỉ tốn sức → nghĩ tới song song
- ít việc, không đáng tối ưu → tuần tự

- dùng song song cho việc phải chờ → loại
- dùng đồng thời cho việc thuần sức → loại

## cách đọc hệ thống để xác nhận
- cpu chỉ chạy nhẹ, không đều → không phải song song
- cpu rảnh nhưng vẫn chờ → đồng thời
- cpu nhiều lõi chạy căng → song song

## kết luận hành động
- mô hình xử lý là hệ quả của tài nguyên, không phải sở thích
- đồng thời giúp không lãng phí thời gian chờ
- song song mới thật sự làm nhanh hơn
- chọn sai mô hình → hệ thống phức tạp hơn nhưng không hiệu quả
