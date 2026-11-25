import http from "k6/http";
import { check, sleep } from "k6";

const target = __ENV.TARGET_URL || "http://127.0.0.1:8000/health";
if (!/^http:\/\/(?:127\.0\.0\.1|\[::1\])(?::[0-9]{1,5})?\/[a-zA-Z0-9_./-]*$/.test(target)) {
  throw new Error("TARGET_URL must be a loopback HTTP endpoint without credentials");
}

const profiles = {
  load: { executor: "constant-vus", vus: 2, duration: "5s" },
  stress: {
    executor: "ramping-vus",
    startVUs: 1,
    stages: [{ target: 4, duration: "5s" }, { target: 8, duration: "5s" }, { target: 0, duration: "3s" }],
  },
  spike: {
    executor: "ramping-vus",
    startVUs: 1,
    stages: [{ target: 8, duration: "1s" }, { target: 8, duration: "3s" }, { target: 1, duration: "1s" }],
  },
};
const profile = __ENV.LOAD_PROFILE || "load";
if (!Object.hasOwn(profiles, profile)) {
  throw new Error("LOAD_PROFILE must be load, stress, or spike");
}

export const options = {
  scenarios: { health: { ...profiles[profile], gracefulStop: "2s" } },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<250"],
    checks: ["rate>0.99"],
  },
  maxRedirects: 0,
};

export default function () {
  const response = http.get(target, { timeout: "2s" });
  check(response, { "health returns 200": (result) => result.status === 200 });
  if (profile !== "load") sleep(0.1);
}
