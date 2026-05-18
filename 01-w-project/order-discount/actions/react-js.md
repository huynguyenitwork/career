#tag: #react #react19 #state #rendering #data-flow #architecture

## mục tiêu

- bám **thuật ngữ chính thức React** → không tự đặt tên
- dùng để **ra quyết định code ngay**
- chọn **1–2 hướng đủ tốt → thử ngay**

---

## 1. core value (react → danh từ hoá từ docs)

- **"component model" (component-based architecture)**
  - bản chất: ui = tree component
  - dùng để: chia nhỏ + tái sử dụng

- **"rendering model" (react rendering)**
  - bản chất: render → reconcile → commit
  - dùng để: hiểu khi nào re-render

- **"state & lifecycle" (state management)**
  - bản chất: `useState`, `useReducer`, lifecycle hooks
  - dùng để: quản lý dữ liệu local

- **"data flow" (unidirectional data flow)**
  - bản chất: props down, events up
  - dùng để: kiểm soát luồng dữ liệu

- **"side effects" (effects)**
  - bản chất: `useEffect`, `useLayoutEffect`
  - dùng để: sync với external system

- **"concurrent features" (concurrent rendering)**
  - bản chất: `useTransition`, `Suspense`
  - dùng để: control UX khi render nặng

---

## 2. mapping core value → quyết định

- **component model**
  - reuse ≥2 lần → tách component
  - chỉ dùng 1 nơi → inline

- **rendering model**
  - re-render nhiều → memo / split
  - không cần tối ưu → giữ đơn giản

- **state**
  - state local → `useState`
  - state phức tạp → `useReducer`
  - cross component → lift state / context

- **data flow**
  - sâu >3 level → context
  - shallow → props

- **side effects**
  - sync external (api, dom) → `useEffect`
  - không external → không dùng effect

- **concurrent**
  - UI block >100ms → `useTransition`
  - loading async → `Suspense`

---

## 3. hướng tiếp cận khả thi (shortlist)

### hướng A — "react thuần + tối giản state"

- cách làm:
  - server (next) fetch → pass props xuống
  - client chỉ giữ state UI nhỏ
  - không global state lib

- áp dụng khi:
  - app CRUD / dashboard vừa
  - data không share phức tạp

- loại khi:
  - state cross-page nhiều
  - cần cache client phức tạp

---

### hướng B — "react + server state (tanstack query)"

- cách làm:
  - server fetch initial
  - client dùng query để cache/refetch

- áp dụng khi:
  - data thay đổi thường xuyên
  - cần retry / cache / sync background

- loại khi:
  - data mostly static
  - chỉ read 1 lần

---

### hướng C — "react + global state (zustand/redux)"

- cách làm:
  - store global cho state dùng chung

- áp dụng khi:
  - state shared nhiều (auth, cart…)

- loại khi:
  - chỉ local state
  - overkill (80% case)

---

## 4. bảng so sánh (chọn nhanh)

| hướng            | tốc độ dev | độ phức tạp | rủi ro           |
| ---------------- | ---------- | ----------- | ---------------- |
| A (thuần)        | nhanh nhất | thấp        | thiếu scale      |
| B (server state) | trung bình | trung bình  | thêm abstraction |
| C (global state) | chậm       | cao         | over-engineer    |

---

## 5. loại sớm (anti-pattern)

- dùng `useEffect` để fetch khi đã có server → **loại**
- global state cho mọi thứ → **loại**
- prop drilling sâu nhưng không dùng context → **loại**
- tối ưu sớm (`memo` mọi nơi) → **loại**

---

## 6. chọn hướng (decision nhanh)

- default:
  - chọn **A (react thuần)**

- nếu gặp:
  - data stale / refetch → nâng cấp **B**

- chỉ khi:
  - state shared phức tạp → thêm **C**

---

## 7. bước tiếp theo (làm ngay)

- tạo 1 feature:
  - server fetch → pass props
  - client component chỉ giữ state UI

- check:
  - có dùng `useEffect` fetch không → **xoá**
  - có state global không cần thiết → **xoá**

- nếu thiếu:
  - thêm `tanstack query` cho 1 endpoint duy nhất → test

---

## 8. chốt

- react = **6 trục quyết định**
  - component
  - rendering
  - state
  - data flow
  - effects
  - concurrent

→ mỗi code phải map vào ≥1 trục
→ không map được → xoá
