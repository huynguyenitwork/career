# k6 đo api local (latency, error rate, throughput)

## mục tiêu
- đo 3 metric cốt lõi
- chạy local, độc lập business
- chạy ngay bằng bunx / npx

---

## cấu trúc file

k6/

* loadtest.js
* request.json

---

## file request.json
```json
{
  "url": "/api/set-discount-rk7-data",
  "method": "POST",
  "timeout": "3s",
  "headers": {
    "content-type": "application/json",
    "X-Source-Service": "MD"
  },
  "payload": {
    "ActName": "SaveDiscount",
    "CallbackUrl": "http://localhost:5000/api/integration/discount/callback",
    "Payload": {
      "DiscountCondition": {
        "Action": 2,
        "DiscountItem": {
          "genSAPCODE": "200125PSCL",
          "MainParentIdent": null,
          "Name": "Promotion SkyCloud 200125 update",
          "Status": "1"
        },
        "DiscountTypeItem": {
          "genSAPCODE": "18012025",
          "MainParentIdent": null,
          "Name": "[dev] open discount 18012025",
          "Status": "1"
        }
      },
      "JobId": "616e0253-7d11-4e17-88b1-e08cd3c7145e"
    },
    "RequestId": "fb1d7b6d-d63e-48ea-a5c8-a6b9b69ca734"
  }
}
```

---

## script k6 (loadtest.js)

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const errors = new Rate("errors");

const BASE_URL = __ENV.BASE_URL || "http://localhost:2329";
const req = JSON.parse(open("./request.json"));

export const options = {
  vus: 20,
  duration: "1m",
  thresholds: {
    http_req_duration: ["p(95)<500"],
    errors: ["rate<0.01"],
  },
};

export default function () {
  const res = http.request(
    req.method,
    `${BASE_URL}${req.url}`,
    JSON.stringify(req.payload),
    {
      headers: req.headers,
      timeout: req.timeout,
    }
  );

  const ok = check(res, {
    "status 200": (r) => r.status === 200,
  });

  errors.add(!ok);
  sleep(0.2);
}
```

---

## chạy bằng exe

* hành động:

  * `bunx k6.exe run -e BASE_URL=http://localhost:2329 loadtest.js`
* dùng khi:

  * đã có file k8.exe
  * cần startup nhanh

---

## đọc metric để quyết

* latency:

  * `http_req_duration` → p95
* error rate:

  * `errors` hoặc `% checks failed`
* throughput:

  * `http_reqs/s`

---

## quy tắc loại

* p95 vượt ngưỡng → api chưa ổn
* vus tăng mà throughput không tăng → bottleneck
* error tăng theo vus → timeout / tài nguyên

---

## gate cuối

* chạy < 5 phút
* nhìn số là biết làm gì tiếp
* chưa qua local → không bàn grafana

## kịch bản đo metric

### kịch bản 1: api sống
- mục tiêu: kiểm tra endpoint phản hồi
```javascript
export const options = { vus: 5, duration: "10s" };
```

---

### kịch bản 2: latency p95

* mục tiêu: đọc p95 nhanh

```javascript
export const options = { vus: 10, duration: "30s" };
```

---

### kịch bản 3: so version (deterministic)

* mục tiêu: so 2 lần chạy

```javascript
export const options = { vus: 10, iterations: 100 };
```

---

### kịch bản 4: chịu tải nhẹ

* mục tiêu: phát hiện bottleneck

```javascript
export const options = { vus: 20, duration: "1m" };
```

---

### quy tắc chọn

* lỗi cấu hình → kịch bản 1
* nghi chậm → kịch bản 2
* so code → kịch bản 3
* nghi nghẽn → kịch bản 4

```
