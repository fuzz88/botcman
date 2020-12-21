<script>
    import { push } from "svelte-spa-router";
    import { onMount } from "svelte";

    export let params = {};

    let manager;
    let ext_id;
    let chat_message;
    let courier_message;
    let mover_message;
    let brigadier_message;
    let status;

    let errors = [];
    let has_error;

    import { getJob, editJob, managers } from "../stores/JobsStore";
    import InputValidatorLabelHelper from "./InputValidatorLabelHelper.svelte";

    async function handleEditJobClick() {
        errors = await editJob(
            params.id,
            ext_id,
            manager,
            status,
            chat_message,
            brigadier_message,
            mover_message,
            courier_message
        );
        errors = errors === undefined ? [] : errors;

        if (errors.length == 0) {
            push("/jobs");
        }
    }

    onMount(async () => {
        let data = await getJob(params.id);
        ext_id = data["ext_id"];
        manager = data["manager"];
        status = data["status"];
        chat_message = data["chat_message"];
        courier_message = data["courier_message"];
        mover_message = data["mover_message"];
        brigadier_message = data["brigadier_message"];
    });

    $: {
        has_error = [];
        errors.forEach((error) => (has_error[error["loc"][1]] = error["msg"]));
    }
</script>

<style>
</style>

<div class="container">
    <h4>Изменить данные</h4>
    <dir class="row is-full-screen">
        <div class="col">
            <form>
                <p>
                    <label for="ext_id">Номер</label>
                    <InputValidatorLabelHelper error={has_error['ext_id']} />
                    <input id="ext_id" bind:value={ext_id} type="text" />
                </p>
                <p>
                    <label for="manager">Исполнитель</label>
                    <InputValidatorLabelHelper error={has_error['manager']} />
                    <select id="manager" bind:value={manager}>
                        {#each managers().sort() as manager}
                            <option value={manager}>{manager}</option>
                        {/each}
                    </select>
                </p>
                <p>
                    <label
                        class:bg-error={has_error['status']}
                        for="status">Статус</label>
                    <InputValidatorLabelHelper error={has_error['status']} />
                    <select id="status" bind:value={status}>
                        <option value="новая">новая</option>
                        <option value="завершена">завершена</option>
                        <option value="в архиве">в архиве</option>
                        <option value="опрос чата">опрос чата</option>
                    </select>
                </p>
                <p>
                    <label
                        class:bg-error={has_error['chat_message']}
                        for="chat_message">Задание в чат</label>
                    <InputValidatorLabelHelper
                        error={has_error['chat_message']} />
                    <textarea
                        rows="20"
                        class:has_error={has_error['chat_message']}
                        bind:value={chat_message}
                        id="chat_message" />
                </p>
                <p>
                    <label
                        class:bg-error={has_error['brigadier_message']}
                        for="brigadier_message">Бригадиру в лc</label>
                    <InputValidatorLabelHelper
                        error={has_error['brigadier_message']} />
                    <textarea
                        rows="20"
                        class:has_error={has_error['brigadier_message']}
                        bind:value={brigadier_message}
                        id="brigadier_message" />
                </p>
                <p>
                    <label
                        class:bg-error={has_error['mover_message']}
                        for="mover_message">Муверу в лc</label>
                    <InputValidatorLabelHelper
                        error={has_error['mover_message']} />
                    <textarea
                        rows="20"
                        class:has_error={has_error['mover_message']}
                        bind:value={mover_message}
                        id="mover_message" />
                </p>
                <p>
                    <label
                        class:bg-error={has_error['courier_message']}
                        for="courier_message">Курьеру в лc</label>
                    <InputValidatorLabelHelper
                        error={has_error['courier_message']} />
                    <textarea
                        rows="20"
                        class:has_error={has_error['courier_message']}
                        bind:value={courier_message}
                        id="courier_message" />
                </p>
            </form>
            <p class="text-right">
                <button
                    on:click={handleEditJobClick}
                    class="button outline primary">Сохранить</button>
            </p>
        </div>
    </dir>
</div>
