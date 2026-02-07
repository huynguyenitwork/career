# timeline

- [02-02-2026] trao đổi với anh trưởng, anh khương test luồng và giải quyết các vấn đề sau test

---

# vấn đề sau trao đổi

## ưu tiên
- timeline xử lý luồng manual (tự đặt thời gian và cam kết với nó | tự làm khó là loại)
- bổ sung thêm script loại giá mở trên skycrm và script sau mr và nơi lưu script, với loại bên rk7 dùng tổng (thay vì % | hỏi thêm anh đầy)
- bỏ validate ở phía ecom=>skytransfer (thêm mới liên tục)
- điều chỉnh lại timezone lưu trữ skytransfer(utc)=>skycrm(local)=>rk7(?) format time dùng `2026-01-15T21:35:00+07:00`
- luồng skycrm=>rk7 (gồm 2 luồng auto/manual)
- đặt trạng thái gởi sang luôn là draft từ ecom=>skytransfer (dù trạng thái có là gì). trạng thái chỉ thay đổi khi có can thiệp của người dùng trên skycrm/rk7
## dàn đều
- luồng cập nhật test lại trên rk7 (hiện lúc lưu/ được lúc không)
- bộ mapping cần có để thấy được sự thay đổi khi dữ liệu lớn dần lên

