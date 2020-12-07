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
        const res = fetch("/api/botcman/team", {
            method: "GET",
            credentials: 'include'
        }).then(result => result.json())
            .then(r => set(r));
    };
    return () => {};
}, []);


export async function newTeamMember(fullname, experience, stamina, activity) {

    const new_member = {
        fullname: fullname,
        experience: experience,
        stamina: stamina,
        activity: activity,
    }

    const resp = await fetch("/api/botcman/team/add", {
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


export async function deleteTeamMember(id) {

    const resp = await fetch("/api/botcman/team/delete/" + id, {
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