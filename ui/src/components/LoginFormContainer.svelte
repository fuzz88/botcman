<script>

let username = ''
let password = ''

async function getLogged() {
        const user = {'username': username, 'password': password}
        const res = await fetch('/api/botcman/auth', {
            method: 'POST',
            mode: 'same-origin', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (res.ok) {
            return res;
        } else {
            throw new Error(data);
        }
    }


    function handleLoginClick() {
        getLogged().then(result => console.log(result))
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
        </div>
    </div>
</div>

<style>


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