# timeline + effort
## rule rủi ro
- thêm thời gian bù giờ vì mọi việc không trôi smooth, bị gap (10-15')

## raw
# wbs – [3.3] skycrm => rk7 - ui-driven promotion service (manual)

- define api contract + mapping promotion (create/update/delete, khóa field cần dùng) [chỉ promotion | input từ ui skycrm | không backward compat] <0.75h>
- implement service skycrm=>rk7 (expose 3 endpoint ui call, stateless) [không reuse direct flow | không queue/retry | 1 request = 1 promotion] <1.5h>
- integrate rk7 xml api theo action (reuse xml client, branch create/update/delete) [giữ logic hiện có | không refactor sâu] <0.5h>
- parse rk7 response tối thiểu (success/failed, lưu raw xml) [không map business error | dùng cho debug] <0.25h>
- log trạng thái sync ui-driven (promotion_id + action + status) [log best-effort | không điều phối flow] <0.33h>
- dev test ui flow end-to-end (create/update/delete từ skycrm, verify rk7) [test tay | không automation] <0.75h>

---

# wbs – fixbug / bổ sung (daily meeting)

- script loại giá mở skycrm (convert → tổng cho rk7) [chạy sau mr | lưu scripts/migration] <0.5h>
- bỏ validate promotion ecom=>skytransfer (cho phép gửi liên tục) [không ảnh hưởng luồng khác] <0.25h>
- chỉnh timezone + datetime format skytransfer=skycrm=>rk7 (utc → local → keep offset) [format iso8601 có offset] <0.5h>
- re-test luồng skycrm=>rk7 auto/manual (độc lập service/flag) [không share state machine] <0.5h>
- fix trạng thái promotion gửi sang draft (override từ ecom) [chỉ đổi khi user can thiệp] <0.25h>

---

# tổng effort
- task mới ui-driven service: ~4.1h
- fixbug / bổ sung: ~2.0h

## editing

# wbs – [3.3] skycrm => rk7 - ui-driven promotion service (manual)

- define api contract + mapping promotion (create/update/delete, khóa field cần dùng) [chỉ promotion | input từ ui skycrm | không backward compat] <0.9h>
- implement service skycrm=>rk7 (expose 3 endpoint ui call, stateless) [không reuse direct flow | không queue/retry | 1 request = 1 promotion] <1.75h>
- integrate rk7 xml api theo action (reuse xml client, branch create/update/delete) [giữ logic hiện có | không refactor sâu] <0.65h>
- parse rk7 response tối thiểu (success/failed, lưu raw xml) [không map business error | dùng cho debug] <0.4h>
- log trạng thái sync ui-driven (promotion_id + action + status) [log best-effort | không điều phối flow] <0.5h>
- dev test ui flow end-to-end (create/update/delete từ skycrm, verify rk7) [test tay | không automation] <0.9h>
---

# wbs – fixbug / bổ sung (daily meeting)

- script loại giá mở skycrm (convert → tổng cho rk7) [chạy sau mr | lưu scripts/migration] <0.65h>
- bỏ validate promotion ecom=>skytransfer (cho phép gửi liên tục) [không ảnh hưởng luồng khác] <0.3h>
- chỉnh timezone + datetime format skytransfer=>skycrm=>rk7 (utc → local → keep offset) [format iso8601 có offset] <0.65h>
- re-test luồng skycrm=>rk7 auto/manual (độc lập service/flag) <0.65h>
- fix trạng thái promotion gửi sang draft (override từ ecom) [chỉ đổi khi user can thiệp] <0.3h>

---

# tổng effort (đã bù gap)

- task mới ui-driven service: ~5h  
- fixbug / bổ sung: ~2.7h  
- tổng cộng: ~7.7h



## handler
# thời gian
- bắt đầu xử lý 03-02-2026 01:00:14 (thứ 2)

# wbs – [3.3] skycrm => rk7 - ui-driven promotion service (manual)

- ~~define api contract + mapping promotion (create/update/delete, khóa field cần dùng) [chỉ promotion | input từ ui skycrm | không backward compat] <0.9h>~~
- ~~implement service skycrm=>rk7 (expose 3 endpoint ui call, stateless) [không reuse direct flow | không queue/retry | 1 request = 1 promotion] <1.75h>~~
- ~~integrate rk7 xml api theo action (reuse xml client, branch create/update/delete) [giữ logic hiện có | không refactor sâu] <0.65h>~~
- ~~parse rk7 response tối thiểu (success/failed, lưu raw xml) [không map business error | dùng cho debug] <0.4h>~~
- ~~log trạng thái sync ui-driven (promotion_id + action + status) [log best-effort | không điều phối flow] <0.5h>~~
- ~~dev test ui flow end-to-end (create/update/delete từ skycrm, verify rk7) [test tay | không automation] <0.9h>~~
## issue
- define api contract lookup thông tin về loại discount trong rk7 (tự tìm, nhờ hỗ trợ anh Khương, Hiệp mất thời gian ban đầu) (0.5h)
- implement service skycrm=>rk7 ban đầu sử dụng action filter (vấn đề về response người dùng) => chuyển hướng sử dụng service job queue (2h)
---

# wbs – fixbug / bổ sung (daily meeting)

- ~~script loại giá mở skycrm (convert → tổng cho rk7) [chạy sau mr | lưu scripts/migration] <0.65h>~~
- ~~bỏ validate promotion ecom=>skytransfer (cho phép gửi liên tục) [không ảnh hưởng luồng khác] <0.3h>~~
- ~~chỉnh timezone + datetime format skytransfer=>skycrm=>rk7 (utc → local → keep offset) [format iso8601 có offset] **reject*- <0.65h>~~
- re-test luồng skycrm=>rk7 auto/manual (độc lập service/flag) <0.65h>
- ~~fix trạng thái promotion gửi sang draft (override từ ecom) [luôn là draft khi tạo, cập nhật không xử lý, chỉ đổi khi user can thiệp rk7] <0.3h>~~

## explain
- time format skytransfer=>skycrm (utc → local(+7utc) → keep offset(vì không có)). đây là dạng iso8601 hoặc rfc 3339. đầu ra của skytransfer là +7 => không cần sửa vì api skycrm nhận time utc. hợp đồng api ecom gửi sang cũng là utc (không cần mapping/convert)

---

# tổng effort (đã bù gap)

- task mới ui-driven service: ~5h  
- fixbug / bổ sung: ~2.7h  
- tổng cộng: ~7.7h


## demo
- mục tiêu demo: chứng minh ui skycrm có thể điều khiển promotion xuống rk7 thủ công, không phụ thuộc auto flow, không làm chậm response user

---

## kịch bản demo chính (happy path)

- chuẩn bị 1 promotion mới trên skycrm ui → tiêu chí loại: nếu promotion có logic phức tạp nhiều loại discount rk7 chưa lookup → bỏ
- thao tác "create promotion" từ ui → tiêu chí loại: nếu cần queue/retry mới chạy được → fail vì service thiết kế stateless
- verify api skycrm=>rk7 được gọi đúng 1 request = 1 promotion → tiêu chí loại: nếu phát sinh batch hoặc multi promotion → sai scope
- kiểm tra rk7 nhận promotion thành công (status success từ xml response) → tiêu chí loại: nếu cần map business error mới hiểu → không thuộc phạm vi demo
- kiểm tra raw xml response được lưu log → tiêu chí loại: nếu không truy ra promotion_id + action + status → fail debug capability

---

## kịch bản update promotion

- sửa 1 field promotion được phép mapping (vd: thời gian, giá trị discount) → tiêu chí loại: nếu sửa field rk7 không hỗ trợ → bỏ
- trigger update promotion từ skycrm ui → tiêu chí loại: nếu update yêu cầu recreate promotion → fail contract
- verify rk7 nhận update thành công → tiêu chí loại: nếu status promotion trên rk7 bị đổi khỏi draft → fail rule override

---

## kịch bản delete promotion

- chọn promotion đã sync trước đó → tiêu chí loại: nếu promotion chưa từng tạo ở rk7 → bỏ
- thao tác delete từ skycrm ui → tiêu chí loại: nếu delete phụ thuộc manual thao tác rk7 → fail service value
- verify rk7 remove hoặc disable promotion tương ứng → tiêu chí loại: nếu không truy được promotion mapping → fail

---

## kịch bản chứng minh fix issue đã xảy ra


## kịch bản regression sau fix bug daily

### timezone / datetime

- demo gửi promotion với start/end time từ ecom → skycrm → rk7 → tiêu chí loại: nếu cần convert timezone tại skycrm → fail design
- verify time vẫn giữ utc theo contract → tiêu chí loại: nếu rk7 nhận sai offset → fail integration consistency

---

### trạng thái promotion

- demo tạo promotion từ ecom flow → verify rk7 luôn nhận trạng thái draft → tiêu chí loại: nếu promotion auto active → fail business rule
- demo update promotion → verify không override trạng thái → tiêu chí loại: nếu update làm đổi trạng thái rk7 → fail

---

## kịch bản chứng minh tính độc lập auto/manual

- bật manual flow từ ui skycrm → tiêu chí loại: nếu cần bật auto service → fail separation
- re-test auto flow promotion → tiêu chí loại: nếu manual ảnh hưởng auto → fail isolation

---

## artefact cần chuẩn bị trước demo

- 1 promotion mẫu create mới
- 1 promotion mẫu update
- 1 promotion đã sync để test delete
- access log raw xml
- màn hình rk7 verify promotion

---

## thông điệp kỹ thuật cần chốt trong demo

- service stateless
- 1 request = 1 promotion
- không queue / retry
- không backward compat
- logging chỉ phục vụ debug không orchestration
- timezone giữ nguyên utc theo contract

---

## dấu hiệu demo thất bại

- user ui phải chờ rk7 xử lý
- promotion trạng thái rk7 bị override ngoài rule
- mapping discount cần sửa tay
- flow manual ảnh hưởng auto
- không truy được log raw xml

---