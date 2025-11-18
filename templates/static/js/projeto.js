document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('novoProjetoModal');
    const btn = document.getElementById('novoProjetoBtn');
    const cancelBtn = document.getElementById('cancelNovoProjeto');

    if (btn) {
        btn.addEventListener('click', function(event) {
            event.preventDefault(); 
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

    document.querySelectorAll('.editar-projeto-btn').forEach(button => {
    button.addEventListener('click', function () {
        const modal = document.getElementById('editarProjetoModal');
        const id = this.dataset.id;
        const nome = this.dataset.nome;
        const descricao = this.dataset.descricao;
        const participantes = this.dataset.participantes ? this.dataset.participantes.split(',') : [];

        document.getElementById('editar_projeto_id').value = id;
        document.getElementById('editar_nome_projeto').value = nome;
        document.getElementById('editar_descricao').value = descricao;
        document.getElementById('editarProjetoForm').action = `/produtiva/projetos/editar/${id}/`;

        const select = document.getElementById('editar_participantes');
        Array.from(select.options).forEach(opt => {
        opt.selected = participantes.includes(opt.value);
        });

        modal.classList.remove('hidden');
    });
    });

    document.getElementById('cancelEditarProjeto').addEventListener('click', () => {
    document.getElementById('editarProjetoModal').classList.add('hidden');
    });

    document.querySelectorAll('.delete-project-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Tem certeza que deseja cancelar este projeto?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.concluir-projeto-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Deseja marcar este projeto como concluído?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.restaurar-projeto-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Deseja restaurar este projeto?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.excluir-definitivo-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Tem certeza que deseja excluir este projeto permanentemente? Essa ação não poderá ser desfeita.")) {
                window.location.href = url;
            }
        });
    });

    const messages = document.querySelectorAll('.mb-4.space-y-2 .w-full');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.classList.add('transition-opacity', 'duration-500');
            msg.style.opacity = 0;
            setTimeout(() => msg.remove(), 500); 
        }, 3000); 
    });
});
