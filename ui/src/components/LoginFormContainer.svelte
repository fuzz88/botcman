<script>

import { getLogged } from "../stores/AuthStore";

let username = ""
let password = ""

function handleLoginClick() {
    getLogged(username, password).then(result => console.log(result))
    .catch(error => alert('Ошибка авторизации.\n\nПроверьте ваши логин и пароль.'))
}

</script>


<div class="container">
    <div class="columns">
        <div class="text-center сol-4 col-mx-auto">
            <h1>Боцман</h1>
            <h5>система управления доставкой</h5>

            <form class="form p-centered">
                <div class="form-group">
                <input bind:value={username}
                    type="text"
                    class="form-input"
                    id="login">
                </div>
                <div class="form-group">
                <input bind:value={password}
                    type="password"
                    class="form-input"
                    id="password">
                </div>
                <button on:click={handleLoginClick}
                    type="submit"
                    class="btn btn-primary">Войти в панель управления
                </button>
            </form>
        </div>
    </div>
</div>

<style>


    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        margin-bottom: 0px;
    }

    h5 {
        color: #ff3e00;
        font-weight: 200;
        font-size: 1.4em;
    }

    form {
        margin-top: 1em;
        max-width: 320px;
    }

</style>