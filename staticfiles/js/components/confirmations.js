// Inicializa as confirmacoes compartilhadas
export function initializeConfirmations() {
    document.addEventListener("submit", (event) => {
        const form = event.target;

        if (event.defaultPrevented) {
            return;
        }

        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        if (!form.hasAttribute("data-confirm")) {
            return;
        }

        // Recupera a mensagem de confirmacao
        const message = form.dataset.confirm.trim() ||
            "Deseja realmente realizar esta operação?";

        // Interrompe o envio caso o usuario cancele
        if (!window.confirm(message)) {
            event.preventDefault();
        }
    });
}
