$.ajax({
    type: 'get',
    url: '',
    data: {
        datasend: "Sended"
    },
    success: function(json) {
        console.log(json)
        createChartForLastest12MonthsSales(json)
        createChartForSalesOfThisMonthByTimeframes(json)
    },
    error: function(error) {
        console.log(error)
    }
})

function createChartForSalesOfThisMonthByTimeframes(json) {
    stadiums = json.all_stadium_sales_of_this_month_by_timeframes
    for (let i = 0; i < stadiums.length; i++) {
        stadium = stadiums[i]
        stadiumName = stadium.stadium_name
        stadiumNameConverted = stadiumName.replace(/ /g, '_')

        let canvas =  document.createElement('CANVAS')
        console.log(canvas)
        let chartsDiv = document.getElementById('this-month-charts')
        let newDiv = document.createElement('div')
        newDiv.className = 'col-sm-11'

        canvas.id = `this-month-charts-of-${stadiumNameConverted}`
        canvas.width = 400
        canvas.height = 400

        data = stadium.sales_and_number_of_orders
        dataOfSales = data.sales
        dataOfNumberOfOrder = data.number_of_orders
        labelsOfChart = stadium.timeframes
        chartId = canvas.id

        newDiv.appendChild(canvas)
        chartsDiv.appendChild(newDiv)

        createDoubleColumnChart(dataOfSales, dataOfNumberOfOrder, labelsOfChart, chartId, stadiumName)
    }
}

function createDoubleColumnChart(dataOfSales, dataOfNumberOfOrder, labelsOfChart, chartId, stadiumName) {
    var canvas = document.getElementById(chartId);
    var myChart = new Chart(canvas, {
        type: 'bar',
        data: {
            datasets: [{
                data: dataOfSales,
                label: 'Doanh thu',
                backgroundColor: [
                    'rgba(55, 52, 214, 0.2)',
                ],
                // This binds the dataset to the left y axis
                yAxisID: 'left-y-axis'
            }, {
                data: dataOfNumberOfOrder,
                label: 'Số người đặt',
    
                // This binds the dataset to the right y axis
                yAxisID: 'right-y-axis'
            }],
            labels: labelsOfChart
        },
        options: {
            scales: {
                'left-y-axis': {
                    type: 'linear',
                    position: 'left'
                },
                'right-y-axis': {
                    type: 'linear',
                    position: 'right'
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Biểu đồ doanh thu của ${stadiumName} trong tháng này`
                }
            }
        }
    });
}

function createChartForLastest12MonthsSales(json) {
    stadiums = json.sales_in_lastest_12_months
        for (let i = 0; i < (stadiums.length - 1); i++) {
            stadium = stadiums[i]
            stadiumName = stadium.stadium_name
            if(stadiumName === undefined) {
                stadiumName = 'Total sales'
            }

            stadiumNameConverted = stadiumName.replace(/ /g, '_')

            let canvas =  document.createElement('CANVAS')
            console.log(canvas)
            let chartsDiv = document.getElementById('twelve-months-charts')
            let newDiv = document.createElement('div')
            newDiv.className = 'col-sm-6'

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
}

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

function setEventForShowChartBtn() {
    thisMonthShowBtn = document.getElementById('this-month-show')
    twelveMonthsShowBtn = document.getElementById('twelve-months-show')
    thisMonthCharts = document.getElementById('this-month-charts')
    twelveMonthsCharts = document.getElementById('twelve-months-charts')

    thisMonthShowBtn.addEventListener('click', function() {
        twelveMonthsCharts.style.display = 'none'
        thisMonthCharts.style.display = 'flex'
        // if (twelveMonthsCharts.style.display === 'block') {
        //     twelveMonthsCharts.style.display = 'none'
        // }
        console.log('clicked')
    })

    twelveMonthsShowBtn.addEventListener('click', function() {
        twelveMonthsCharts.style.display = 'flex'
        thisMonthCharts.style.display = 'none'
        // if (twelveMonthsCharts.style.display === 'block') {
        //     twelveMonthsCharts.style.display = 'none'
        // }
        console.log('clicked')
    })
}

setEventForShowChartBtn()

