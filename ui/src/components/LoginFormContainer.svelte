<script>

import { getLogged } from "../stores/AuthStore";

let username = ""
let password = ""

function handleLoginClick(event) {
    event.preventDefault();
    getLogged(username, password).then()
    .catch(error => alert('Ошибка авторизации.\n\nПроверьте ваши логин и пароль.'));
}

</script>


<div class="container">
    <div class="row">
        <div class="col-3 col-4-xs col-4-md col-4-lg"></div>
        <div class="col-6 col-4-xs col-4-md col-4-lg text-center">
            <h1>Боцман</h1>
            <h5>система управления перевозками</h5>
            <form>
                    <p>
                    <input bind:value={username}
                        type="text"
                        class="form-input"
                        id="login">
                    </p>
                    <p>
                    <input bind:value={password}
                        type="password"
                        class="form-input"
                        id="password">
                    </p>
                    <p>
                    <button on:click={handleLoginClick}
                        type="submit"
                        class="btn btn-primary">Войти в панель управления
                    </button>
                    </p>
            </form>
        </div>
        <div class="col-3 col-4-xs col-4-md col-4-lg"></div>
    </div>
</div>


<style>


    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        margin-bottom: -5px;
    }

    h5 {
        color: #ff3e00;
        font-weight: 200;
        font-size: 1em;
        margin-top: 0px;
        margin-bottom: 25px;
    }

</style>