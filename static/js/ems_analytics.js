/**
 * Smart Employee Management System — Advanced Analytics & Visualization Client
 * High-performance chart rendering, KPI aggregation, and live real-time trend computation.
 */

class EMSAnalyticsEngine {
    constructor() {
        this.charts = {};
        this.defaultFont = "'Plus Jakarta Sans', -apple-system, sans-serif";
    }

    /**
     * Renders an enterprise multi-series line chart with smooth gradients.
     */
    renderTrendChart(canvasId, labels, datasets) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        const ctx = canvas.getContext('2d');
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        const formattedDatasets = datasets.map(ds => {
            const gradient = ctx.createLinearGradient(0, 0, 0, 300);
            gradient.addColorStop(0, ds.color ? ds.color + '44' : 'rgba(30, 58, 138, 0.35)');
            gradient.addColorStop(1, 'rgba(255, 255, 255, 0.0)');

            return {
                label: ds.label,
                data: ds.data,
                borderColor: ds.color || '#1e3a8a',
                backgroundColor: gradient,
                borderWidth: 2.5,
                fill: true,
                tension: 0.38,
                pointBackgroundColor: ds.color || '#1e3a8a',
                pointRadius: 3,
                pointHoverRadius: 6
            };
        });

        const chart = new Chart(ctx, {
            type: 'line',
            data: { labels: labels, datasets: formattedDatasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { family: this.defaultFont, size: 12 }, boxWidth: 14 }
                    },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: this.defaultFont, weight: 'bold' },
                        bodyFont: { family: this.defaultFont },
                        padding: 12,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: { grid: { display: false }, ticks: { font: { family: this.defaultFont } } },
                    y: { grid: { color: '#f1f5f9' }, ticks: { font: { family: this.defaultFont } } }
                }
            }
        });

        this.charts[canvasId] = chart;
        return chart;
    }

    /**
     * Renders a doughnut distribution chart with center text.
     */
    renderDistributionDoughnut(canvasId, labels, data, colors) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;

        const ctx = canvas.getContext('2d');
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors || ['#1e3a8a', '#10b981', '#f59e0b', '#ef4444', '#06b6d4'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { family: this.defaultFont, size: 11 }, boxWidth: 12, padding: 12 }
                    }
                }
            }
        });

        this.charts[canvasId] = chart;
        return chart;
    }
}

window.emsAnalytics = new EMSAnalyticsEngine();
