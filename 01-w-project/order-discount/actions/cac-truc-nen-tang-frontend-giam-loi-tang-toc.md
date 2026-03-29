# các trục nền tảng frontend (giảm lỗi + tăng tốc)

#tag: #frontend #corepack #dependency #code-consistency #type-safety #state-logic #build-run #testing #ui-system #workflow

---

## 1. môi trường chạy (environment)

- mục tiêu: mọi máy chạy giống nhau

- hành động:
  - bật corepack:
    - `corepack enable`

  - lock version:

    ```json
    "packageManager": "pnpm@8.x"
    ```

  - tạo `.nvmrc`:

    ```
    18
    ```

- loại:
  - không lock node
  - mỗi máy 1 pnpm version

---

## 2. dependency (build ổn định)

- mục tiêu: install deterministic

- hành động:
  - `pnpm install`
  - commit:
    - `pnpm-lock.yaml`

- rule:
  - sau `git pull` → luôn `pnpm install`

- loại:
  - nhiều package manager
  - xoá lockfile

---

## 3. code consistency

- mục tiêu: giảm conflict + dễ đọc

- hành động:
  - cài:
    - `eslint`
    - `prettier`

  - bật auto format on save

- loại:
  - format tay
  - mỗi người 1 style

---

## 4. type safety

- mục tiêu: fail sớm

- hành động:
  - dùng `typescript`

- loại:
  - js thuần (project dài hạn)

---

## 5. state & logic

- mục tiêu: không tự build lại

- hành động:
  - form → `react-hook-form`
  - server → react-query
  - url → `nuqs`

- loại:
  - tự viết state/form

---

## 6. ui system

- mục tiêu: tăng tốc ui

- hành động:
  - dùng `shadcn`
  - dùng design system chung

- loại:
  - custom từng component

---

## 7. build & run

- mục tiêu: config ít, chạy nhanh

- hành động:
  - dùng `vite` hoặc `next`

- loại:
  - webpack custom

---

## 8. testing

- mục tiêu: tránh regression

- hành động:
  - `vitest`
  - chạy:
    - `pnpm test`

- loại:
  - không test (project dài hạn)

---

## 9. workflow

- mục tiêu: hệ không drift

- hành động:
  - không mix tool
  - luôn install sau pull
  - commit lockfile

- loại:
  - “máy tôi chạy”

---

# bảng tổng kết trục

| trục             | mục tiêu             | hành động chính         | tiêu chí loại         |
| ---------------- | -------------------- | ----------------------- | --------------------- |
| environment      | đồng nhất môi trường | corepack + `.nvmrc`     | không lock version    |
| dependency       | build ổn định        | pnpm + lockfile         | nhiều tool / xoá lock |
| code consistency | giảm conflict        | eslint + prettier       | format tay            |
| type safety      | giảm bug runtime     | typescript              | js thuần              |
| state & logic    | không reinvent       | react-hook-form / query | tự viết               |
| ui system        | tăng tốc ui          | shadcn                  | custom rời rạc        |
| build            | chạy nhanh           | vite / next             | webpack custom        |
| testing          | tránh regression     | vitest                  | không test            |
| workflow         | giữ ổn định          | install + commit lock   | drift môi trường      |

---

## kết luận

- bắt buộc:
  - environment + dependency + typescript

- đủ tốt:
  - thêm lint + ui + state

→ làm đúng các trục → giảm phần lớn lỗi frontend
→ không cần tự giải lại các bài toán đã có lời giải
