<script>
  import { logout } from "../stores/AuthStore";
  import { link } from "svelte-spa-router";
  import active from "svelte-spa-router/active";

  function handleLogoutClick() {
    logout();
  }
</script>

<header>
<nav class="nav bg-dark">
  <div class="nav-left">
    <a href="/team" class="button primary" use:link use:active={{className:"bd-success"}}>Команда</a>
    <a href="/jobs" class="button primary" use:link use:active={{className:"bd-success"}}>Задания</a>
  </div>
  <div class="nav-center hide-xs">
    <a href="/" class="brand" use:link>
      <img alt="Боцман @ Коробка" src="img/box.svg"/>
    </a>
  </div>
  <div class="nav-right">
    <a on:click={ handleLogoutClick } class="button primary">Выйти</a>
  </div>
</nav>
</header>

<style>

</style>