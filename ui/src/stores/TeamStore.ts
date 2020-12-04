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
        experience: parseInt(experience),
        stamina: parseInt(stamina),
        activity: parseInt(activity)
    }

    const res = await fetch("/api/botcman/team/add", {
        method: "POST",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_member)
    });
};