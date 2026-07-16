## thị trường mua bán ứng viên

question:
==làm thế nào để cv gốc của tôi luôn matching được với nhiều nhà tuyển dụng, khiến họ hứng thú liên hệ và sẵn sàng trả mức lương cao hơn?==
outcome:

- hiểu bản chất của việc "matching" giữa ứng viên và nhà tuyển dụng.
- có một cv gốc (master cv) chứa toàn bộ năng lực.
- từ cv gốc có thể sinh nhiều cv mục tiêu chỉ trong vài phút.
- tăng xác suất được gọi phỏng vấn.
- tăng khả năng đàm phán lương.
  mechanisms:

| mechanism           | use when                            | +                           | -                        | signals                                      |
| ------------------- | ----------------------------------- | --------------------------- | ------------------------ | -------------------------------------------- |
| value proposition   | muốn biết mình đang bán gì          | tập trung vào giá trị       | khó viết lúc đầu         | recruiter hiểu ngay bạn giải quyết vấn đề gì |
| buyer persona       | mỗi công ty khác nhau               | matching cao                | phải nghiên cứu jd       | jd khác nhau sẽ đổi trọng tâm                |
| keyword matching    | ats hoặc hr lọc cv                  | tăng tỉ lệ qua vòng đầu     | không đủ để đậu kỹ thuật | jd chứa nhiều keyword trùng cv               |
| evidence matching   | cần tạo niềm tin                    | rất thuyết phục             | cần dự án thật           | mọi keyword đều có ví dụ                     |
| pain → solution     | muốn "bán hàng" thay vì "kể chuyện" | recruiter thấy đúng nhu cầu | phải hiểu business       | cv trả lời đúng vấn đề công ty đang tuyển    |
| signal optimization | muốn nổi bật trong 10 giây          | đọc rất nhanh               | phải cắt nội dung thừa   | mắt luôn dừng ở các điểm quan trọng          |

links:

- chưa có

## bài toán 1: cô đọng thành ý chính

question:
==**một ứng viên có đủ năng lực để doanh nghiệp tuyển dụng và đồng hành lâu dài hay không?**==
outcome:

- đánh giá được toàn diện ứng viên thay vì chỉ dựa trên kỹ năng kỹ thuật.
- giảm rủi ro tuyển sai người.
- tìm được người vừa giải quyết được công việc, vừa hòa hợp với tổ chức.
  mechanisms:

| mechanism                                   | use when                                 | +                                         | -                                 | signals                              |
| ------------------------------------------- | ---------------------------------------- | ----------------------------------------- | --------------------------------- | ------------------------------------ |
| technical competency (năng lực kỹ thuật)    | cần biết ứng viên có làm được việc không | đánh giá năng lực chuyên môn              | không phản ánh cách làm việc      | kinh nghiệm, dự án, công nghệ        |
| business competency (năng lực nghiệp vụ)    | công việc phụ thuộc nhiều vào domain     | hiểu nghiệp vụ, giảm thời gian onboarding | cần trải nghiệm thực tế           | hiểu business, biết trade-off        |
| behavioral competency (năng lực hành vi)    | cần đánh giá cách làm việc               | dự đoán cách ứng xử                       | khó đánh giá trong thời gian ngắn | ownership, feedback, learning        |
| collaboration competency (năng lực hợp tác) | làm việc theo team                       | giảm xung đột, tăng hiệu quả              | phụ thuộc môi trường              | giao tiếp rõ ràng, phối hợp ba/qa/pm |
| culture fit (phù hợp với văn hóa)           | cần làm việc lâu dài                     | tăng khả năng gắn bó                      | dễ mang tính chủ quan             | phù hợp giá trị công ty              |
| growth potential (tiềm năng tăng trưởng)    | tuyển senior hoặc leader                 | đầu tư dài hạn                            | khó đo chính xác                  | học nhanh, thích nghi, cải tiến      |

links:

- competency model
- behavioral interview

## bài toán 2: hiểu cơ chế vận hành trước modeling

question:

- **doanh nghiệp thực sự đánh giá ứng viên bằng cơ chế nào trước khi xây dựng mô hình tuyển dụng?**
  domain:
