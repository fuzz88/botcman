<script>

import { user } from '../stores/AuthStore.ts';

let username = ''
let password = ''

async function getLogged() {
        const user = {'username': username, 'password': password}
        const res = await fetch('http://localhost:8000/auth', {
            method: 'POST',
            body: JSON.stringify(user)
        });

        const data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }


    function handleLoginClick() {
        let promise = getLogged();
        promise.then(result => console.log(result))
        .catch(error => alert('Ошибка авторизации.\n\nПроверьте ваши логин и пароль.'))
    }
</script>


<div class="container">
    <div class="row justify-content-center">
        <div class="login_from__heading сol-sm col-md-5 col-lg-4">
            <h1>Боцман</h1>
            <h5>система управления доставкой</h5>
        </div>
        <div class="col-sm col-md-5 col-lg-4">
            <form class="form">

              <div class="form-group">
                <input bind:value={username} type="text" class="form-control" id="login">
              </div>

              <div class="form-group">
                <input bind:value={password} type="password" class="form-control" id="password">
              </div>

              <button on:click={handleLoginClick} type="submit" class="btn btn-dark">Войти в панель управления</button>

            </form>
            <h1>{$user}</h1>
        </div>
    </div>
</div>

<style>
    @import "../custom";
    @import "../../node_modules/bootstrap/scss/bootstrap";

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
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

    .login_from__heading {
        text-align: center;
    }

</style>