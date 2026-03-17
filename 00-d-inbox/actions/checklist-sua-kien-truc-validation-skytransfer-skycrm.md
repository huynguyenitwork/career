# checklist sửa kiến trúc validation skytranfer + skycrm

#tag: #audit #identify-and-classify #refactor #test

## audit
- scan lại toàn bộ controller + service xem danh sách cần sửa
=> est: 1-2h (2 service)

## xác định và phân loại validation

### schema (sync)
- required field
- type
- format
- length

### business
- trạng thái transaction
- quyền thực hiện
- rule domain

### integration (service/async worker)
- verify
=> est: 1-2h/service

## refactor

### controller
- thêm schema validation
- chuyển validation từ service lên controller
rule controller chỉ cần đảm bảo
- validate
- dto mapping
- call service
- return response
=> est: 1.5h

### service
- xóa schema validation
- giữ business rule
=> est: 1.5h

## test
- request invalid → fail tại controller
- request valid → vào service
- worker không validate request
=> est: 1-2h