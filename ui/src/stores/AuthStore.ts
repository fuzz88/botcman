import { readable } from 'svelte/store';
import jwt_decode from "jwt-decode";
import Cookies from 'js-cookie';


export const user = readable(null, function start(set) { 

    const cookie = Cookies.get('token');
    
    if (cookie) {
        set(jwt_decode(cookie));
    } else {
        set(null);
    }

    return function stop() {
    };
});