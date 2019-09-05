let ctx = document.getElementById('myChart').getContext('2d');

let labels = ['Pizza 🍕', 'Taco 🌮', 'Hot Dog 🌭', 'Sushi 🍣', 'Waffles', 'Apples','Berry','Bread','Hummus','Kebab','Beef','Chicken','Pineapple'];
let colorHex = ['#a91834', '#4B1858', '#ffffff', '#00daff', '#006633', '#8cff1f', '#000000', '#d86a77', '#EEEEEE', '#a9b6aa', '#f3d8a5', '#353D5B', '#97bd91'];

let myChart = new Chart(ctx, {
  type: 'pie',
  data: {
    datasets: [{
      data: [30, 10, 40, 20, 20, 40,60,34,43,23,54,23,65],
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