- tuyển dụng nhân sự.
  identity:
- xác định mức độ phù hợp giữa **con người** và **tổ chức**.
  value:

  | entity                              | attributes                                                                                        |
  | ----------------------------------- | ------------------------------------------------------------------------------------------------- |
  | candidate (ứng viên)                | skill, behavior, experience, motivation, value (kỹ năng, hành vi, kinh nghiệm, động lực, giá trị) |
  | recruiter (nhà tuyển dụng)          | evaluation, expectation (đánh giá, kỳ vọng)                                                       |
  | hiring manager (quản lý tuyển dụng) | technical assessment (đánh giá kỹ thuật)                                                          |
  | team                                | collaboration style (phong cách hợp tác)                                                          |
  | company                             | culture, mission, process (văn hóa, sứ mệnh, quy trình)                                           |
  | job                                 | responsibility, requirement (trách nhiệm, yêu cầu)                                                |

  relation:
  | source | relation | target |
  | -------------- | ----------------- | --------- |
  | candidate | applies to | job |
  | recruiter | screens | candidate |
  | hiring manager | interviews | candidate |
  | candidate | collaborates with | team |
  | team | belongs to | company |
  | company | defines | culture |

  collection:

  | entity           | cardinality |
  | ---------------- | ----------- |
  | company → team   | 1..n        |
  | team → candidate | n..n        |
  | job → candidate  | 1..n        |

  behavior:
  function:

  | function             | input           | output          |
  | -------------------- | --------------- | --------------- |
  | resume screening     | cv              | interview       |
  | technical interview  | skill           | technical score |
  | behavioral interview | behavior        | culture score   |
  | hiring decision      | all evaluations | offer / reject  |

  rule:
  | rule | condition | result |
  | --------------------------------- | -------------------- | ---------------- |
  | thiếu năng lực kỹ thuật | technical score thấp | reject |
  | kỹ thuật tốt nhưng không hợp team | behavior thấp | reject hoặc hold |
  | đủ cả năng lực và văn hóa | đạt ngưỡng | hire |

  state:
  | entity | states |
  | --------- | ------------------------------------------------- |
  | candidate | applied → screening → interview → offer → onboard |

  event:
  | event | trigger | effect |
  | --------- | ------------- | ------------ |
  | apply | gửi cv | tạo hồ sơ |
  | interview | recruiter mời | đánh giá |
  | offer | đạt yêu cầu | thương lượng |
  | reject | không đạt | kết thúc |

  time:
  | concept | description |
  | ---------- | ----------- |
  | screening | vài phút |
  | interview | 1–3 vòng |
  | probation | 2–3 tháng |
  | employment | 2–5 năm |

  constraint:
  | constraint | reason |
  | ---------------------------- | ---------------------- |
  | thời gian phỏng vấn ngắn | thông tin hạn chế |
  | thông tin từ cv không đầy đủ | cần xác minh |
  | chi phí tuyển sai cao | ảnh hưởng toàn bộ team |

  structure:
  composition:
  | whole | part |
  | ----------- | ---------- |
  | recruitment | screening |
  | recruitment | interview |
  | recruitment | hiring |
  | recruitment | onboarding |
  abstraction:

- **tuyển dụng là bài toán dự đoán xác suất hợp tác thành công trong tương lai dựa trên lượng thông tin rất hạn chế.**
  quality:
- accuracy
- fairness
- predictability

  complexity:
  | aspect | complexity |
  | -------------- | ---------- |
  | technical | medium |
  | human behavior | high |
  | culture | very high |

  implementation:

- **cv** → mô tả knowledge, skill.
- **interview** → xác minh behavior.
- **assessment** → đo problem solving.
- **reference check** → xác minh trust.
- **onboarding** → kiểm chứng mô hình dự đoán.

  verification:

- tỷ lệ pass probation.
- retention sau 1 năm.
- performance review.

  feedback:

- cập nhật jd.
- cập nhật competency framework.
- cải tiến câu hỏi phỏng vấn.

  links:

- [[competency framework]]
- [[recruitment lifecycle]]

## bài toán 3: hiểu các giai đoạn làm việc cùng nhau 2–5 năm

