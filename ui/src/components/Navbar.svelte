<script>
  import { logout } from "../stores/AuthStore";
  import { router } from 'tinro';

  function handleLogoutClick() {
    logout();
    router.goto("/botcman/")
  }
</script>

<header>
<nav class="nav bg-dark">
  <div class="nav-left">
    <a href="/botcman/team" class="button button-primary">Команда</a>
    <a href="/botcman/jobs" class="button button-primary">Задания</a>
  </div>
  <div class="nav-center hide-xs">
    <a class="brand">
      <img alt="Боцман @ Коробка" src="img/box.svg"/>
    </a>
  </div>
  <div class="nav-right">
    <a on:click={ handleLogoutClick } class="button button-primary">Выйти</a>
  </div>
</nav>
</header>

<style>
</style>