## timeline 
- rule command-driven khi entity phụ thuộc cha/mẹ (parent–child)
- rule command-driven cho api create / update / delete từ ecom → rk7 (áp dụng trên 1 đối tượng)

---

## rule command-driven khi entity phụ thuộc cha/mẹ (parent–child)

phần này **bổ sung trực tiếp cho tài liệu cud ở trên**, không thay đổi bản chất,
chỉ làm rõ khi entity **không đứng một mình** (ví dụ: discount thuộc discount group).

---

## nguyên tắc gốc

- lifecycle của **child phụ thuộc parent**
- rk7 (system of record) **không tự ý tạo hoặc hồi sinh parent**
- mọi thao tác với child **phải kiểm tra trạng thái parent trước**

phạm vi áp dụng: mọi mô hình aggregate có quan hệ cha/mẹ trong domain
(discount–group, item–category, price–pricebook…).

---

## 1. create (request_create) với child entity

### rule xử lý

- nếu **parent không tồn tại**:
  - ~~→ **reject**~~
  - ~~lý do: child không được tồn tại độc lập ngoài aggregate hợp lệ~~
  - ~~phạm vi áp dụng: system of record, parent sở hữu lifecycle~~

	- **ngoại lệ bootstrap (khởi tạo ban đầu)**:
		- nếu **parent chưa từng tồn tại trong hệ thống** và request thuộc luồng setup ban đầu:
		- → **cho phép tạo parent trước, sau đó tạo child**
		- lý do:
			* cần khởi tạo aggregate root lần đầu để hệ thống vận hành
			* không tồn tại parent thì không thể có child về mặt nghiệp vụ
			* phạm vi áp dụng:
			* bootstrap system
			* setup merchant / dcgroup lần đầu
			* migration dữ liệu gốc
		- giới hạn:
			* chỉ áp dụng khi parent chưa từng tồn tại
			* không áp dụng cho runtime thông thường
			* không áp dụng nếu parent đã từng bị soft-delete
- nếu **parent tồn tại nhưng soft-delete / inactive**:
	- → **reject**
	- lý do: parent đã bị loại khỏi lifecycle nghiệp vụ, child không được gắn vào
	- phạm vi áp dụng: soft-delete mang ý nghĩa nghiệp vụ

- nếu **parent tồn tại và active**:
	- tiếp tục áp dụng rule create của child:
		- child chưa tồn tại → create
		- child active → reject (duplicate)
		- child soft-delete → reject

### kết luận
- create child **không được auto-create parent**
- create child **không được revive parent**

---

## 2. update (request_update) với child entity

### rule xử lý

- nếu **parent không tồn tại**:
  - → **reject**
  - lý do: aggregate không hợp lệ

- nếu **parent soft-delete / inactive**:
  - → **reject**
  - lý do: không cho phép thay đổi child của aggregate đã bị đóng

- nếu **parent active**:
  - tiếp tục rule update child:
    - child active → update
    - child missing → reject
    - child soft-delete → reject

### kết luận
- update child **luôn phụ thuộc parent đang active**
- không có update ngầm để "vá" aggregate hỏng

---

## 3. delete (request_delete) với child entity

### rule xử lý

- nếu **parent không tồn tại**:
  - → **noop hoặc reject** (theo policy)
  - lý do: không có aggregate hợp lệ để thao tác

- nếu **parent soft-delete / inactive**:
  - → **noop**
  - lý do: child đã mặc định không còn hiệu lực theo parent

- nếu **parent active**:
  - áp dụng rule delete child:
    - child active → soft-delete
    - child soft-delete → noop
    - child missing → noop hoặc reject

### kết luận
- delete child **không làm thay đổi parent**
- delete parent thường kéo theo **vô hiệu hóa toàn bộ child** (cascade theo domain)

---

## 4. điểm chốt để implement không sai

- parent **luôn được kiểm tra trước child**
- không auto-create, không auto-revive parent
- child không bao giờ vượt quyền lifecycle của parent
- mọi reject đều là hành vi đúng trong command-driven

nói gọn kiểu kỹ sư:

> parent chết thì con không được sinh,  
> parent chưa sống thì con không được sửa,  
> parent đã đóng vòng đời thì cả nhà dừng lại.

rule này kết hợp với tài liệu cud trước đó là **đủ chặt để code production**.

## rule command-driven cho api create / update / delete từ ecom → rk7 (áp dụng trên 1 đối tượng)

tài liệu này mô tả **chính xác hành vi cần implement** trong mô hình command-driven,
khi rk7 là **system of record / source of truth**, nhằm tránh mơ hồ và tránh hiểu nhầm
giữa create mới, update, duplicate và revive.

---

## 1. tiền đề bắt buộc

