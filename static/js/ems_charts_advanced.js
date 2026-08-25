/**
 * Smart Employee Management System — Advanced Charting & Dashboard Analytics
 * Renders radar charts, polar area charts, stacked bar charts, and sparkline trends.
 */

class EMSAdvancedCharts {
    static renderRadarSkillMatrix(canvasId, labels, currentLevels, targetLevels) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;
        const ctx = canvas.getContext('2d');

        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Current Proficiency',
                        data: currentLevels,
                        borderColor: '#1e3a8a',
                        backgroundColor: 'rgba(30, 58, 138, 0.25)',
                        borderWidth: 2,
                        pointBackgroundColor: '#1e3a8a'
                    },
                    {
                        label: 'Required Benchmark',
                        data: targetLevels,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.15)',
                        borderWidth: 2,
                        borderDash: [4, 4],
                        pointBackgroundColor: '#10b981'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: '#e2e8f0' },
                        grid: { color: '#f1f5f9' },
                        pointLabels: { font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 } },
                        ticks: { stepSize: 1, max: 5, min: 0 }
                    }
                }
            }
        });
    }

    static renderStackedMonthlyPayroll(canvasId, labels, basicData, hraData, allowanceData) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;
        const ctx = canvas.getContext('2d');

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Basic Salary', data: basicData, backgroundColor: '#1e3a8a' },
                    { label: 'HRA', data: hraData, backgroundColor: '#0284c7' },
                    { label: 'Special & Other Allowances', data: allowanceData, backgroundColor: '#10b981' }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true, grid: { display: false } },
                    y: { stacked: true, grid: { color: '#f1f5f9' } }
                }
            }
        });
    }
}

window.EMSAdvancedCharts = EMSAdvancedCharts;
