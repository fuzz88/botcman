<script>

import { user } from '../stores/AuthStore.ts';

</script>


<div>
    <h1> Hello, { $user.user.username }! </h1>
</div>

<style>

    @import "../../node_modules/bootstrap/scss/bootstrap";

</style>