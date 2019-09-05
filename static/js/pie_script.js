
let ctx = document.getElementById('myChart').getContext('2d');
let colorHex = ['#a91834', '#4B1858', '#ffffff', '#00daff', '#006633', '#8cff1f', '#000000', '#d86a77', '#EEEEEE', '#a9b6aa', '#f3d8a5', '#353D5B', '#97bd91'];

console.log(labels);
console.log(values);

// May not need iterative rendering, just assign passed in array values
// https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/

let myChart = new Chart(ctx, {
  type: 'pie',
  data: {
    datasets: [{
    data : [{% for item in values %}
                {{item}},
              {% endfor %}],
      backgroundColor: colorHex
    }],
    labels: [{% for item in labels %}
             "{{item}}",
            {% endfor %}]
  },
  options: {
    responsive: true,
    legend: {
      position: 'bottom'
    },
    plugins: {
      datalabels: {
        color: '#fff',
        anchor: 'end',
        align: 'start',
        offset: -10,
        borderWidth: 2,
        borderColor: '#fff',
        borderRadius: 25,
        backgroundColor: (context) => {
          return context.dataset.backgroundColor;
        },
        font: {
          weight: 'bold',
          size: '10'
        },
        formatter: (value) => {
          return value + ' %';
        }
      }
    }
  }
})
