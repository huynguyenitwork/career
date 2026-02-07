# sơ đồ trao đổi
1. service refagent thực hiện nhiệm vụ sau:
2. inbound from api
3. queue request api và payload
4. schedule gởi request api và payload to rk7
5. outbound to rk7
6. emit/subcriber khi outbound to rk7 được gởi đi

# mô tả
hãy tưởng tượng refagent là **một người điều phối lạnh lùng**: không xử lý nghiệp vụ, không phán đúng sai, chỉ đảm bảo "đúng lúc – đúng thứ tự – đúng nơi".

---

## 1. inbound from api – cửa vào của thế giới hỗn loạn

đây là điểm tiếp xúc đầu tiên.

- api bên ngoài gọi vào refagent
- payload có thể là lệnh, dữ liệu, yêu cầu đồng bộ sang rk7

vai trò của refagent lúc này **không phải xử lý**, mà là:

- validate tối thiểu (đủ shape, đủ key, không rỗng)
- gắn metadata: request_id, source, timestamp
- **ack nhanh** cho client (đừng để client chờ rk7)

tư duy:

> inbound càng nhanh → hệ thống càng ít nghẽn → người gọi càng bớt cáu.

---

## 2. queue request api + payload – đóng băng thời gian

sau khi nhận xong, refagent **không gửi ngay**.

nó làm một việc rất quan trọng:
**đưa request + payload vào queue**.

queue để làm gì?

- tách đời sống api ra khỏi rk7 (rk7 sống chậm, api sống nhanh)
- chống burst (api spam 1000 request thì rk7 không chết)
- cho phép retry, delay, schedule

payload trong queue thường gồm:

- request_id
- endpoint rk7 target
- payload gốc
- trạng thái (pending / scheduled / sent / failed)
- retry_count

queue ở đây là "vùng đệm đạo đức":
ai đến trước chưa chắc được đi trước, nhưng không ai bị mất.

---

## 3. schedule gửi request api + payload to rk7 – nhịp tim của hệ thống

đây là phần **não điều khiển**.

refagent có một scheduler (cron / worker / background service) làm các việc:

- lấy item từ queue theo rule:

  * theo thời gian
  * theo độ ưu tiên
  * theo rate limit rk7 chịu được
- quyết định **khi nào được gửi**, không phải có là gửi

ví dụ:

- mỗi 5s gửi tối đa 10 request
- rk7 lỗi thì pause 1 phút
- ban đêm gửi batch, ban ngày gửi lẻ

tư duy cốt lõi:

> refagent kiểm soát thời gian, không để thời gian kiểm soát mình.

---

## 4. outbound to rk7 – bắn tên lửa

khi scheduler quyết định "giờ đẹp rồi":

- refagent call api rk7
- gắn header trace_id / request_id
- log đầy đủ request + response

kết quả outbound:

- success → update trạng thái queue = sent
- fail → tăng retry_count, quay lại queue hoặc dead-letter

quan trọng:
**outbound này là hành động có rủi ro**, nên phải:

- idempotent (gửi lại không gây double effect)
- có timeout rõ ràng
- có retry policy

---

## 5. emit / subscriber khi outbound to rk7 được gửi đi – hệ thần kinh

đây là phần nhiều team hay bỏ qua, nhưng lại cực kỳ đáng tiền.

sau khi outbound xảy ra (thành công hoặc thất bại):

- refagent **emit event** (ví dụ: rk7.request.sent, rk7.request.failed)
- các service khác subscribe:

  * logging service
  * monitoring
  * notification
  * business workflow

lợi ích:

- refagent không cần biết ai quan tâm
- hệ thống mở rộng mà không sửa refagent
- debug theo event cực đã

nói ngắn gọn:

> refagent làm xong việc thì "lên tiếng", còn ai nghe là chuyện của họ.

---

## 6. bản chất kiến trúc (nếu nói một câu)

refagent không phải service nghiệp vụ.
nó là **anti-corruption layer + traffic controller + event source**.

nếu ví von:

- api client = người gửi thư
- rk7 = quan chức khó tính
- refagent = thư ký riêng, biết lúc nào nên trình hồ sơ

---

## 7. sơ đồ tinh thần (sketch)

```
client api
   ↓
inbound api (ack nhanh)
   ↓
queue (đóng băng + kiểm soát)
   ↓
scheduler (quyết định thời điểm)
   ↓
outbound rk7
   ↓
emit event → subscribers
```
refagent đúng nghĩa là làm cho hệ thống **điềm tĩnh giữa một thế giới hấp tấp**.
---
