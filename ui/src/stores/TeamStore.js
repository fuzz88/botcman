import { derived, readable } from "svelte/store";


export const wss_event_trigger = readable({ event: { name: null } }, function start(set) {
    set({ event: { name: "team_members_update" } });
    var socket = new WebSocket("wss://gaps-apps.ru:443/api/botcman/events");
    
    socket.onmessage = function (event) {
        set(JSON.parse(event.data));
    };

    return function stop () {
        socket.close();
    }
});


export const team_members = derived(wss_event_trigger, ($wss_event_trigger, set) => {
    if ($wss_event_trigger.event.name == "team_members_update") {
        fetch("https://gaps-apps.ru/api/botcman/team/list", {
            method: "GET",
            credentials: 'include'
        }).then(result => result.json())
            .then(r => set(r));
    };
    return () => {};
}, []);


export async function newTeamMember(fullname, reliability, stamina, experience) {

    const new_member = {
        fullname: fullname,
        reliability: reliability,
        stamina: stamina,
        experience: experience,
    }

    const resp = await fetch("https://gaps-apps.ru/api/botcman/team/add", {
        method: "POST",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_member)
    })

    if (resp.status == 422) {
        const data = await resp.json();
        return data["detail"];
    };
};


export async function archiveTeamMember(id) {

    const resp = await fetch("https://gaps-apps.ru/api/botcman/team/archive/" + id, {
        method: "DELETE",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (resp.status == 422) {
        const data = await resp.json();
    };
};