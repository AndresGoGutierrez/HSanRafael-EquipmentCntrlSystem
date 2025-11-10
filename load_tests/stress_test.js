import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    stages: [
        { duration: "10s", target: 10 },
        { duration: "10s", target: 30 },
        { duration: "10s", target: 50 },
        { duration: "10s", target: 0 },
    ],
};

export default function () {
    let res = http.get("http://localhost:8000/health");

    check(res, {
        "status is 200": (r) => r.status === 200,
    });

    sleep(1);
}