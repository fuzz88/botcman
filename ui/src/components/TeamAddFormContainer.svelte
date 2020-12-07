<script>
    import { push } from "svelte-spa-router";
    
    let fullname;
    let experience;
    let stamina;
    let activity;

    let errors = [];
    let has_error;

    import { newTeamMember } from "../stores/TeamStore";

    async function handleNewTeamMemberClick () {
        errors = await newTeamMember(fullname, experience, stamina, activity);
        errors = errors === undefined ? [] : errors;
        
        if (errors.length == 0) {
            push("/team");
        }

    }

    $: {
        has_error = []
        errors.forEach(error => has_error[error["loc"][1]] = error["msg"])
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
                    <label class:bg-error={has_error["fullname"]} for="fullname">Ф.И.О.</label>
                    <small>{has_error["fullname"] === undefined ? "" : has_error["fullname"]}</small>
                    <input
                        bind:value={fullname}
                        type="text"
                        id="fullname"
                        placeholder="Иванов Иван Иванович" />
                </p>
                <p>
                    <label class:bg-error={has_error["experience"]} for="experience">Опыт</label>
                    <small>{has_error["experience"] === undefined ? "" : has_error["experience"]}</small>
                    <input
                        class:has_error={has_error["experience"]}
                        bind:value={experience}
                        type="text"
                        id="exprerience"
                        placeholder="16" />
                </p>
                <p>
                    <label class:bg-error={has_error["stamina"]} for="stamina">Стамина</label>
                    <small>{has_error["stamina"] === undefined ? "" : has_error["stamina"]}</small>
                    <input
                        class:has_error={has_error["stamina"]}
                        bind:value={stamina}
                        type="text"
                        id="stamina"
                        placeholder="32" />
                </p>
                <p>
                    <label class:bg-error={has_error["activity"]} for="activity">Активность</label>
                    <small>{has_error["activity"] === undefined ? "" : has_error["activity"]}</small>
                    <input
                        class:has_error={has_error["activity"]}
                        bind:value={activity}
                        type="text"
                        id="activity"
                        placeholder="21" />
                </p>
            </form>
            <p class="text-right">
                <button on:click={handleNewTeamMemberClick} class="button outline primary">Сохранить</button>
            </p>
        </div>
    </dir>
</div>
