# git – bối cảnh ra đời, tiến hóa khái niệm, nguyên tắc quyết định workflow và faq

---

## mục tiêu tài liệu

- hiểu vì sao git sinh ra → chọn đúng lệnh trong workflow
- map thuật ngữ git ↔ vấn đề thực tế nó giải quyết
- rút ngắn thời gian quyết định khi thao tác branch / history

---

## bối cảnh git sinh ra

- svn/cvs dùng mô hình central server → merge khó, branch tốn chi phí → team hạn chế tách nhánh
- dev phụ thuộc server → làm việc offline gần như không thể
- linux kernel mất bitkeeper năm 2005 → cần tool thay thế → git ra đời

---

## triết lý thiết kế git (gốc rễ quyết định cách dùng)

- git lưu snapshot toàn repo thay vì diff file → restore và branch nhanh
- mỗi dev có full history local → giảm phụ thuộc server → thao tác nhanh
- branch chỉ là pointer commit → tạo/xóa branch chi phí gần như 0
- commit là immutable object → lịch sử là nguồn sự thật

---

## timeline phát triển git theo giai đoạn

| giai đoạn              | thời gian   | vấn đề thực tế                                  | khái niệm/lệnh sinh ra                  | payoff chính                   | tiêu chí dùng        |
| ---------------------- | ----------- | ----------------------------------------------- | --------------------------------------- | ------------------------------ | -------------------- |
| tiền git (svn/cvs)     | 1990 → 2005 | phụ thuộc server, merge khó, branch tốn chi phí | centralized vcs                         | quản lý version cơ bản         | team nhỏ, ít branch  |
| git ra đời             | 2005        | linux kernel mất bitkeeper                      | commit, branch, merge, distributed repo | offline, branch rẻ, tốc độ cao | thay centralized vcs |
| git adoption           | 2006 → 2007 | history phân nhánh rối                          | rebase                                  | history tuyến tính             | branch cá nhân       |
| multi-release + hotfix | 2007 → 2008 | copy fix giữa nhiều release                     | cherry-pick                             | copy commit lẻ                 | hotfix/backport      |
| workflow linh hoạt     | 2008 → 2010 | dev cần chuyển context nhanh                    | stash                                   | lưu thay đổi tạm               | switch branch nhanh  |
| dọn lịch sử commit     | 2010 → 2012 | commit rác, khó review                          | interactive rebase, squash, amend       | history sạch                   | trước merge/pr       |
| scale open source      | 2012 → 2016 | cần cộng tác nhiều contributor                  | fork + pull request workflow            | scale collaboration            | open source/team lớn |
| automation + ci/cd     | 2016 → nay  | cần pipeline build/test/deploy                  | hook, gitflow, trunk-based workflow     | tự động hóa release            | devops/microservice  |

---
## mô hình trực quan git qua tiến hóa của cây

| git         | cây thật                    | hình dung                                          | dùng khi                 | loại khi                     |
| ----------- | --------------------------- | -------------------------------------------------- | ------------------------ | ---------------------------- |
| repository  | cả khu rừng                 | toàn bộ hệ sinh thái cây + lịch sử phát triển      | quản lý toàn bộ code     | nghĩ repo chỉ là thư mục     |
| commit      | vòng sinh trưởng thân       | mỗi vòng gỗ ghi lại trạng thái cây tại 1 thời điểm | tạo checkpoint code      | coi commit chỉ là diff       |
| branch      | cành cây                    | hướng mọc mới tách từ thân/cành                    | phát triển song song     | coi branch là copy code      |
| merge       | ghép hai cành               | hai cành mọc riêng → nối lại cùng thân             | giữ lịch sử hai nhánh    | cần history tuyến tính       |
| rebase      | cắt cành ghép lại thân mới  | giữ nội dung cành nhưng đổi điểm mọc               | cập nhật branch cá nhân  | branch đã public             |
| cherry-pick | ghép 1 mắt cây              | lấy 1 phần phát triển nhỏ ghép sang cành khác      | copy fix/hotfix riêng lẻ | cần toàn bộ nhánh            |
| stash       | buộc tạm cành non           | cột tạm phần đang mọc để xử lý việc khác           | chuyển nhánh khi code dở | lưu thay đổi dài hạn         |
| reset       | cắt bỏ phần cành mới mọc    | quay lại trạng thái trước khi cành mọc sai         | xoá commit local sai     | commit đã push               |
| revert      | mọc nhánh sửa sai           | tạo nhánh mới để trung hoà lỗi cũ                  | undo commit public       | cần xoá lịch sử              |
| squash      | gom nhiều cành nhỏ          | gộp nhiều nhánh nhỏ thành 1 nhánh gọn              | dọn history trước merge  | cần giữ chi tiết commit      |
| amend       | chỉnh vòng sinh trưởng cuối | sửa lại bước phát triển gần nhất                   | sửa commit cuối          | commit đã push               |
| remote      | rừng chung                  | nơi nhiều cây cùng tồn tại và chia sẻ              | đồng bộ team             | coi là backup đơn thuần      |
| pull        | kéo thay đổi từ rừng        | cập nhật cây theo phát triển mới từ rừng chung     | đồng bộ code team        | có thay đổi local chưa xử lý |
| push        | đưa cành lên rừng           | xuất bản cành để cây khác thấy và dùng             | chia sẻ commit           | history chưa ổn định         |

