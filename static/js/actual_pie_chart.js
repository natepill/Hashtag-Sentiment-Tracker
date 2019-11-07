
const axios = require('axios')

window.onload = function() {

  console.log("HELLOS!");

  // var frequencies = $('#frequencies').val();
  // var emotion_classes = $('#emotion_classes').val();

  const getData = async() => {
      try {
        return await axios.get('http://127.0.0.1:5000/get_data')
      } catch (error) {
        console.error(error)
      }
    }

  console.log($`getData: ${getData}`)

  let ctx = document.getElementById('myChart').getContext('2d');
  let colorHex = ['#a91834', '#4B1858', '#ffffff', '#00daff', '#006633', '#8cff1f', '#000000', '#d86a77', '#EEEEEE', '#a9b6aa', '#f3d8a5', '#353D5B', '#97bd91'];

  console.log("HELLO")
  // console.log(`values: ${frequencies}`);
  // console.log(`labels: ${labels}`);

  // May not need iterative rendering, just assign passed in array values
  // https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/

  let myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      datasets: [{
      data : frequencies,
        backgroundColor: colorHex
      }],
      labels: emotion_classes
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


} // End Window onload
