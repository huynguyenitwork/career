# mục tiêu
- mô tả flow nhánh git ở mức vận hành
- phân biệt nhánh gốc, nhánh cá nhân, nhánh staging
- dùng để thống nhất cách tạo, merge, quay vòng branch
- loại bỏ chi tiết kỹ thuật git không ảnh hưởng quyết định

# sơ đồ

```plantuml
@startuml
skinparam roundcorner 10

rectangle "main / prod" as main
rectangle "root-branch\n(new-branch-feat-root)" as root

rectangle "dev\n(dev cá nhân)" as dev1
rectangle "stag\n(staging kỹ thuật)" as stag

main --> root
root --> dev1
dev1 --> stag
stag --> root

note right of root
luôn là nhánh mới nhất
gốc sinh branch cá nhân
end note

note left of dev1
mỗi dev 1 nhánh riêng
không phải nhánh quản lý
end note
@enduml
```