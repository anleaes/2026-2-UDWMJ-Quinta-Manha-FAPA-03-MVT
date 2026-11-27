// Inicializa o comportamento responsivo do menu lateral
export function initializeSidebar() {
    const sidebar = document.getElementById("app-sidebar");
    const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
    const mobileViewport = window.matchMedia("(max-width: 768px)");

    if (!sidebar || !sidebarToggle) {
        return;
    }

    // Atualiza o estado do menu lateral
    function setSidebarState(isOpen) {
        sidebar.classList.toggle("is-open", isOpen);
        sidebarToggle.setAttribute("aria-expanded", String(isOpen));
    }

    // Ajusta o menu de acordo com o tamanho da tela
    function synchronizeSidebar() {
        const isMobile = mobileViewport.matches;

        sidebarToggle.hidden = !isMobile;

        setSidebarState(!isMobile);
    }

    // Abre ou fecha o menu lateral
    sidebarToggle.addEventListener("click", () => {
        if (!mobileViewport.matches) {
            return;
        }

        const isOpen = sidebar.classList.contains("is-open");

        setSidebarState(!isOpen);
    });

    // Fecha o menu ao pressionar Escape
    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape" &&
            mobileViewport.matches &&
            sidebar.classList.contains("is-open")
        ) {
            setSidebarState(false);
            sidebarToggle.focus();
        }
    });

    // Identifica a mudanca entre desktop e dispositivos menores
    mobileViewport.addEventListener("change", synchronizeSidebar);

    sidebar.classList.add("is-collapsible");

    synchronizeSidebar();
}
