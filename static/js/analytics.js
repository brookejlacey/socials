document.addEventListener('DOMContentLoaded', () => {
    const engagementChartCtx = document.getElementById('engagement-chart').getContext('2d');
    const metricsContainer = document.getElementById('metrics-container');

    async function loadAnalytics() {
        const response = await fetch('/api/get_analytics');
        const data = await response.json();

        const platforms = Object.keys(data);
        const engagementRates = platforms.map(platform => data[platform].engagement_rate);

        new Chart(engagementChartCtx, {
            type: 'bar',
            data: {
                labels: platforms,
                datasets: [{
                    label: 'Engagement Rate (%)',
                    data: engagementRates,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Engagement Rate (%)'
                        }
                    }
                }
            }
        });

        metricsContainer.innerHTML = '';
        for (const [platform, metrics] of Object.entries(data)) {
            const metricsDiv = document.createElement('div');
            metricsDiv.innerHTML = `
                <h3>${platform}</h3>
                <p>Followers: ${metrics.followers}</p>
                <p>Total Interactions: ${metrics.total_interactions}</p>
                <p>Engagement Rate: ${metrics.engagement_rate}%</p>
            `;
            metricsContainer.appendChild(metricsDiv);
        }
    }

    loadAnalytics();
});
