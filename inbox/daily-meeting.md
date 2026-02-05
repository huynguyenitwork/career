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

- define api contract + mapping promotion (create/update/delete, khóa field cần dùng) [chỉ promotion | input từ ui skycrm | không backward compat] <0.9h>
- implement service skycrm=>rk7 (expose 3 endpoint ui call, stateless) [không reuse direct flow | không queue/retry | 1 request = 1 promotion] <1.75h>
- integrate rk7 xml api theo action (reuse xml client, branch create/update/delete) [giữ logic hiện có | không refactor sâu] <0.65h>
- parse rk7 response tối thiểu (success/failed, lưu raw xml) [không map business error | dùng cho debug] <0.4h>
- log trạng thái sync ui-driven (promotion_id + action + status) [log best-effort | không điều phối flow] <0.5h>
- dev test ui flow end-to-end (create/update/delete từ skycrm, verify rk7) [test tay | không automation] <0.9h>

## issue
- define api contract lookup thông tin về loại discount trong rk7 (tự tìm, nhờ hỗ trợ anh Khương, Hiệp mất thời gian ban đầu) (0.5h)
- implement service skycrm=>rk7 ban đầu sử dụng action filter (vấn đề về response người dùng) => chuyển hướng sử dụng service job queue (2h)
---

# wbs – fixbug / bổ sung (daily meeting)

- ~~script loại giá mở skycrm (convert → tổng cho rk7) [chạy sau mr | lưu scripts/migration] <0.65h>~~
- ~~bỏ validate promotion ecom=>skytransfer (cho phép gửi liên tục) [không ảnh hưởng luồng khác] <0.3h>~~
- ~~chỉnh timezone + datetime format skytransfer=>skycrm=>rk7 (utc → local → keep offset) [format iso8601 có offset] **reject** <0.65h>~~
- re-test luồng skycrm=>rk7 auto/manual (độc lập service/flag) <0.65h>
- ~~fix trạng thái promotion gửi sang draft (override từ ecom) [luôn là draft khi tạo, cập nhật không xử lý, chỉ đổi khi user can thiệp rk7] <0.3h>~~

## explain
- time format skytransfer=>skycrm (utc → local(+7utc) → keep offset(vì không có)). đây là dạng iso8601 hoặc rfc 3339. đầu ra của skytransfer là +7 => không cần sửa vì api skycrm nhận time utc. hợp đồng api ecom gửi sang cũng là utc (không cần mapping/convert)

---

# tổng effort (đã bù gap)

- task mới ui-driven service: ~5h  
- fixbug / bổ sung: ~2.7h  
- tổng cộng: ~7.7h