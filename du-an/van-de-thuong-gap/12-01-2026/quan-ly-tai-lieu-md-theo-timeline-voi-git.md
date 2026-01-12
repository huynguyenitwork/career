# quản lý tài liệu md theo timeline với git

## bối cảnh vấn đề

bạn có nhiều tài liệu dạng file md.

- cập nhật hằng ngày
- nội dung có thể bị sửa, xóa, viết lại
- file có thể được **di chuyển giữa các folder theo ngày**
- khi cần, bạn phải **truy vết lại lịch sử thay đổi**, bao gồm:

  * dòng đã bị xóa
  * nội dung trước khi chỉnh sửa
  * file đã từng nằm ở đâu, thuộc ngày nào

đây không còn là bài toán ghi chú thông thường.
đây là bài toán **lưu giữ ký ức hệ thống**.

nguyên lý 20/80 áp dụng thẳng:

- 20% công cụ đúng → giải quyết 80% rủi ro mất dữ liệu
- công cụ đó là **git**

---

## nguyên tắc cốt lõi

- folder theo ngày chỉ là **giao diện cho con người**
- lịch sử thay đổi phải do **hệ thống kiểm soát phiên bản** quản lý
- nội dung là sự thật, vị trí file chỉ là ngữ cảnh

vì vậy:

- pkm chỉ đóng vai trò viết và đọc
- git là nơi giữ toàn bộ lịch sử sống

---

## kiến trúc khuyến nghị (đơn giản nhưng bền)

- một thư mục duy nhất
- khởi tạo git repo local
- toàn bộ tài liệu là file md

cấu trúc gợi ý:

- `docs/`

  * `2026-01-12/`
  * `2026-01-13/`
  * `shared/`
  * `archive/`

ý nghĩa:

- folder ngày: phản ánh dòng suy nghĩ theo thời gian
- shared: nội dung dùng nhiều ngày
- archive: tài liệu đã kết luận, ít thay đổi

---

## workflow hằng ngày (đi thẳng – đi nhanh)

- viết hoặc chỉnh sửa file md trong folder ngày hiện tại
- nếu cần tiếp tục nội dung cũ:

  * di chuyển file từ folder ngày cũ sang ngày mới
- nếu nội dung không còn giá trị:

  * xóa file

cuối ngày:

- commit toàn bộ thay đổi

nguyên tắc:

- **đừng sợ xóa**
- git sinh ra để cho bạn xóa mà không mất ký ức

---

## quy ước commit (rất quan trọng)

commit phải mang ý nghĩa theo dòng thời gian tư duy.

gợi ý:

- `daily: update notes 2026-01-12`
- `refactor: move notes from 01-11 to 01-12`
- `cleanup: remove obsolete decision log`

mỗi commit là một mốc nhận thức.
đừng gộp nhiều ngày vào một commit.

---

## truy vết lịch sử (phần ăn tiền)

### xem lịch sử của một file (kể cả đã bị xóa)

- `git log -- <path>`

### xem nội dung file trước khi bị xóa

- `git show <commit_hash>:<path>`

### xem ai đã xóa hoặc sửa một dòng cụ thể

- `git blame <file>`

### theo dõi file dù đã bị rename hoặc di chuyển folder

- `git log --follow <file>`

git theo dõi **nội dung**, không theo dõi tên file.
vì vậy việc di chuyển giữa các folder ngày không làm mất lịch sử.

---

## vai trò của obsidian (hoặc editor md khác)

obsidian không thay thế git.
nó đóng vai trò:

- giao diện viết nhanh
- backlink giữa các file ngày cũ và ngày mới
- search toàn bộ vault
- mở md thuần, không phá lịch sử

setup thường dùng:

- obsidian vault = git repo
- commit bằng terminal hoặc git gui

---

## những công cụ không phù hợp cho bài toán này

- notion:

  * không md-native
  * truy vết xóa yếu
- logseq không gắn git:

  * journal tốt
  * forensics kém
- pkm cloud-only:

  * phụ thuộc nền tảng
  * lịch sử không đủ sâu

---

## kết luận

nếu bạn:

- viết tài liệu md mỗi ngày
- thường xuyên sửa, xóa, di chuyển file
- cần đào lại lịch sử tư duy trong quá khứ

thì kiến trúc đúng là:

- **git để giữ ký ức**
- **pkm để kể câu chuyện**

đây không chỉ là quản lý ghi chú.
đây là **personal knowledge versioning system**.

làm đúng từ đầu, bạn sẽ không bao giờ phải hỏi:
"tại sao mình lại xóa đoạn này?"
