document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("novoTarefaModal");
  const novaTarefaBtn = document.getElementById("novaTarefaBtn");
  const cancelBtn = document.getElementById("cancelNovaTarefa");
  const modalTitle = document.getElementById("modalTitle");
  const modalSubmitBtn = document.getElementById("modalSubmitBtn");

  // Abrir modal para nova tarefa
  if (novaTarefaBtn) {
    novaTarefaBtn.addEventListener("click", function (e) {
      e.preventDefault();
      modalTitle.textContent = "Adicionar Tarefa ao Projeto";
      modalSubmitBtn.textContent = "Criar Tarefa";

      document.getElementById("tarefa_id").value = "";
      document.getElementById("nome_tarefa").value = "";
      document.getElementById("descricao").value = "";
      document.getElementById("estimativa_horas").value = "";
      document.getElementById("categoria").value = "";

      modal.classList.remove("hidden");
    });
  }

  // Abrir modal para editar tarefa
  document.querySelectorAll(".editar-tarefa").forEach((button) => {
    button.addEventListener("click", function () {
      modalTitle.textContent = "Editar Tarefa";
      modalSubmitBtn.textContent = "Salvar Alterações";

      document.getElementById("tarefa_id").value = this.dataset.id;
      document.getElementById("nome_tarefa").value = this.dataset.nome;
      document.getElementById("descricao").value = this.dataset.descricao;
      document.getElementById("estimativa_horas").value = this.dataset.estimativa;
      document.getElementById("categoria").value = this.dataset.categoria;

      modal.classList.remove("hidden");
    });
  });

  // Cancelar tarefa
  document.querySelectorAll(".cancelar-tarefa-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const url = this.dataset.url;
      if (confirm("Tem certeza que deseja cancelar esta tarefa?")) {
        window.location.href = url;
      }
    });
  });

  // Restaurar tarefa
  document.querySelectorAll(".restaurar-tarefa-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const url = this.dataset.url;
      if (confirm("Deseja restaurar esta tarefa?")) {
        window.location.href = url;
      }
    });
  });

  // Excluir tarefa permanentemente
  document.querySelectorAll(".excluir-tarefa-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const url = this.dataset.url;
      if (
        confirm(
          "⚠️ Tem certeza que deseja excluir esta tarefa permanentemente? Essa ação não poderá ser desfeita."
        )
      ) {
        window.location.href = url;
      }
    });
  });

  // Fechar modal
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
    }
  });

  // Auto-fechar mensagens
  const messages = document.querySelectorAll(".mb-4.space-y-2 .w-full");
  messages.forEach((msg) => {
    setTimeout(() => {
      msg.classList.add("transition-opacity", "duration-500");
      msg.style.opacity = "0";
      setTimeout(() => {
        if (msg.parentNode) {
          msg.parentNode.removeChild(msg);
        }
      }, 500);
    }, 3000);
  });
});