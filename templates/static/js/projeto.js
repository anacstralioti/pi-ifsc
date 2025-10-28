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

    document.querySelectorAll('.delete-project-btn').forEach(button => {
        button.addEventListener('click', function() {
            const url = this.dataset.url;
            if (confirm("Tem certeza que deseja cancelar este projeto?")) {
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
});
