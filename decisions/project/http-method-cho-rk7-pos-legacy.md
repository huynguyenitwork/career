# http method cho rk7 / pos legacy

## bối cảnh
- api xml, command-based
- không phải restful
- http không mang ý nghĩa crud

## nguyên tắc
- tất cả request đều dùng **http post**
- hành vi hệ thống do "cmd" trong xml quyết định
- http chỉ là kênh truyền

## mapping nghiệp vụ (để khỏi tranh luận)
- query / filter → post + cmd="getrefdata"
- add → post + cmd="addrefdata | createxxx"
- update → post + cmd="updaterefdata"
- delete → post + cmd="deleterefdata"
- action / rule → post + cmd="applyxxx | executexxx"

## tiêu chí loại nhanh
- dùng get / put / delete trực tiếp với rk7 → sai
- debug theo http method → nhiễu
- cố rest-hoá api legacy → tốn công, rủi ro

## vì sao chỉ dùng post
- **payload xml dài**, phức tạp
- **thiết kế theo rpc / command pattern**
- ưu tiên transaction + nghiệp vụ
- **ra đời trước rest**

## cách làm đúng trong hệ thống hiện đại
- giữ nguyên rk7 api
- bọc adapter / service trung gian nếu cần rest
- mapping rest → post + cmd

## câu chốt để nhớ
- post = phong bì
- cmd trong xml = nội dung thư
