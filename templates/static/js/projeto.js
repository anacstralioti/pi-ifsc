 document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('novoTarefaModal');
    const btn = document.getElementById('novaTarefaBtn');
    const cancelBtn = document.getElementById('cancelNovaTarefa');
    
    btn.addEventListener('click', function() {
      modal.classList.remove('hidden');
    });
    
    cancelBtn.addEventListener('click', function() {
      modal.classList.add('hidden');
    });
    
    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        modal.classList.add('hidden');
      }
    });
  });