$(document).ready(function(){
    renderChart()
    setEventForShowChartBtn()
})


function renderChart() {
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
}

function createChartForSalesOfThisMonthByTimeframes(json) {
    stadiums = json.sales_of_this_month_by_timeframes
    for (let stadium of stadiums) {
        stadiumName = stadium.stadium_name
        stadiumNameConverted = stadiumName.replace(/ /g, '_')

        let canvasId = `this-month-charts-of-${stadiumNameConverted}`
        let canvas = $(`<canvas id="${canvasId}" width="400" height="400"></canvas>`)
        let chartsDiv = $('#this-month-charts')
        let newDiv = $('<div class="col-sm-11"></div>')

        data = stadium.sales_and_number_of_orders
        dataOfSales = data.sales
        dataOfNumberOfOrder = data.number_of_orders
        labelsOfChart = stadium.timeframes
        chartId = canvasId

        chartsDiv.append(newDiv)
        newDiv.append(canvas)

        createDoubleColumnChart(dataOfSales, dataOfNumberOfOrder, labelsOfChart, chartId, stadiumName)
    }
}

function createDoubleColumnChart(dataOfSales, dataOfNumberOfOrder, labelsOfChart, chartId, stadiumName) {
    var canvas = $(`#${chartId}`)
    var myChart = new Chart(canvas, {
        type: 'bar',
        data: {
            datasets: [{
                data: dataOfSales,
                label: 'Doanh thu',
                backgroundColor: [
                    'rgba(55, 52, 214, 0.2)',
                ],
                yAxisID: 'left-y-axis'
            }, {
                data: dataOfNumberOfOrder,
                label: 'Số người đặt',
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
    stadiums = json.sales_information_in_lastest_12_months

        for (let [index, stadium] of stadiums.entries()) {
            if (index === (stadiums.length - 1)) {
                break
            }
            stadiumName = stadium.stadium_name

            if(stadiumName === undefined) {
                stadiumName = 'Total sales'
            }
            stadiumNameConverted = stadiumName.replace(/ /g, '_')

            let canvasId = `chart-of-${stadiumNameConverted}`
            let canvas = $(`<canvas id="${canvasId}" width="400" height="400"></canvas>`)
            let chartsDiv = $('#twelve-months-charts')
            let newDiv = $('<div class="col-sm-6"></div>')

            labels = stadium.months_and_year
            data = stadium.sales
            chartId = canvasId

            chartsDiv.append(newDiv)
            newDiv.append(canvas)

            createChart(chartId, labels, data, stadiumName)
        }
}

function createChart(chartId, labels, data, stadiumName){
    var ctx = $(`#${chartId}`)[0].getContext('2d')
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
    $('#this-month-show').click(function() {
        $('#twelve-months-charts').css('display', 'none')
        $('#this-month-charts').css('display', 'flex')
    })

    $('#twelve-months-show').click(function() {
        $('#twelve-months-charts').css('display', 'flex')
        $('#this-month-charts').css('display', 'none')
    })
}



