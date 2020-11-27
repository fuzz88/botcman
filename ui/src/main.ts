import App from './App.svelte';
import { user } from './stores/AuthStore';

const app = new App({
	target: document.body,
    props :{
        user: user
    }
});

export default app;