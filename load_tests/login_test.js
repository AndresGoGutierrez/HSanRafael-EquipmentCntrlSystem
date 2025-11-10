import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 1,
    duration: '5s',
};

export default function () {
    const url = 'http://localhost:8000/api/v1/auth/login';

    const payload = {
        username: 'usertest',
        password: 'userTest123'
    };

    const params = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    };

    let res = http.post(url, payload, params);

    console.log("STATUS:", res.status);
    console.log("BODY:", res.body);

    check(res, {
        'status is 200': (r) => r.status === 200,
        'token exists': (r) => r.json('access_token') !== undefined
    });

    sleep(1);
}
