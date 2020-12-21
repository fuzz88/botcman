<script>
  import Router from "svelte-spa-router";

  import Navbar from "./Navbar.svelte";

  import MainView from "./MainView.svelte";
  import JobsView from "./JobsView.svelte";
  import TeamView from "./TeamView.svelte";
  import NotFound from "./NotFound.svelte";
  import SettingsView from "./SettingsView.svelte";
  import LogView from "./LogView.svelte";
  import TeamAddFormContainer from "./TeamAddFormContainer.svelte";
  import TeamEditFormContainer from "./TeamEditFormContainer.svelte";
  import JobsAddFormContainer from "./JobsAddFormContainer.svelte";
  import JobsEditFormContainer from "./JobsEditFormContainer.svelte";
import JobsPickView from "./JobsPickView.svelte";

  const routes = {
    "/": MainView,

    "/team": TeamView,

    "/team/add": TeamAddFormContainer,

    "/team/edit": TeamEditFormContainer,

    "/jobs": JobsView,

    "/jobs/add": JobsAddFormContainer,

    "/jobs/edit/:id": JobsEditFormContainer,

    "/jobs/pick/:id": JobsPickView,

    "/logs": LogView,

    "/settings": SettingsView,

    "*": NotFound,
  };
</script>

<style>
</style>

<Navbar />

<Router {routes} />
