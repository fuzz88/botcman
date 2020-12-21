<script>
    import {
        is_striped_tables,
        is_hide_archived,
    } from "../stores/SettingsStore";
</script>

<style>
    ul {
        list-style-type: none;
    }
</style>

<div class="container">
    <dir class="row">
        <div class="col">
            <form>
                <fieldset>
                    <legend>Интерфейс</legend>
                    <ul>
                        <li>
                            <p>
                                <label for="checkbox1">
                                    <input
                                        id="checkbox1"
                                        name="checkbox"
                                        type="checkbox"
                                        bind:checked={$is_striped_tables} />
                                    Контрастные строки в таблицах
                                </label>
                            </p>
                        </li>
                        <li>
                            <p>
                                <label for="checkbox2">
                                    <input
                                        id="checkbox2"
                                        name="checkbox"
                                        type="checkbox"
                                        bind:checked={$is_hide_archived} />
                                    Скрывать архив
                                </label>
                            </p>
                        </li>
                    </ul>
                </fieldset>
            </form>
        </div>
    </dir>
</div>
