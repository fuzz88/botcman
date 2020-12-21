import { writable } from "svelte/store";

const stored__is_striped_tables = localStorage.getItem("is_striped_tables");
const stored__is_hide_archived = localStorage.getItem("is_hide_archived");

export const is_striped_tables = writable(stored__is_striped_tables === "true");

is_striped_tables.subscribe(value => {
    localStorage.setItem("is_striped_tables", value);
});

export const is_hide_archived = writable(stored__is_hide_archived === "true");

is_hide_archived.subscribe(value => {
    localStorage.setItem("is_hide_archived", value);
});