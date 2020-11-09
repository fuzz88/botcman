import {get, writable} from 'svelte/store';

function persist(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export function writablelocal(key, initialValue) {
  const localValue = JSON.parse(localStorage.getItem(key));
  if (!localValue) persist(key, initialValue);

  const store = writable(localValue || initialValue);
  store.subscribe(value => persist(key, value));
  return store;
}