<script>
    import { link } from "svelte-spa-router";
    
    let fullname;
    let experience;
    let stamina;
    let activity;

    import { newTeamMember } from "../stores/TeamStore";

    async function handleNewTeamMemberClick () {
        await newTeamMember(fullname, experience, stamina, activity);

    }
</script>

<div class="container">
    <h4>Новый мувер</h4>
    <dir class="row is-full-screen">
        <div class="col">
            <form>
                <p>
                    <label for="fullname">Ф.И.О.</label>
                    <input
                        bind:value={fullname}
                        type="text"
                        id="fullname"
                        placeholder="Иванов Иван Иванович" />
                </p>
                <p>
                    <label for="experience">Опыт</label>
                    <input
                        bind:value={experience}
                        type="text"
                        id="exprerience"
                        placeholder="16" />
                </p>
                <p>
                    <label for="stamina">Стамина</label>
                    <input
                        bind:value={stamina}
                        type="text"
                        id="stamina"
                        placeholder="32" />
                </p>
                <p>
                    <label for="activity">Активность</label>
                    <input
                        bind:value={activity}
                        type="text"
                        id="activity"
                        placeholder="21" />
                </p>
            </form>
            <p class="text-right">
                <a href="/team" on:click={handleNewTeamMemberClick} use:link class="button outline primary">Сохранить</a>
            </p>
        </div>
    </dir>
</div>