- rk7 là **system of record**, sở hữu và quyết định toàn bộ lifecycle nghiệp vụ của entity
- ecom chỉ gửi **command request**, không có quyền ép trạng thái
- mỗi entity có **business key** (code, name + type…)
- rk7 **không cho phép trùng business key trong cùng scope**, để bảo toàn lịch sử và audit

phạm vi áp dụng: các entity có lifecycle nghiệp vụ rõ ràng và ảnh hưởng lịch sử (ví dụ:
discount, promotion, pricing rule); không áp dụng cho hệ chỉ làm sync/mirror/read-model.

---

## 2. create (request_create)

### ý nghĩa
ecom yêu cầu rk7 tạo **một entity mới về mặt nghiệp vụ**, tức là một entity
chưa từng tồn tại trong lifecycle của rk7.

### rule xử lý

- nếu **chưa tồn tại entity nào** với cùng business key:
  - → **create mới**
  - lý do: entity hoàn toàn mới, chưa từng tham gia lifecycle nghiệp vụ
  - phạm vi áp dụng: áp dụng cho system of record; hành vi tạo mới được kiểm soát tại rk7

- nếu **đã tồn tại entity active** với cùng business key:
  - → **reject**
  - lý do: entity đã tồn tại và đang hợp lệ; create trong trường hợp này sẽ tạo duplicate
  - phạm vi áp dụng: áp dụng cho entity yêu cầu business key duy nhất; không áp dụng cho
    hệ cho phép upsert hoặc nhiều bản ghi cùng key

- nếu **đã tồn tại entity soft-delete** với cùng business key:
  - → **reject**
  - lý do: entity đã bị rk7 loại khỏi lifecycle nghiệp vụ; soft-delete mang ý nghĩa
    quyết định kinh doanh cuối nhằm bảo toàn lịch sử (audit, hóa đơn, báo cáo),
    không cho phép quay lại vòng đời thông qua create/update thông thường
  - phạm vi áp dụng: áp dụng khi soft-delete có ý nghĩa nghiệp vụ; không áp dụng cho
    soft-delete kỹ thuật trong hệ sync/mirror

### kết luận
- không tạo duplicate
- không revive soft-delete
- create **chỉ dành cho entity hoàn toàn mới về mặt nghiệp vụ**

---

## 3. update (request_update)

### ý nghĩa
ecom yêu cầu thay đổi **entity đang tồn tại hợp lệ** trong rk7.

### rule xử lý

- nếu entity **tồn tại và active**:
  - → **update**
  - lý do: entity đang trong lifecycle hợp lệ, cho phép thay đổi trạng thái
  - phạm vi áp dụng: áp dụng cho entity active trong system of record

- nếu entity **không tồn tại**:
  - → **reject**
  - lý do: update giả định entity đã tồn tại; cho phép update sẽ dẫn tới tạo ngầm entity
  - phạm vi áp dụng: áp dụng cho command-driven; không áp dụng cho sync-driven upsert

- nếu entity **soft-delete**:
  - → **reject**
  - lý do: entity đã bị loại khỏi lifecycle nghiệp vụ; không cho phép chỉnh sửa
    để tránh phá vỡ lịch sử và audit
  - phạm vi áp dụng: áp dụng khi soft-delete là quyết định nghiệp vụ cuối

### kết luận
- update **không bao giờ tạo mới**
- update **không hồi sinh entity đã xóa**

---

## 4. delete (request_delete)

### ý nghĩa
ecom yêu cầu rk7 loại entity khỏi trạng thái hoạt động.

### rule xử lý

- nếu entity **active**:
  - → **soft-delete**
  - lý do: soft-delete bảo toàn lịch sử trong khi ngăn entity tham gia tương lai
  - phạm vi áp dụng: áp dụng cho entity có lịch sử nghiệp vụ cần lưu vết

- nếu entity **soft-delete**:
  - → **noop**
  - lý do: trạng thái đã đạt mục tiêu; thao tác lặp không làm thay đổi kết quả
  - phạm vi áp dụng: áp dụng cho command idempotent

- nếu entity **không tồn tại**:
  - → **noop hoặc reject** (theo policy)
  - lý do: không có trạng thái hợp lệ để xóa; quyết định tùy thuộc vào mức độ strict của api
  - phạm vi áp dụng: noop thường dùng cho tích hợp lỏng; reject dùng khi cần phát hiện lỗi sớm

### kết luận
- delete là **terminal action** trong lifecycle nghiệp vụ
- delete không thể bị đảo ngược qua create/update thông thường

---

## 5. tóm tắt rõ ràng

- create:
  - không tạo duplicate
  - entity active hoặc soft-delete → reject
- update:
  - chỉ update entity active
  - missing hoặc soft-delete → reject
- delete:
  - chỉ soft-delete
  - không tạo mới, không revive

không có hành vi:
- tự sinh bản ghi mới ngoài create hợp lệ
- tự hồi sinh entity đã bị loại
- tự reconcile để giống upstream

đây là **chuẩn command-driven khi rk7 là system of record**.
