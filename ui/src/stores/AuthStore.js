import { readable, derived } from "svelte/store";
import jwt_decode from "jwt-decode";
import Cookies from "js-cookie";


const auth_cookie = readable(Cookies.get("token"), function start(set) {
    const interval = setInterval(function () {
        set(Cookies.get("token"));
    }, 100);

    return function stop() {
        clearInterval(interval);
    };
});

export const unauthorized_user = { username: "unknown", role: "unauthorized" };

export const user = derived(auth_cookie,
    $auth_cookie => $auth_cookie ? jwt_decode($auth_cookie)["user"] : unauthorized_user
);

export async function getLogged(username, password) {
        const user = {'username': username, 'password': password}
        const res = await fetch('https://gaps-apps.ru/api/botcman/auth', {
            method: 'POST',
            credentials: 'include', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (res.ok) {
            return res;
        } else {
            throw new Error(res.toString());
        }
    }

export function logout() {
    Cookies.remove('token');
}