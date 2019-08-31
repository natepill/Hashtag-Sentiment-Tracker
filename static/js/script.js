let ctx = document.getElementById('myChart').getContext('2d');

let labels = ['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
// NOTE: Only the first four colors are unique
let colorHex = ['#FB3640', '#EFCA08', '#43BA8B', '#153D5B', '#FB8640', '#EF3A08', '#41AA8B', '#453D5B', '#AB3640', '#FFCA08', '#53AA8B', '#353D5B', '#53AA8B'];

let myChart = new Chart(ctx, {
  type: 'pie',
  data: {
    datasets: [{
      data: values,
      backgroundColor: colorHex
    }],
    labels: labels
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
