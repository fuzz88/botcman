<script>
  import { user } from "../stores/AuthStore.ts";

  import Router from "svelte-spa-router";

  import Navbar from "./Navbar.svelte";

  import MainView from "./MainView.svelte";
  import JobsView from "./JobsView.svelte";
  import TeamView from "./TeamView.svelte";
  import NotFound from "./NotFound.svelte";

  const routes = {

    "/": MainView,

    "/team": TeamView,

    "/jobs": JobsView,

    "*": NotFound,
}

</script>

<Navbar/>

<Router { routes }/>

<style>
</style>


