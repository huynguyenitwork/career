# timeline
- [28-01-2026] tạo ip-public với refagent
- [28-01-2026] sửa org-id
- [28-01-2026] lưu ý chung
---

# tạo ip-public với refagent
./cloudflared.exe tunnel --url http://localhost:5901
# sửa org-id
- cập nhật bằng api parameters key là **MasterDataOrganizationId**, cache là 120' trong cacheservice(get-all-parameters)

# lưu ý chung
- cache lưu theo từng process/service và trên ram không có cách can thiệp bên ngoài trừ api