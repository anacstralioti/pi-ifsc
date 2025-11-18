document.addEventListener('DOMContentLoaded', function() {

    const modal = document.getElementById('novoTarefaModal');
    const cancelBtn = document.getElementById('cancelNovaTarefa');
    const modalTitle = document.getElementById('modalTitle');
    const modalSubmitBtn = document.getElementById('modalSubmitBtn');
    const novaTarefaBtn = document.getElementById('novaTarefaBtn');

    if (novaTarefaBtn) {
        novaTarefaBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modalTitle.textContent = "Adicionar Tarefa ao Projeto";
            modalSubmitBtn.textContent = "Criar Tarefa";

            document.getElementById('tarefa_id').value = "";
            document.getElementById('nome_tarefa').value = "";
            document.getElementById('descricao').value = "";
            document.getElementById('estimativa_horas').value = ""; 
            document.getElementById('categoria').value = "";

            modal.classList.remove('hidden');
        });
    }

    document.querySelectorAll('.editar-tarefa').forEach(button => {
        button.addEventListener('click', function() {
            modalTitle.textContent = "Editar Tarefa";
            modalSubmitBtn.textContent = "Salvar Alterações";

            document.getElementById('tarefa_id').value = this.dataset.id;
            document.getElementById('nome_tarefa').value = this.dataset.nome;
            document.getElementById('descricao').value = this.dataset.descricao;
            document.getElementById('estimativa_horas').value = this.dataset.estimativa;
            document.getElementById('categoria').value = this.dataset.categoria;

            modal.classList.remove('hidden');
        });
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.classList.add('hidden');
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) modal.classList.add('hidden');
    });


    document.querySelectorAll('.concluir-tarefa-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Deseja marcar esta tarefa como concluída?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.cancelar-tarefa-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Tem certeza que deseja cancelar esta tarefa?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.restaurar-tarefa-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Deseja restaurar esta tarefa?")) {
                window.location.href = url;
            }
        });
    });

    document.querySelectorAll('.excluir-tarefa-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Tem certeza que deseja excluir esta tarefa permanentemente?")) {
                window.location.href = url;
            }
        });
    });

    const messages = document.querySelectorAll('.mb-4.space-y-2 > div');

    messages.forEach(msg => {
        msg.style.transition = "opacity 0.5s ease";
        setTimeout(() => {
            msg.style.opacity = 0;
            setTimeout(() => {
                msg.remove();
            }, 500); 
        }, 3000); 
    });
});
