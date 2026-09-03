# quy trình tạo gởi cv

## quy trình

1. tóm tắt thông tin <jd>
2. kiểm tra sơ lược công ty làm lĩnh vực gì, lịch sử hình thành, review trải nghiệm của nhân sự, khách hàng <công ty>
3. xác định điểm nghẽn thực của công ty <công ty> dựa trên jd (giới hạn 4)
4. xác định mức độ tương hợp dựa trên ranh giới và giới hạn <ranh giới + giới hạn>
5. kiểm tra mức tương hợp >= 60% tạo mail cover letter {dựa trên jd, cv, matching và cấu trúc mail} (nếu thỏa mãn)
6. chuyển tiếp quy trình

## mẫu

# ranh giới và giới hạn

- **ranh giới (định tính):**
  - cho phép **backend(.net core, python,...), level mid-senior, product company, business complexity, integration, architecture, reliability, enterprise domain, khoảng cách di chuyển từ huỳnh bá chánh tới công ty <= 20km**;
  - không cho phép **outsourcing company, fullstack đa vai trò, kiêm frontend/devops/pm, lệch khỏi chuyên môn backend**.
- **giới hạn (định lượng):**
  - tối thiểu **>=35m, ≥70% skill match, 50 nhân sự, 3 năm hoạt động, doanh thu tăng >10%, biên lợi nhuận >15%, dòng tiền dương**;
  - tối đa **<=20km, <40m, 300 nhân sự, 12 năm hoạt động, ≤2 lần jd đăng lại/quý, ≤10% giảm lương, nợ ngắn hạn/tài sản ngắn hạn ≤1,5**.

# bộ lọc tiêu chí chọn

## van điều tiết

| ưu tiên | nhóm điều kiện         | tiêu chí                                                                                                                                                                              |
| ------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **p1**  | **skill backend**      | backend .net/python level mid-senior, business complexity, integration, architecture, reliability, enterprise domain; **không outsourcing company, fullstack/kiêm quá nhiều vai trò** |
| **p2**  | **lương**              | **≥35m**, ưu tiên 35–40m; loại nếu **<35m**                                                                                                                                           |
| **p3**  | **quy mô**             | **50–300 nhân sự**                                                                                                                                                                    |
| **p4**  | **vị trí**             | **sài gòn, ưu tiên <=20km từ huỳnh bá chánh**                                                                                                                                         |
| **p5**  | **tuổi + tài chính**   | 3–12 năm; doanh thu >10%; margin >15%; cash flow dương; nợ ngắn hạn/tài sản ngắn hạn ≤1,5                                                                                             |
| **p6**  | **hành vi tuyển dụng** | jd đăng lại ≤2 lần/quý; giảm lương ≤10%                                                                                                                                               |

- p1–p4 = whitelist chính.
- p5 = bộ lọc chất lượng.
- p6 = bộ lọc rủi ro tuyển dụng.
- phương án chọn: skill 40% + lương 20% + vị trí 15% + quy mô 10% + tuổi/tài chính 10% + hành vi tuyển dụng 5%

## kho dự trữ

product

|   # | công ty                | p1 backend | p2 ≥35m | p3 50–300 | p4 ≤20km | p5  | p6  | kết luận    |
| --: | ---------------------- | ---------- | ------- | --------- | -------- | --- | --- | ----------- |
|   1 | **AnyWork**            | **đạt**    | **đạt** | ?         | **đạt**  | ?   | ?   | **a**       |
|   2 | **Arobid**             | **đạt**    | **đạt** | **đạt**   | **đạt**  | ?   | ?   | **a**       |
|   3 | **Anfin**              | **đạt**    | **đạt** | ?         | **đạt**  | ?   | ?   | **a**       |
|   4 | **INS Enco**           | **đạt**    | **đạt** | ?         | ?        | ?   | ?   | **a−**      |
|   5 | **Simpson Strong-Tie** | **đạt**    | ?       | ?         | **đạt**  | ?   | ?   | **a−**      |
|   6 | **L4 Studio**          | **đạt**    | **đạt** | ?/đạt     | **đạt**  | ?   | ?   | **loại p1** |
|   7 | **Larion**             | **đạt**    | ?       | ?         | **đạt**  | bỏ  | ?   | **loại p5** |
|   8 | **InApps Technology**  | trung lập  | ?       | đạt       | **đạt**  | ?   | ?   | **b**       |
|   9 | **Relia Software**     | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  10 | **Groove Technology**  | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  11 | **PalTech**            | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  12 | **Designveloper**      | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  13 | **Techbase Vietnam**   | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  14 | **HDWEBSOFT**          | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |
|  15 | **EZTEK**              | đạt        | ?       | ?         | **đạt**  | ?   | ?   | **b**       |

thứ tự: arobid → anfin → simpson strong-tie vietnam → ins enco → anywork → relia software → groove technology → paltech → designveloper → techbase vietnam → hdwebsoft → eztek → inapps technology

product-outsource

