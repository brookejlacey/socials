document.addEventListener('DOMContentLoaded', () => {
    const engagementChartCtx = document.getElementById('engagement-chart').getContext('2d');
    const sentimentChartCtx = document.getElementById('sentiment-chart').getContext('2d');
    const metricsContainer = document.getElementById('metrics-container');

    async function loadAnalytics() {
        const response = await fetch('/api/get_analytics');
        const data = await response.json();

        const platforms = Object.keys(data);
        const engagementRates = platforms.map(platform => data[platform].metrics.engagement_rate);
        const sentiments = platforms.map(platform => data[platform].metrics.avg_sentiment || 0);

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

        new Chart(sentimentChartCtx, {
            type: 'line',
            data: {
                labels: platforms,
                datasets: [{
                    label: 'Average Sentiment',
                    data: sentiments,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Sentiment (-1 to 1)'
                        },
                        min: -1,
                        max: 1
                    }
                }
            }
        });

        metricsContainer.innerHTML = '';
        for (const [platform, accountData] of Object.entries(data)) {
            const metricsDiv = document.createElement('div');
            metricsDiv.innerHTML = `
                <h3>${platform}</h3>
                <p>Followers: ${accountData.metrics.followers}</p>
                <p>Total Interactions: ${accountData.metrics.total_interactions}</p>
                <p>Engagement Rate: ${accountData.metrics.engagement_rate.toFixed(2)}%</p>
                <p>Engagement Trend: ${accountData.metrics.engagement_trend > 0 ? 'Increasing' : 'Decreasing'}</p>
                <p>Average Sentiment: ${accountData.metrics.avg_sentiment.toFixed(2)}</p>
                <p>Sentiment Variation: ${accountData.metrics.sentiment_std.toFixed(2)}</p>
                <h4>Top Hashtags:</h4>
                <ul>${accountData.metrics.top_hashtags ? accountData.metrics.top_hashtags.map(([tag, count]) => `<li>${tag}: ${count}</li>`).join('') : 'N/A'}</ul>
                <h4>Top Mentions:</h4>
                <ul>${accountData.metrics.top_mentions ? accountData.metrics.top_mentions.map(([user, count]) => `<li>${user}: ${count}</li>`).join('') : 'N/A'}</ul>
                <h4>Post Frequency:</h4>
                <p>${accountData.metrics.post_frequency ? accountData.metrics.post_frequency.toFixed(2) + ' posts/day' : 'N/A'}</p>
                <h4>Best Posting Time:</h4>
                <p>${accountData.metrics.best_posting_time || 'N/A'}</p>
            `;
            metricsContainer.appendChild(metricsDiv);
        }
    }

    loadAnalytics();
});
