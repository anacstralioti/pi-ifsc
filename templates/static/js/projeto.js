document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os elementos do modal de PROJETO
    const modal = document.getElementById('novoProjetoModal');
    const btn = document.getElementById('novoProjetoBtn');
    const cancelBtn = document.getElementById('cancelNovoProjeto');

    // Garante que os elementos existem antes de adicionar os listeners
    if (btn) {
        btn.addEventListener('click', function(event) {
            event.preventDefault(); // Impede o link de recarregar a página
            modal.classList.remove('hidden');
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.classList.add('hidden');
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });
});