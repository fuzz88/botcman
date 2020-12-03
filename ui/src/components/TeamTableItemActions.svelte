<script>
    import { link } from "svelte-spa-router";
    import copy from "copy-text-to-clipboard";
    import Fa from "svelte-fa";
    import {
        faHandsHelping,
        faTrash,
        faPen,
    } from "@fortawesome/free-solid-svg-icons";

    function handleShowCodeClick() {
        copy("10983513");
        alert("Код для регистрации скопирован в буфер обмена.");
    }
</script>

<style>
    .actions {
        display: flex;
        justify-content: space-evenly;
    }
</style>

<div class="actions">
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handleShowCodeClick}>
        <Fa size="1.25x" icon={faHandsHelping} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a href="/team/edit" use:link><Fa size="1.25x" icon={faPen} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a><Fa size="1.25x" icon={faTrash} /></a>
</div>