|   # | công ty                        | p1          | p2      | p3                    | p4          | nhận định |
| --: | ------------------------------ | ----------- | ------- | --------------------- | ----------- | --------- |
|   1 | **l4 studio**                  | **rất cao** | **đạt** | **đạt/ cần xác minh** | **đạt**     | **a+**    |
|   2 | **larion**                     | **rất cao** | ?       | **đạt**               | **đạt**     | **a+**    |
|   3 | **sstech**                     | **rất cao** | ?       | **không đạt**         | **đạt**     | b         |
|   4 | **arobid**                     | **rất cao** | **đạt** | **đạt**               | **đạt**     | **a**     |
|   5 | **groove technology**          | cao         | ?       | ?                     | đạt         | a         |
|   6 | **relia software**             | cao         | ?       | ?                     | đạt         | a         |
|   7 | **paltech**                    | cao         | ?       | ?                     | đạt         | a         |
|   8 | **designveloper**              | cao         | ?       | ?                     | đạt         | a         |
|   9 | **techbase vietnam**           | cao         | ?       | ?                     | đạt         | b         |
|  10 | **hdwebsoft**                  | cao         | ?       | ?                     | đạt         | a         |
|  11 | **eztek software development** | cao         | ?       | ?                     | đạt         | a         |
|  12 | **mti technology**             | cao         | ?       | ?                     | đạt         | a         |
|  13 | **weaver software**            | khá/cao     | ?       | ?                     | đạt         | a         |
|  14 | **sde digital technology**     | khá/cao     | ?       | ?                     | **rất gần** | a         |
|  15 | **simpson strong-tie vietnam** | **cao**     | ?       | ?                     | đạt         | a         |

thứ tự: l4 → larion → arobid → groove → relia → paltech → designveloper → hdwebsoft → eztek → mti → weaver → sde → simpson → techbase → sstech.

# công cụ hỗ trợ tìm việc

- ranh giới: chỉ tìm và sàng lọc jd ưu tiên mid/senior backend/it tại hcm trên 5 kênh; không mở rộng sang nền tảng khác trừ khi cần kiểm tra thông tin công ty.
- giới hạn: tìm và sàng lọc jd 5 kênh tuyển dụng **itviec → linkedin → topdev → vietnamworks → topcv**; không vượt ngoài kênh này

# mail cover letter
yêu cầu:
đóng vai một đối tác giải pháp (**solution partner**), không phải người xin việc. giọng văn tự tin, trực diện, hãy đặt người đọc vào một bầu không khí có chiều sâu bằng cách đan xen những câu dài mô tả bối cảnh với câu ngắn tạo điểm nhấn. sử dụng danh từ cụ thể và động từ mạnh làm bộ khung cốt lõi, đồng thời khéo léo giữ lại những tính từ, trạng từ thực sự đắt giá để khơi gợi cảm xúc. tuyệt đối lọc bỏ từ đệm thừa thãi. viết dứt khoát, chân thực và cuốn hút với kết thư mở, kết nối năng lực kỹ thuật với mục tiêu kinh doanh.
kết quả cần là có thể call to action
outcome:
1. góc nhìn doanh nghiệp vs. ứng viên
* **doanh nghiệp cần:** giải pháp cho nỗi đau nghiệp vụ, cam kết đồng hành dài hạn, niềm tin vào năng lực thực thi.
* **ứng viên cần:** khẳng định giá trị kỹ thuật, minh chứng sự am hiểu bài toán công ty, chế độ đãi ngộ tương xứng.
2. điểm chạm chung & call to action (cta)
* **mục đích chung:** thiết lập quan hệ đối tác kinh doanh — đổi năng lực giải quyết vấn đề lấy ngân sách và không gian phát triển.
* **cơ chế cta:** đề xuất một buổi thảo luận kỹ thuật trực tiếp để chứng minh phương án xử lý bài toán của doanh nghiệp.
3. cấu trúc cover letter tối giản (chuẩn 2 chiều)
ranh giới và giới hạn:
- mạch thư cần: điểm chạm → năng lực → hiểu vấn đề → đề nghị hợp tác
- nội dung giới hạn (tối ưu): 180–250 chữ 
cấu trúc thư:
> **mở đầu:** tuyên bố vị trí ứng tuyển + khẳng định sự am hiểu về bài toán nghiệp vụ hiện tại của công ty.
> **thân bài:**
> * **giải quyết vấn đề:** chứng minh năng lực xử lý bài toán tương tự qua con số/kết quả thực tế.
> * **cam kết giá trị:** định hướng gắn bó thông qua việc tối ưu hệ thống dài hạn.
> **kỳ vọng & cta:**
> * **mức thù lao:** thỏa thuận dựa trên phạm vi đóng góp (mục tiêu 35–40m).
> * **hành động:** đề xuất lịch trao đổi kỹ thuật giải quyết bài toán của công ty.

mẫu thư tổng quát:
Kính gửi anh/chị [Tên người tuyển dụng],

Tôi biết đến vị trí **Mid–Senior Backend / Business Complexity Engineer** của công ty qua [LinkedIn/ITViec]. Tôithấy vị trí khá phù hợp với kinh nghiệm của mình, đặc biệt ở các bài toán backend, nghiệp vụ phức tạp và tích hợp nhiều hệ thống.

Tôi có hơn 6 năm phát triển hệ thống doanh nghiệp, chủ yếu tập trung vào việc biến các quy trình nghiệp vụ thành hệ thống rõ ràng, ổn định và dễ vận hành:

* **Business logic:** Thiết kế Promotion Engine, workflow ERP/POS/Tài chính và validation dữ liệu.
* **System integration:** Xây dựng luồng POS ↔ SAP ↔ E-Commerce, xử lý Retry, Idempotency và Fallback.
* **Reliability:** Thiết lập Monitoring, Tracing và Auto-healing; góp phần giảm khoảng 40% thời gian xử lý sự cố Production.

Tôi kỳ vọng mức thu nhập **35–40 triệu VND/tháng**, có thể trao đổi thêm dựa trên phạm vi công việc và trách nhiệm thực tế.

Nếu anh/chị thấy phù hợp, em rất mong có dịp trao đổi thêm về vị trí và các bài toán hệ thống mà team đang gặp phải.

Trân trọng,

**Nguyễn Phú Huy**
Senior Software Engineer | Business Complexity Specialist
SĐT: (+84) 353.072.938
Email: [huy.nguyen.it.work@gmail.com](mailto:huy.nguyen.it.work@gmail.com)
LinkedIn: linkedin.com/in/nguyen-phu-huy-580180250
