import { readable } from "svelte/store";



export const team_members = readable([], function start(set) {
    const interval = setInterval(function () {
        const res = fetch("/api/botcman/team", {
            method: "GET",
            credentials: 'include'
        }).then(result => result.json())
            .then(r => set(r));
    }, 1000);

    return function stop() {
        clearInterval(interval);
    };
});


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
        console.log(data["detail"]);
    };
};