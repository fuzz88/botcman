import { derived, readable } from "svelte/store";


export const wss_event_trigger = readable({ event: { name: null } }, function start(set) {
    set({ event: { name: "jobs_update" } });
    var socket = new WebSocket("wss://gaps-apps.ru:443/api/botcman/events");
    
    socket.onmessage = function (event) {
        set(JSON.parse(event.data));
    };

    return function stop () {
        socket.close();
    }
});


export const jobs = derived(wss_event_trigger, ($wss_event_trigger, set) => {
    if ($wss_event_trigger.event.name == "jobs_update") {
        fetch("https://gaps-apps.ru/api/botcman/jobs/list", {
            method: "GET",
            credentials: 'include'
        }).then(result => result.json())
            .then(r => set(r));
    };
    return () => {};
}, []);

export const managers = function () {
    return ['Стародубцев', 'Чупрова', 'Миронова']
}

export async function newJob(ext_id, manager, status, chat_message, courier_message, brigadier_message, mover_message) {
    const new_job = {
        ext_id: ext_id,
        manager: manager,
        status: status,
        chat_message: chat_message,
        brigadier_message: brigadier_message,
        courier_message: courier_message,
        mover_message: mover_message,
    }

    const resp = await fetch("https://gaps-apps.ru/api/botcman/jobs/add", {
        method: "POST",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_job)
    })

    if (resp.status == 422) {
        const data = await resp.json();
        return data["detail"];
    };
}

export async function getJob(id) {

    const resp = await fetch("https://gaps-apps.ru/api/botcman/jobs/get/" + id, {
        method: "GET",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (resp.status == 200) {
        return await resp.json();
    };

}

export async function archiveJob(id) {

    const resp = await fetch("https://gaps-apps.ru/api/botcman/jobs/archive/" + id, {
        method: "DELETE",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (resp.status == 422) {
        const data = await resp.json();
        // WTF? Why 422?
    };

}

export async function editJob(id, ext_id, manager, status, chat_message, brigadier_message, mover_message, courier_message) {
    const new_job = {
        ext_id: ext_id,
        manager: manager,
        status: status,
        chat_message: chat_message,
        brigadier_message: brigadier_message,
        courier_message: courier_message,
        mover_message: mover_message,
    }

    const resp = await fetch("https://gaps-apps.ru/api/botcman/jobs/edit/"+id, {
        method: "POST",
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_job)
    })

    if (resp.status == 422) {
        const data = await resp.json();
        return data["detail"];
    };

}

export async function runJob(id) {
    const resp = await fetch("https://gaps-apps.ru/api/botcman/jobs/run/" + id, {
        method: "GET",
        credentials: 'include',
    })
}