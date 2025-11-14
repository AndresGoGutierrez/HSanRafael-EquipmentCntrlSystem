import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
    vus: 5,
    duration: "10s",
};

// Login with valid user
function loginAdmin() {
    const url = "http://localhost:8000/api/v1/auth/login";

    const payload = "username=usertest&password=userTest123";

    const headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    };

    const res = http.post(url, payload, { headers });

    check(res, {
        "login status is 200": (r) => r.status === 200,
        "token exists": (r) => JSON.parse(r.body).access_token !== undefined,
    });

    return JSON.parse(res.body).access_token;
}

export default function () {
    const token = loginAdmin();

    const registerUrl = "http://localhost:8000/api/v1/auth/register";

    const payload = JSON.stringify({
        username: `user_k6_${__ITER}`,
        email: `user_k6_${__ITER}@example.com`,
        full_name: "Usuario K6",
        password: "12345678",
        role: "administrador",
    });

    const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };

    const res = http.post(registerUrl, payload, { headers });

    console.log(`REGISTER STATUS: ${res.status}`);
    console.log(`BODY: ${res.body}`);

    check(res, {
        "status is 201": (r) => r.status === 201,
    });

    sleep(1);
}