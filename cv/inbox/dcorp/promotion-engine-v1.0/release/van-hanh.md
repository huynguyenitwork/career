## mục tiêu
- thông tin kết nối: cấu hình và môi trường triển khai
- chạy đủ service skytransfer/skycrm-api/masterdata/refagent/rk7
- chạy service `skytransfer`/`refagent` trên remote server (rdp + publish)
- nắm được thông tin về source code + branch đã thực hiện
## thông tin kết nối
### cấu hình 
#### parameter skytransfer
- tham khảo: [[data-layer#3.1 system parameters]]
#### org id
- stag: `8547` (MH | QSR)
- dev: `8582` (MH | QSR)

### môi trường triển khai
#### stg/dev
1. dùng chung
	- skytransfer: http://118.69.108.41:2340
	- refagent: http://118.69.108.41:2329
	- rk7: https://118.69.108.41:2323
2. tách riêng
	- skycrm: 
		- staging: https://api-stg.dcorp.com.vn/crm
		- dev: https://api-dev.dcorp.com.vn/crm
#### local
- skytransfer: http://localhost:2340
- refagent: http://localhost:2329
- skycrm: http://localhost:6001
- masterdata (grpc): http://localhost:50031
- rk7: https://118.69.108.41:2323
*lưu ý*: chỉ môi trường `local` cần chạy service masterdata (`stg/dev` không cần vì dùng kiến trúc microservice)

## chạy service skytransfer/refagent
### bước 1: đăng nhập server
* `mstsc` → `192.168.2.32`
* user/pass: `administrator / Dcorp@2025`
### bước 2: stop app (trước khi publish)
- port 2340: dùng với skytransfer
- port 2329: dùng với refagent
```bat
netstat -ano | findstr 2340
taskkill /f /pid <pid>
netstat -ano | findstr 2329
taskkill /f /pid <pid>
```
* còn pid → không publish
### bước 2 publish
### case 1: source nằm trên server (ổ C)
* chạy publish trong `rider` hoặc `visual studio` trực tiếp trên server
* target:
  * `C:\huynp-dev\skytransfer`
  * `C:\huynp-dev\refagent`
* bắt buộc:
  * `"Delete existing files" = true`
### case 2: source nằm local (máy dev)
* publish từ local → qua network share
* target:
  * `//skyxqaserver/huynp-dev/skytransfer`
  * `//skyxqaserver/huynp-dev/refagent`
* yêu cầu:
  * có quyền `administrator`
  * truy cập được `\\SKYXQASERVER\c$`
* fail:
  * không access được → check network / credential
  * thiếu file → publish lỗi → không run
![[publish-skytransfer.jpg]]
### bước 3 kiểm tra output
* mỗi app phải có:
  * `.exe`
  * `.dll`
  * `appsettings.*`
* thiếu → stop → không chạy
### bước 4 chạy app
```bat
start "" "C:\huynp-dev\shortcut\skytransfer.lnk"
start "" "C:\huynp-dev\shortcut\refagent.lnk"
```
* sai shortcut → chạy nhầm bản → sửa ngay
### bước 5 kiểm tra process
```bat
tasklist | findstr skytransfer
tasklist | findstr refagent
```
* không thấy → app crash → xem log
### bước 6 kiểm tra port
```bat
curl http://localhost:2340
curl http://localhost:2329
```
* 2340 fail → lỗi `skytransfer`
* 2329 fail → lỗi `refagent`
### bước 7 tắt app
```bat
netstat -ano | findstr 2340
netstat -ano | findstr 2329
taskkill /f /pid <pid>
```
* verify:
  * không còn pid → ok
## source code
### module skytransfer
* env: `dev`/`staging` (thiết lập qua file cấu hình)
* branch: `sap-ecom-sync-order-discount`
### module skycrm-api
* env: `dev`/`staging`
* branch env: `origin/develop`/ `origin/staging`
* branch feature: `develop-huynp-base`/`staging-huynp-base`
* note: 
	* env dev: đã merge `develop-huynp-base` vào `develop` mới nhất ngày 23/04/2026 [mr-396](https://gitlab.skyxtech.com.vn/back-end/skycrm-api/-/merge_requests/396)
	* env stg: chưa merge `staging-huynp-base` vào `staging` mới nhất ngày 19/03/2026 [mr-336](https://gitlab.skyxtech.com.vn/back-end/skycrm-api/-/merge_requests/336)
### module skyresto-webman
* env: `dev` (chưa thực hiện env staging)
* branch: `huynp-dev/feat/dc-14585`
* note: đã merge `huynp-dev/feat/dc-14585` vào `develop` mới nhất ngày 22/04/2026
### module masterdata
* env: `dev`/`staging`
* branch env: `develop`/ `staging`
* branch feature: `develop-huynp-base`/`staging-huynp-base`
* note: 
	* env dev: đã merge `develop-huynp-base` vào `develop` mới nhất ngày 24/03/2026 [mr-487](https://gitlab.skyxtech.com.vn/back-end/masterdata-api/-/merge_requests/487)
	* env stg: chưa merge `staging-huynp-base` vào `staging` mới nhất ngày 04/04/2026 [mr-448](https://gitlab.skyxtech.com.vn/back-end/masterdata-api/-/merge_requests/488)
### module refagent
* env: `dev`/`staging`
* branch: `feat/ref-agent-qsr`