#tag: #nextjs #react #server-components #rendering #routing #data-fetching #caching #architecture
## mục tiêu
- core value **không tự đặt tên** → bám đúng từ hệ sinh thái Next.js / Vercel
- dùng để **ra quyết định code ngay**, không mơ hồ
## 1. core value (chuẩn theo tài liệu chính thức → danh từ hoá)
> gốc từ docs: “rendering strategies”, “server components”, “file-system routing”, “data fetching”, “caching”, “optimizations”
- **"chiến lược kết xuất" (rendering strategies)**
  - bản chất: SSG / SSR / ISR / CSR / streaming
  - dùng để: chọn cách build + serve html
- **"thành phần phía máy chủ" (server components)**
  - bản chất: React Server Components (RSC)
  - dùng để: chạy logic + fetch ở server
- **"định tuyến hệ thống tệp" (file-system routing)**
  - bản chất: folder = route
  - dùng để: tổ chức url
- **"truy xuất dữ liệu" (data fetching)**
  - bản chất: fetch tại server (default)
  - dùng để: quyết định data đi đâu
- **"cơ chế bộ nhớ đệm" (caching)**
  - bản chất: cache + revalidate + no-store
  - dùng để: kiểm soát freshness vs performance
- **"tối ưu hoá tích hợp" (built-in optimizations)**
  - bản chất: image, font, bundling, code-split
  - dùng để: giảm effort tối ưu thủ công
## 2. mapping core value → quyết định
- **chiến lược kết xuất**
  - seo / landing → SSG / ISR
  - dashboard realtime → SSR / no-store
  - không rõ → SSR + revalidate
- **thành phần phía máy chủ**
  - default: server component
  - có state / event → chuyển client
- **định tuyến hệ thống tệp**
  - feature = `/app/<feature>/page.tsx`
  - dynamic = `[id]`
- **truy xuất dữ liệu**
  - read → fetch trong server component
  - write → API route
- **cơ chế bộ nhớ đệm**
  - data ổn định → `revalidate`
  - data realtime → `no-store`
- **tối ưu hoá tích hợp**
  - image → `next/image`
  - font → `next/font`
  - không custom nếu chưa cần
## 3. kiến trúc dòng chảy (gốc → thân)
```id="flow-root"
request
→ routing (file-system)
→ rendering strategy quyết định
→ server component chạy
→ data fetching
→ caching apply
→ html stream về client
→ client component hydrate (nếu có)
```
## 4. cấu trúc chuẩn (thân → nhánh)
```id="structure-final"
/app
  layout.tsx
  page.tsx
  /blog
    page.tsx
    [slug]/page.tsx
    loading.tsx
    error.tsx
    components/
/api
/components
/lib
/public
```
## 5. rule triển khai (rút trực tiếp từ core value)
- không ghi rõ render strategy → **lỗi**
- không kiểm soát cache → **lỗi**
- fetch ở client khi không cần → **lỗi**
- dùng API route cho read → **lỗi**
- `"use client"` không lý do → **lỗi**
## 6. flow làm feature (chuẩn)
- tạo route folder `/app/x`
- viết `page.tsx` (server component)
- chọn **render strategy**
- fetch data
- set **cache**
- tách component:
  - server: render
  - client: interaction
- thêm `loading.tsx`
- chỉ thêm API nếu có write
## 7. checklist review (dùng ngay)
- render strategy đã chọn chưa?
- cache đã explicit chưa?
- có client component dư không?
- data fetch đúng layer chưa?
- route có đúng file-system không?
## 8. loại sớm (anti-pattern)
- SPA mindset (useEffect fetch) → loại
- all-in API route → loại
- không set cache → loại
- client component tràn lan → loại
## 9. chốt
- nextjs = **6 trục quyết định**
  - rendering
  - server component
  - routing
  - data
  - cache
  - optimization
→ mỗi code viết ra phải map vào ≥1 trục
→ không map được → xoá / viết lại
