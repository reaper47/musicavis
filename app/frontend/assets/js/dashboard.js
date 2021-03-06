import Chart from 'chart.js';
const moment = require('moment');
import 'chartjs-plugin-colorschemes';


function setupDashboard(datasets, dates) {
    const tableStats = document.getElementById('dashboard__table-statistics')
    const practiceContainer = document.getElementById('dashboard__practice-container')

    document.getElementById('dashboard__li-stats').addEventListener('click', () => {
        practiceContainer.style.display = 'none'
        tableStats.style.display = 'inline-table'
    });

    document.getElementById('dashboard__li-practice').addEventListener('click', () => {
        practiceContainer.style.display = 'block';
        tableStats.style.display = 'none';
    });

    createPracticeGraph(datasets, dates.map(x => moment(x, 'YYYY-MM-DD')));
}

function createPracticeGraph(sets, labels) {
    let datasets = []
    for (let instrument in sets) {
        datasets.push({
            label: instrument,
            borderWidth: 2,
            hoverBackgroundColor: '#FFF',
            data: Array.from(sets[instrument]).map(x => x.length)
        });
    }

    const ctx = document.getElementById('dashboard__practice-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets
        },
        options: {
            plugins: {
                colorschemes: {
                    scheme: 'tableau.Classic10'
                }
            },
            maintainAspectRatio: false,
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: (item, data) => item.yLabel.toFixed(1) + 'm'
                },
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Practice Time (minutes)',
                        fontSize: 15,
                        fontFamily: "'Roboto', 'Helvetica', 'Helvetica', 'Arial', sans-serif",
                        lineHeight: 2
                    },
                    gridLines: {
                        color: 'rgba(255, 99, 132, 0.2)',
                        lineWidth: 0.75
                    }
                }],
                xAxes: [{
                    type: 'time',
                    time: {
                        tooltipFormat: 'll'
                    },
                    gridLines: {
                        color: 'rgba(255, 99, 132, 0.2)',
                        lineWidth: 0.75
                    }
                }]
            }
        },
        plugins: [{
            afterDatasetsDraw: (chart) => {
                if (chart.tooltip._active && chart.tooltip._active.length) {
                    const activePoint = chart.tooltip._active[0]
                    const y_axis = chart.scales['y-axis-0']
                    const x = activePoint.tooltipPosition().x
                    ctx.save();
                    ctx.beginPath();
                    ctx.moveTo(x, y_axis.top);
                    ctx.lineTo(x, y_axis.bottom)
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = '#07C';
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }]
    })
}

export { setupDashboard };
