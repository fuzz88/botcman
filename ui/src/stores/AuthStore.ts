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

const unauthorized_user = { username: "unknown", role: "unauthorized" };

export const user = derived(auth_cookie,
    $auth_cookie => $auth_cookie ? jwt_decode($auth_cookie)["user"] : unauthorized_user
);