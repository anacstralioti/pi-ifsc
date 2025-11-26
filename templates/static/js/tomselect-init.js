document.addEventListener('DOMContentLoaded', function () {

    const editarSelect = document.querySelector('#editar_participantes');

    if (editarSelect) {

        if (editarSelect.tomselect) {
            editarSelect.tomselect.destroy();
        }

        editarSelect.innerHTML = editarSelect.innerHTML;

        new TomSelect(editarSelect, {
            plugins: ['remove_button'],
            persist: false,
            create: false,
            placeholder: 'Selecione participantes...',
        });
    }

});
