document.addEventListener('DOMContentLoaded', function() {

  // Novo Projeto
  const novoSelect = document.querySelector('#participantesSelect');
  if (novoSelect) {
    new TomSelect(novoSelect, {
      plugins: ['remove_button'],
      persist: false,
      create: false,
      placeholder: 'Selecione participantes...',
      render: {
        option: function(data, escape) {
          return `<div class="py-1 px-2">${escape(data.text)}</div>`;
        },
        item: function(data, escape) {
          return `<div class="bg-indigo-100 text-indigo-800 rounded px-2 py-0.5 mr-1 mb-1">${escape(data.text)}</div>`;
        }
      }
    });
  }

  // Editar Projeto
  const editarSelect = document.querySelector('#editar_participantes');
  if (editarSelect) {
    // Evita duplicação se o Tom Select já estiver ativo
    if (editarSelect.tomselect) {
      editarSelect.tomselect.destroy();
    }

    new TomSelect(editarSelect, {
      plugins: ['remove_button'],
      persist: false,
      create: false,
      placeholder: 'Selecione participantes...',
      render: {
        option: function(data, escape) {
          return `<div class="py-1 px-2">${escape(data.text)}</div>`;
        },
        item: function(data, escape) {
          return `<div class="bg-indigo-100 text-indigo-800 rounded px-2 py-0.5 mr-1 mb-1">${escape(data.text)}</div>`;
        }
      }
    });
  }

});