---

## khái niệm git và vấn đề nó giải quyết

### commit

- lưu snapshot trạng thái code theo thời gian
- dùng khi cần checkpoint logic để rollback/debug

---

### branch

- cho phép dev làm việc song song
- dùng khi phát triển feature hoặc thử nghiệm độc lập

---

### merge

- hợp nhất nhiều nhánh code
- giữ nguyên lịch sử commit hai nhánh

tiêu chí loại:

- history cần tuyến tính → không dùng merge

---

### rebase

- làm lịch sử commit tuyến tính
- cập nhật branch theo base mới nhất

tiêu chí chọn:

- branch cá nhân chưa share → dùng
- branch public → loại

---

### cherry-pick

- copy 1 commit cụ thể sang branch khác
- dùng cho backport hoặc hotfix production

tiêu chí chọn:

- cần commit lẻ → dùng
- cần toàn bộ lịch sử → merge/rebase

---

### stash

- tạm lưu thay đổi chưa commit
- dùng khi cần chuyển branch gấp

tiêu chí loại:

- thay đổi có giá trị lịch sử → commit thay vì stash

---

### reset

- di chuyển pointer branch về commit cũ
- dùng để bỏ commit local sai

tiêu chí loại:

- commit đã push → không dùng reset

---

### revert

- undo commit nhưng giữ lịch sử
- dùng khi commit đã public

tiêu chí chọn:

- commit public → revert
- commit local → reset

---

### squash / amend / interactive rebase

- dọn lịch sử commit trước khi merge
- sửa commit nhỏ, commit rác hoặc message sai

tiêu chí chọn:

- chuẩn bị merge → squash
- commit cuối sai message → amend

---

## workflow git hiện đại (rút gọn quyết định)

### phát triển feature

- tạo branch từ staging/main
- commit nhỏ theo logic
- rebase branch theo base trước merge
- squash commit nếu cần history gọn

---

### fix bug production

- tạo branch hotfix
- cherry-pick commit fix cần thiết
- merge vào các branch release liên quan

---

### chuyển context khi code dở

- stash thay đổi
- chuyển branch
- pop stash sau

---

## nguyên tắc chọn lệnh nhanh

- giữ lịch sử hai nhánh → merge
- cần history tuyến tính → rebase
- copy commit lẻ → cherry-pick
- undo commit public → revert
- xóa commit local → reset
- tạm lưu thay đổi → stash
- dọn commit trước merge → squash/amend

---

## mô hình tư duy gốc khi dùng git

- branch = workspace tạm
- commit = checkpoint logic
- history = tài sản quan trọng
- remote = nguồn chia sẻ sự thật

---

## sai lầm phổ biến cần loại sớm

- rebase branch đã public → lệch history
- commit quá lớn → khó debug và review
- stash quá lâu → mất ngữ cảnh
- merge liên tục từ base → history nhiễu

---

## checklist trước khi thao tác history

- thay đổi đã push chưa?
- commit cần chia sẻ hay chỉ dùng local?
- thay đổi có cần giữ lịch sử rõ không?
- thao tác có khiến người khác phải force sync không?

---

## kết luận

- git sinh ra để giải quyết collaboration quy mô lớn
- mỗi lệnh git tồn tại để xử lý xung đột lịch sử thay đổi
- chọn đúng lệnh → giảm conflict → giảm nhiễu lịch sử → giảm chi phí review

## faq
### cắt tỉa cây git trên local (loại bỏ dư thừa)
```git bash
git fetch --prune
```
### đọc hiểu cây git
[learngitbranching.js.org](https://learngitbranching.js.org/?locale=vi)

### kiểm thử cú pháp cli git
[git-school.github.io/visualizing-git](https://git-school.github.io/visualizing-git/)