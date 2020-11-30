<script>
  import { user } from "../stores/AuthStore.ts";
  import { Route } from 'tinro';

  import Navbar from "./Navbar.svelte";

</script>

<Navbar/>

<Route path="/botcman/team">team</Route>
<Route path="/botcman/jobs">jobs</Route>

<style>
</style>


