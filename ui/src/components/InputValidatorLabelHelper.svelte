<script>
    export let error;
</script>

<style>
    .error {
        background-color: firebrick;
        color: floralwhite;
    }
</style>

<small
    class:error={error !== undefined}>{error === undefined ? '' : error}</small>
