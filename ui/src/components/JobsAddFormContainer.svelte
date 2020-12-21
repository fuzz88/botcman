<script>
    import { push } from "svelte-spa-router";

    let ext_id;
    let manager;
    let status;
    let chat_message;
    let courier_message;
    let mover_message;
    let brigadier_message;

    let errors = [];
    let has_error;

    import { newJob, managers } from "../stores/JobsStore";
    import InputValidatorLabelHelper from "./InputValidatorLabelHelper.svelte";

    async function handleNewJobClick() {
        errors = await newJob(
            ext_id,
            manager,
            status,
            chat_message,
            courier_message,
            brigadier_message,
            mover_message
        );
        errors = errors === undefined ? [] : errors;

        if (errors.length == 0) {
            push("/jobs");
        }
    }

    $: {
        has_error = [];
        errors.forEach((error) => (has_error[error["loc"][1]] = error["msg"]));
    }
</script>

<style>
</style>

<div class="container">
    <h4>Новая заявка</h4>
    <dir class="row is-full-screen">
        <div class="col">
            <form>
                <p>
                    <label for="ext_id">Номер</label>
                    <InputValidatorLabelHelper error={has_error['ext_id']} />
                    <input id="ext_id" bind:value={ext_id} type="text" />
                </p>
                <p>
                    <label
                        class:bg-error={has_error['manager']}
                        for="manager">Исполнитель</label>
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
                    on:click={handleNewJobClick}
                    class="button outline primary">Сохранить</button>
            </p>
        </div>
    </dir>
</div>
