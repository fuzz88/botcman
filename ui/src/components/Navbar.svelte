<script>
  import { logout } from "../stores/AuthStore"

  function handleLogoutClick() {
    logout();
  }
</script>

<header>
<nav class="nav bg-dark">
  <div class="nav-left">
    <a href="..." class="button button-primary">Команда</a>
    <a href="..." class="button button-primary">Задания</a>
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