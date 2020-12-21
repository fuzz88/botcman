<script>
    import { push } from "svelte-spa-router";

    let fullname;
    let experience;
    let stamina;
    let reliability;

    let errors = [];
    let has_error;

    import { newTeamMember } from "../stores/TeamStore";
    import InputValidatorLabelHelper from "./InputValidatorLabelHelper.svelte";

    async function handleNewTeamMemberClick() {
        errors = await newTeamMember(
            fullname,
            reliability,
            stamina,
            experience,
        );
        errors = errors === undefined ? [] : errors;

        if (errors.length == 0) {
            push("/team");
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
    <h4>Новый мувер</h4>
    <dir class="row is-full-screen">
        <div class="col">
            <form>
                <p>
                    <label for="fullname">Ф.И.О.</label>
                    <InputValidatorLabelHelper error={has_error['fullname']} />
                    <input
                        bind:value={fullname}
                        type="text"
                        id="fullname"
                        placeholder="Иванов Иван Иванович" />
                </p>
                <p>
                    <label for="experience">Опыт</label>
                    <InputValidatorLabelHelper
                        error={has_error['experience']} />
                    <input
                        class:has_error={has_error['experience']}
                        bind:value={experience}
                        type="text"
                        id="experience"
                        placeholder="16" />
                </p>
                <p>
                    <label for="stamina">Стамина</label>
                    <InputValidatorLabelHelper error={has_error['stamina']} />
                    <input
                        class:has_error={has_error['stamina']}
                        bind:value={stamina}
                        type="text"
                        id="stamina"
                        placeholder="32" />
                </p>
                <p>
                    <label for="reliability">Надёжность</label>
                    <InputValidatorLabelHelper error={has_error['reliability']} />
                    <input
                        class:has_error={has_error['reliability']}
                        bind:value={reliability}
                        type="text"
                        id="reliability"
                        placeholder="21" />
                </p>
            </form>
            <p class="text-right">
                <button
                    on:click={handleNewTeamMemberClick}
                    class="button outline primary">Сохранить</button>
            </p>
        </div>
    </dir>
</div>
