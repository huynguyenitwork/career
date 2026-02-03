import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const errors = new Rate("errors");

const BASE_URL = __ENV.BASE_URL || "http://localhost:2329";
const req = JSON.parse(open("./request.json"));

export const options = {
    vus: 10,
    duration: "15s",
    gracefulStop: "0s",
    thresholds: {
        http_req_duration: ["p(95)<500"],
        errors: ["rate<0.05"],
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