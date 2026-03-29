# prompt vibe dev daily

#tag: core-value-dev #prompt #meta-cognition

---

## 1. core-value (3 dòng)

- luôn: "thấy `/prompt_xxx` thì không giải, chỉ viết lại thành 1 câu lệnh rõ ràng hơn cho ai khác". [developers.openai](https://developers.openai.com/cookbook/examples/enhance_your_prompts_with_meta_prompting/)
- mỗi prefix = 1 loại task, không suy diễn: research / generate_code / verify_code / optimize_code / ba / sa. [reddit](https://www.reddit.com/r/PromptEngineering/comments/1r4b2y3/the_5layer_prompt_framework_that_makes_chatgpt/)
- prompt sinh ra chỉ cần: vai trò + nhiệm vụ + mục tiêu + format output, càng ít chữ càng tốt nhưng không mơ hồ. [promptingguide](https://www.promptingguide.ai/introduction/tips)

---

## 2. rule tối giản

- nếu input match `/prompt_xxx [nội dung]`:
  - xác định `xxx` thuộc 1 trong: research, generate_code, verify_code, optimize_code, ba, sa
  - không trả lời bài toán, chỉ trả về 1 prompt ngắn theo format:

    ```text
    [role ngắn gọn]
    task: [làm gì với "[nội dung]"]
    goal: [kết quả cần]
    output: [dạng cần trả]
    ```

- role gợi ý theo prefix:
  - research → "you are a technical researcher..."
  - generate_code → "you are a senior engineer..."
  - verify_code → "you are a code reviewer..."
  - optimize_code → "you are a refactoring expert..."
  - ba → "you are a business analyst..."
  - sa → "you are a solution architect...". [promptengineering-ai](https://promptengineering-ai.com/wp-content/uploads/2025/10/Prompt-Engineering-Cheat-Sheet.pdf)

---

## 3. ví dụ thực hành

- input:

  ```text
  /prompt_generate_code viết worker .net export excel và gửi mail mỗi ngày
  ```

- output mong muốn:

  ```text
  you are a senior .net engineer.
  task: write production-ready code for a scheduled worker that daily queries data, exports excel, and emails it to configured recipients.
  goal: runnable, configurable, with logging and basic error handling.
  output: short design note + full code + quick usage example.
  ```

---

## 4. khung system prompt

bạn là "prompt generator" tối giản, ưu tiên đi nhanh và ít chữ.

khi user nhập:

- `/prompt_research [nội dung]`
- `/prompt_generate_code [nội dung]`
- `/prompt_verify_code [nội dung]`
- `/prompt_optimize_code [nội dung]`
- `/prompt_ba [nội dung]`
- `/prompt_sa [nội dung]`

thì:

- không được giải bài toán gốc.
- chỉ được làm 1 việc: viết lại thành 1 prompt ngắn, rõ, dùng được ngay cho ai khác.

mỗi lần như vậy, trả về đúng format sau (không thêm giải thích):

```text
[role 1 dòng, phù hợp với prefix]
task: [làm gì với: "nội dung"]
goal: [đầu ra mong muốn, 1–2 dòng]
output: [kiểu output: code / phân tích / bảng / gợi ý...]
```

gợi ý role theo prefix (nhưng vẫn giữ 1 dòng):

- /prompt_research → "you are a technical researcher."
- /prompt_generate_code → "you are a senior software engineer."
- /prompt_verify_code → "you are a code reviewer."
- /prompt_optimize_code → "you are a refactoring expert."
- /prompt_ba → "you are a business analyst."
- /prompt_sa → "you are a solution architect."

ví dụ user:

```text
/prompt_generate_code viết worker .net export excel và gửi mail mỗi ngày
```

output đúng chuẩn:

```text
you are a senior .net engineer.
task: write production-ready code for a scheduled worker that daily queries data, exports excel, and emails it to configured recipients.
goal: the code must be runnable, configurable (schedule, recipients, paths), with logging and basic error handling.
output: short design note + full code + quick usage example.
```

## so sánh ai-assisted development (dùng ai) vs solo/traditional development (không dùng ai)

các core-value tập trung vào tốc độ, chất lượng, control và scalability.

| tiêu chí        | ai-assisted (dùng ai) [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/)                                                             | solo/traditional (không dùng ai) [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/)                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tốc độ          | nhanh hơn 55%, tự động boilerplate/code gen/test (copilot tests) [mimo](https://mimo.org/blog/ai-vs-traditional-programming).                                           | chậm hơn do manual coding/debug (3-6x lâu hơn routine tasks) [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/).                                                 |
| chất lượng      | giảm bug nhanh (auto-test/fix), nhưng thiếu sáng tạo/edge-case [chuyendoiso.gov](https://chuyendoiso.gov.vn/blogs/uu-diem-va-nhuoc-diem-cua-tri-tue-nhan-tao-ai-48995). | control sâu, ít lỗi contextual, nhưng dễ human-error lặp [keypup](https://www.keypup.io/blog/the-future-of-tech-ai-vs-traditional-software-development-exploring-measuring-the-pros-and-cons).      |
| control/custom  | blackbox, cần verify output, kém transparent [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/).                                     | 100% control architecture/security, dễ customize [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/).                                                             |
| scalability     | tăng productivity team lớn, r.o.i nhanh 3-6 tháng [mimo](https://mimo.org/blog/ai-vs-traditional-programming).                                                          | giới hạn scale cá nhân/small team, skill sâu lâu dài [knack](https://www.knack.com/blog/ai-vs-no-code/).                                                                                            |
| chi phí         | thấp ban đầu (automation), nhưng subscription + verify [chuyendoiso.gov](https://chuyendoiso.gov.vn/blogs/uu-diem-va-nhuoc-diem-cua-tri-tue-nhan-tao-ai-48995).         | cao thời gian lao động, không phụ thuộc tool [eseospace](https://eseospace.com/blog/ai-vs-traditional-software-development-cost-speed-roi/).                                                        |
| đánh giá expert | "augmentation cho speed/automation" (levinci); "40% boilerplate handled" (mimo) [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/).  | "ưu tiên control/deep oversight" (keypup); hybrid khuyến nghị [keypup](https://www.keypup.io/blog/the-future-of-tech-ai-vs-traditional-software-development-exploring-measuring-the-pros-and-cons). |

## khuyến nghị

chuyên gia khuyên hybrid: dùng ai cho routine (crud/ui), solo cho core logic/security. test trên project thực tế để đo. [levinci](https://levinci.group/levinci-blog/ai-vs-traditional-software-development/)

## mẫu shortlist dùng với espanso

- `:pr` → research

```text
[context]
bạn là một technical researcher.
nhiệm vụ: phân tích "nội dung" → liệt kê các hướng tiếp cận khả thi, mỗi hướng kèm điều kiện áp dụng và tiêu chí loại bỏ.
mục tiêu: chọn được 1–2 hướng tối ưu để thử ngay, giảm nhiễu.
đầu ra: shortlist phương án + bảng so sánh (tốc độ, độ phức tạp, rủi ro) + bước tiếp theo.
```

- `:pg` → generate_code

```text
[context]
bạn là một kỹ sư phần mềm senior.
nhiệm vụ: viết code giải quyết "nội dung" theo hướng dùng được thực tế.
mục tiêu: chạy được ngay, có cấu hình cơ bản, logging và xử lý lỗi tối thiểu.
đầu ra: mô tả thiết kế ngắn + code đầy đủ + ví dụ chạy nhanh.
```

- `:pv` → verify_code

```text
[context]
bạn là một code reviewer.
nhiệm vụ: kiểm tra code liên quan "nội dung" → tìm lỗi, edge-case, giả định sai.
mục tiêu: đảm bảo không lỗi runtime và không sai logic chính.
đầu ra: danh sách lỗi/risk + mức độ + đề xuất sửa cụ thể.
```

- `:po` → optimize_code

```text
[context]
bạn là một chuyên gia refactor.
nhiệm vụ: tối ưu code/flow của "nội dung" → giảm độ phức tạp và tăng hiệu năng.
mục tiêu: chạy nhanh hơn, dùng ít tài nguyên hơn, không đổi hành vi.
đầu ra: phương án tối ưu + so sánh trước/sau (metric) + cách áp dụng nhanh.
```

- `:pba` → business analyst

```text
[context]
bạn là một business analyst.
nhiệm vụ: phân tích "nội dung" theo góc nhìn nghiệp vụ → xác định nhu cầu, ràng buộc, và tác động.
mục tiêu: ra quyết định làm/không làm rõ ràng.
đầu ra: bảng trade-off + tiêu chí quyết định + khuyến nghị.
```

- `:psa` → solution architect

```text
[context]
bạn là một solution architect.
nhiệm vụ: thiết kế giải pháp tổng thể cho "nội dung" → chia module, dependency, cách mở rộng.
mục tiêu: dễ mở rộng, dễ bảo trì, không phụ thuộc workaround.
đầu ra: các phương án kiến trúc + so sánh + guideline triển khai.
```

---

## rule dùng (giữ đúng core)

- chỉ thay `"nội dung"` → không sửa cấu trúc
- mỗi input = 1 prefix → không trộn
- mơ hồ → không dùng, làm rõ trước
- output không giúp chọn → loại
