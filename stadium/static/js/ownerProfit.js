$.ajax({
    type: 'get',
    url: '',
    data: {
        datasend: "Sended"
    },
    success: function(json) {
        stadiums = json.sales
        for (let i = 0; i < (stadiums.length - 1); i++) {
            stadium = stadiums[i]
            stadiumName = stadium.stadium_name
            if(stadiumName === undefined) {
                stadiumName = 'Total sales'
            }

            stadiumNameConverted = stadiumName.replace(/ /g, '_')

            let canvas =  document.createElement('CANVAS')
            console.log(canvas)
            let chartsDiv = document.getElementById('charts')
            let newDiv = document.createElement('div')
            newDiv.className = 'col-sm-5'

            canvas.id = `chart-of-${stadiumNameConverted}`
            canvas.width = 400
            canvas.height = 400
            labels = stadium.months_and_year
            data = stadium.sales
            chartId = canvas.id

            newDiv.appendChild(canvas)
            chartsDiv.appendChild(newDiv)

            createChart(chartId, labels, data, stadiumName)
        }
    },
    error: function(error) {
        console.log(error)
    }
})

function createChart(chartId, labels, data, stadiumName){
    var ctx = document.getElementById(chartId).getContext('2d');
    var chartId = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `Sales`,
                data: data,
                backgroundColor: [
                    'rgba(55, 52, 214, 0.2)',
                ],
                borderColor: [
                    'rgba(55, 52, 214, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Biểu đồ doanh thu của ${stadiumName} trong vòng 12 tháng gần nhất`
                }
            }

        }
    });
}

