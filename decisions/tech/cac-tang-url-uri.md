# các tầng url / uri

## tầng 0: định danh
  - uri
    - url
    - urn

- "uri"
  - ví dụ: "mailto:admin@example.com"
  - viết tắt của: "uniform resource identifier"
  - hiểu nhanh: chuỗi để định danh 1 tài nguyên, không chắc gọi được

- "url"
  - ví dụ: "http://localhost:5901/api/users"
  - viết tắt của: "uniform resource locator"
  - hiểu nhanh: uri có vị trí + truy cập được

- "urn"
  - ví dụ: "urn:isbn:9780134685991"
  - viết tắt của: "uniform resource name"
  - hiểu nhanh: uri chỉ tên định danh, không chỉ nơi ở
  
## tầng 1: url tổng thể
  - scheme://authority/path?query#fragment

## tầng 2: authority
  - host:port

## tầng 3: chi tiết
  - scheme → http
  - host → localhost
  - port → 5901
  - path → /
  - query → ?
  - fragment → #

- ví dụ ráp lại
  - http://localhost:5901
    - url
      - scheme: http
      - authority
        - host: localhost
        - port: 5901
