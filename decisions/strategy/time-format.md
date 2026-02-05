# time format

## mục tiêu

- chọn đúng time format → giảm lỗi parse, timezone, đồng bộ hệ thống
- ưu tiên format giúp api, db, log chạy ổn định 7-30 ngày
- loại bỏ format gây mơ hồ hoặc phụ thuộc locale

---

## nguyên tắc chọn

- nếu cần trao đổi dữ liệu giữa hệ thống → dùng "iso 8601 / rfc 3339"
- nếu cần tính toán nhanh hoặc lưu trữ nội bộ → dùng "unix timestamp"
- nếu cần hiển thị cho người dùng → convert sang "locale format"
- nếu làm distributed system → bổ sung "logical clock"
- nếu làm scheduling theo quốc gia → bắt buộc lưu timezone kèm timestamp

---

## timeline tiến hóa + quyết định áp dụng

### bảng tiến hóa các loại time

| giai đoạn   | loại time                  | cách biểu diễn                         | xã hội cần giải quyết         | ví dụ minh họa                | quyết định áp dụng hiện tại                       |
| ----------- | -------------------------- | -------------------------------------- | ----------------------------- | ----------------------------- | ------------------------------------------------- |
| cổ đại      | solar time                 | ngày / tháng / năm theo mặt trời       | xác định mùa vụ nông nghiệp   | lịch gregorian                | chỉ dùng cho hiển thị lịch                        |
| cổ đại      | lunar time                 | chu kỳ trăng                           | nghi lễ, văn hóa              | âm lịch, lịch hijri           | chỉ dùng business domain đặc thù                  |
| trung đại   | sundial / local solar hour | giờ theo bóng mặt trời từng địa phương | sinh hoạt dân cư              | mỗi thành phố 1 giờ khác nhau | loại khỏi hệ thống số                             |
| trung đại   | 12h clock                  | "hh:mm am/pm"                          | dễ đọc cho con người          | `03:30 pm`                    | chỉ dùng ui                                       |
| trung đại   | 24h clock                  | "hh:mm"                                | giảm nhầm sáng/chiều          | `15:30`                       | ui và scheduling nội bộ                           |
| công nghiệp | timezone time              | local time + offset                    | đồng bộ tàu hỏa, viễn thông   | `2026-02-05 15:30 utc+7`      | bắt buộc lưu offset khi business phụ thuộc địa lý |
| khoa học    | utc time                   | thời gian chuẩn nguyên tử              | đồng bộ hệ thống toàn cầu     | `2026-02-05t08:30:00z`        | chuẩn backend mặc định                            |
| máy tính    | epoch time                 | số giây từ 1970                        | tối ưu tính toán và lưu trữ   | `1738734600`                  | storage, queue, cache                             |
| internet    | iso 8601                   | datetime chuẩn chuỗi                   | tránh lỗi parse cross system  | `2026-02-05t15:30:00+07:00`   | chuẩn log, api phổ biến                           |
| internet    | **rfc 3339**               | iso 8601 dạng ràng buộc                | giảm ambiguity parser         | `2026-02-05t15:30:00+07:00`   | chuẩn api khuyến nghị                             |
| distributed | lamport time               | counter logic                          | xác định thứ tự event         | `event_a=5 → event_b=6`       | dùng event sourcing / microservice                |
| distributed | vector clock               | nhiều counter node                     | causal consistency multi node | `[node1=3,node2=5]`           | chỉ dùng multi region phức tạp                    |
| hiện đại    | monotonic time             | counter tăng liên tục                  | đo duration chính xác         | `process.elapsed=120ms`       | dùng performance measurement                      |
| hiện đại    | hybrid logical clock       | utc + logical counter                  | giảm sai lệch clock vật lý    | `timestamp + logical counter` | dùng distributed db                               |

---

### lịch thiên văn (solar / lunar calendar)

- mục đích: tổ chức xã hội, nông nghiệp, tôn giáo
- giá trị cho dev: gần như = 0
- quyết định: loại khỏi thiết kế hệ thống

---

### 12h / 24h clock

- mục đích: chuẩn hóa sinh hoạt con người
- payoff: tăng readability cho ui
- rủi ro: 12h dễ nhầm am/pm
- quyết định:
  - hiển thị ui → cho phép dùng
  - lưu trữ / api → cấm dùng

---

### timezone (1884)

- mục đích: đồng bộ giao thông, thương mại toàn cầu
- payoff: đảm bảo event đúng vùng địa lý
- rủi ro: daylight saving, lệch offset
- quyết định:
  - luôn lưu "utc" + "timezone offset"
  - không lưu local time đơn lẻ

---

### utc (1960s)

- mục đích: chuẩn thời gian vật lý toàn cầu
- payoff: chuẩn đồng bộ mọi hệ thống
- quyết định:
  - tất cả timestamp backend phải normalize về utc
  - cấm lưu local server time

---

### unix timestamp (1970)

- format:
  - số giây / millisecond từ epoch
- payoff:
  - so sánh nhanh
  - index db tốt
  - serialize nhẹ
- tradeoff:
  - khó đọc
  - dễ sai timezone khi convert
- quyết định:
  - dùng cho:
    - cache
    - queue
    - job scheduler
    - internal storage
  - không expose trực tiếp cho api public

---

### iso 8601 (1988)

- format chuẩn:
  - "yyyy-mm-ddthh:mm:ssz"
- payoff:
  - parse ổn định cross-language
  - human readable
  - chuẩn api industry
- quyết định:
  - mặc định cho:
    - rest api
    - log system
    - message broker payload

---

### rfc 3339

- mục đích: subset chặt chẽ của iso 8601 cho internet
- payoff:
  - giảm ambiguity parser
- quyết định:
  - nếu design api mới → ưu tiên rfc 3339
  - nếu hệ thống legacy → iso 8601 vẫn chấp nhận

---

### logical clock (lamport / vector)

- mục đích: xác định thứ tự event distributed
- payoff:
  - tránh race condition
  - đảm bảo causal consistency
- quyết định:
  - dùng khi:
    - microservice
    - event sourcing
    - multi region system
  - loại nếu hệ thống single database

---

## rule thiết kế hệ thống

- backend:
  - lưu trữ = unix timestamp hoặc utc datetime
- api:
  - input/output = rfc 3339
- database:
  - index = numeric timestamp nếu cần performance
- log:
  - iso 8601 + timezone
- ui:
  - convert theo locale user
- queue / worker:
  - dùng timestamp numeric để so sánh nhanh

---

## anti-pattern cần loại sớm

- lưu datetime không timezone
- lưu string date dạng "dd/mm/yyyy"
- dùng server local time
- convert timezone nhiều tầng service
- expose unix timestamp cho client

---

## checklist trước khi commit design

- timestamp có normalize utc chưa
- payload api có timezone chưa
- format có parse ổn cross-language chưa
- storage có index theo time chưa
- có khả năng xảy ra race condition chưa xử lý chưa

---

## default recommendation

- storage: "unix timestamp (ms)"
- api: "rfc 3339"
- log: "iso 8601 utc"
- distributed event: "lamport timestamp nếu cần"