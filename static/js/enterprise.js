/**
 * Smart Employee Management System — Enterprise Core Scripts (V2 Ultra)
 * Interactive UI behaviors, Web Audio chimes, Live Toast notifications, and search helpers
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-highlight current active sidebar link
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.ems-sidebar .ems-nav-link');
    sidebarLinks.forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && (href === currentPath || (href !== '/' && href !== '/auth/dashboard/' && currentPath.startsWith(href)))) {
            link.classList.add('active');
        }
    });

    // 2. Auto-dismiss alert banners after 6 seconds with smooth fade
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'all 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } else {
                    alert.remove();
                }
            }, 500);
        }, 6000);
    });

    // 3. Initialize tooltips
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 4. Live Toast Notification Helper with Audio Chime
    window.emsToast = function (title, message, type = 'info') {
        let toastContainer = document.getElementById('emsToastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'emsToastContainer';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1090';
            document.body.appendChild(toastContainer);
        }

        const iconMap = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-exclamation-triangle-fill text-danger',
            warning: 'bi-exclamation-circle-fill text-warning',
            info: 'bi-info-circle-fill text-primary'
        };
        const iconClass = iconMap[type] || iconMap.info;

        const toastEl = document.createElement('div');
        toastEl.className = 'toast align-items-center border-0 shadow-lg mb-2';
        toastEl.style.background = 'rgba(255, 255, 255, 0.95)';
        toastEl.style.backdropFilter = 'blur(16px)';
        toastEl.style.borderRadius = '14px';
        toastEl.style.border = '1px solid rgba(226, 232, 240, 0.8)';
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');

        toastEl.innerHTML = `
            <div class="d-flex p-3 align-items-center gap-3">
                <i class="bi ${iconClass} fs-4"></i>
                <div class="flex-grow-1">
                    <div class="fw-bold text-dark small">${title}</div>
                    <div class="text-muted" style="font-size: 0.8rem;">${message}</div>
                </div>
                <button type="button" class="btn-close me-1 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toastEl);
        const bsToast = new bootstrap.Toast(toastEl, { delay: 5000 });
        bsToast.show();

        // Play Notification Sound
        if (window.emsAudio) {
            if (type === 'success') window.emsAudio.playSuccess();
            else if (type === 'error' || type === 'warning') window.emsAudio.playAlert();
            else window.emsAudio.playChime();
        }

        toastEl.addEventListener('hidden.bs.toast', function () {
            toastEl.remove();
        });
    };

    // 5. Generic Chart.js Helper
    window.renderEMSChart = function (canvasId, type, data, options) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;
        const ctx = canvas.getContext('2d');
        
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: { size: 12, family: "'Plus Jakarta Sans', sans-serif" }
                    }
                }
            }
        };

        const mergedOptions = Object.assign({}, defaultOptions, options || {});
        return new Chart(ctx, {
            type: type,
            data: data,
            options: mergedOptions
        });
    };

    // 6. Live Table Search Filter
    const liveSearchInputs = document.querySelectorAll('[data-ems-search-target]');
    liveSearchInputs.forEach(function (input) {
        input.addEventListener('keyup', function () {
            const targetTableId = this.getAttribute('data-ems-search-target');
            const table = document.getElementById(targetTableId);
            if (!table) return;

            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(filter) > -1 ? '' : 'none';
            });
        });
    });
});