question:
**làm thế nào để doanh nghiệp và nhân viên có thể hợp tác hiệu quả và bền vững trong nhiều năm?**
problem space:

- tuyển đúng người chỉ là điểm bắt đầu.
- giá trị thật nằm ở khả năng cùng phát triển lâu dài.

  context:

- nhân sự thay đổi.
- công nghệ thay đổi.
- business thay đổi.
- tổ chức mở rộng.
  nếu không làm:
- turnover cao.
- onboarding liên tục.
- mất tri thức.
- giảm năng suất.

  goals:

- tạo niềm tin.
- phát triển năng lực.
- giữ người phù hợp.
- tăng hiệu suất dài hạn.

  constraints:

- thời gian.
- ngân sách.
- thay đổi business.
- giới hạn con người.

  forces:
  | force | current | trend | impact |
  | ------------ | ------------------- | ------------ | ------------------- |
  | scale | tăng | tăng | cần chuẩn hóa |
  | latency | phản hồi chậm | giảm | cần giao tiếp nhanh |
  | throughput | nhiều dự án | tăng | cần phối hợp |
  | consistency | không đồng đều | tăng | cần quy trình |
  | availability | nhân sự nghỉ việc | luôn tồn tại | cần backup |
  | cost | tuyển mới cao | tăng | giữ người tốt |
  | complexity | domain tăng | tăng | học liên tục |
  | team | thay đổi thành viên | liên tục | cần trust |

  design space:
  | strategy | mechanism | use when | + | - | signals |
  | --------------------- | ------------------- | ------------------- | ------------------ | --------------- | ------------------ |
  | onboarding | truyền đạt domain | nhân viên mới | hòa nhập nhanh | tốn mentor | hiểu business |
  | coaching | feedback định kỳ | phát triển năng lực | cải thiện liên tục | tốn thời gian | tiến bộ rõ |
  | ownership | giao trách nhiệm | senior | tăng trust | áp lực | chủ động |
  | career path | lộ trình phát triển | giữ người | gắn bó lâu | cần đầu tư | mục tiêu rõ |
  | continuous learning | học và chia sẻ | công nghệ thay đổi | thích nghi | chi phí đào tạo | cập nhật kiến thức |
  | culture reinforcement | thực hành giá trị | toàn công ty | thống nhất hành vi | khó đo | hành vi nhất quán |

  decision:
  selected:

- **xây dựng quan hệ dựa trên trust + growth + shared value.**
  why:
- kỹ năng sẽ thay đổi theo thời gian.
- niềm tin và khả năng hợp tác quyết định hiệu quả dài hạn.

  rejected:
  | mechanism | reason |
  | --------------------- | ------------------------------- |
  | chỉ đánh giá kpi | bỏ qua hành vi |
  | chỉ đánh giá kỹ thuật | không phản ánh khả năng hợp tác |
  | chỉ đánh giá văn hóa | thiếu năng lực thực thi |

  verification:
  | metric | target |
  | ------------------ | ------------------ |
  | pass probation | >95% |
  | retention 2 years | cao |
  | performance review | đạt kỳ vọng |
  | team satisfaction | tích cực |
  | promotion rate | tăng theo năng lực |

  links:

- [[employee lifecycle]]
- [[organizational trust]]

## nguyên lý chung

ba bài toán này thực chất là ba mức nhìn của cùng một hệ thống:
| bài toán | mục tiêu |
| ------------------------- | --------------------------------------------------------------- |
| **1. competency** | tuyển đúng người |
| **2. recruitment model** | hiểu cơ chế đánh giá để tuyển đúng |
| **3. employee lifecycle** | tạo điều kiện để hai bên hợp tác và phát triển bền vững 2–5 năm |

chúng tạo thành một chuỗi liên tục:

```text
competency
      ↓
recruitment
      ↓
onboarding
      ↓
collaboration
      ↓
trust
      ↓
growth
      ↓
long-term partnership
```

đây là baseline có thể áp dụng không chỉ cho tuyển dụng mà còn cho nhiều bài toán hợp tác dài hạn khác như đối tác kinh doanh, khách hàng chiến lược hay xây dựng cộng đồng.
