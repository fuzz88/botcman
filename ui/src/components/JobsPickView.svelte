<script>
    import { onMount } from "svelte";
    import { runJob } from "../stores/JobsStore";

    export let params = {};

    onMount(async () => {
        await runJob(params.id);
    });
</script>

<div class="container">
    <dir class="row">
        <div class="col">
            <h1>Набор команды</h1>
            <h3>Заявка отправлена в чат.</h3>
            <p>Здесь будет отображены результаты опроса по заявке.</p>
            <p>
                Можно будет посмотреть статус муверов и бригадира, увидеть
                подтверждения, назначить автозамену.
            </p>
        </div>
    </dir>
</div>
