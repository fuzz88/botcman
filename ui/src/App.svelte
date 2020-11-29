<script>
    document.title = "Боцман -- Dashboard";

    export let user;

    import { unauthorized_user } from "./stores/AuthStore";

    import Router from "svelte-spa-router";
    import { replace } from "svelte-spa-router";
    import { wrap } from "svelte-spa-router/wrap";

    import LoginFormContainer from "./routes/LoginFormContainer.svelte";
    import Dashboard from "./routes/Dashboard.svelte";
    import NotFound from "./routes/NotFound.svelte";


    const routes = {

        "/login": wrap({
            component: LoginFormContainer,
            conditions: [
            (details) => { console.log($user); return $user === unauthorized_user; },
            ],
            userData: {
                redirect: "/"
            },
        }),

        "/": wrap({
            component: Dashboard,
            conditions: [
            (details) => { console.log($user); return $user !== unauthorized_user; },
            ],
            userData: {
                redirect: "/login"
            },
        }),

        "*": NotFound,
    };

    function conditionsFailed(event) {
        replace(event.detail.userData.redirect)

}

</script>

<Router {routes} on:conditionsFailed={conditionsFailed}/>
