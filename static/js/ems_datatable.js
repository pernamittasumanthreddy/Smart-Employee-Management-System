/**
 * Smart Employee Management System — High-Performance Client Data Grid
 * Real-time sorting, searching, pagination, and multi-column filtering.
 */

class EMSDataGrid {
    constructor(tableId, options = {}) {
        this.table = document.getElementById(tableId);
        this.options = options;
        this.currentPage = 1;
        this.pageSize = options.pageSize || 15;
        this.data = [];
        this.filteredData = [];
    }

    setData(rows) {
        this.data = rows;
        this.filteredData = [...rows];
        this.render();
    }

    filter(query) {
        const q = String(query).toLowerCase().trim();
        if (!q) {
            this.filteredData = [...this.data];
        } else {
            this.filteredData = this.data.filter(row => {
                return Object.values(row).some(val => String(val).toLowerCase().includes(q));
            });
        }
        this.currentPage = 1;
        this.render();
    }

    sortBy(columnKey, ascending = true) {
        this.filteredData.sort((a, b) => {
            if (a[columnKey] < b[columnKey]) return ascending ? -1 : 1;
            if (a[columnKey] > b[columnKey]) return ascending ? 1 : -1;
            return 0;
        });
        this.render();
    }

    render() {
        if (!this.table) return;
        const tbody = this.table.querySelector('tbody');
        if (!tbody) return;

        const start = (this.currentPage - 1) * this.pageSize;
        const pageItems = this.filteredData.slice(start, start + this.pageSize);

        tbody.innerHTML = '';
        if (pageItems.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" class="text-center text-muted py-4">No records found.</td></tr>';
            return;
        }

        pageItems.forEach(item => {
            const tr = document.createElement('tr');
            Object.values(item).forEach(val => {
                const td = document.createElement('td');
                td.textContent = String(val);
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
}

window.EMSDataGrid = EMSDataGrid;
