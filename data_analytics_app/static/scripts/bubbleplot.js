function Bubbleplot(
  values_column1,
  values_column2,
  selected_column1,
  selected_column2
) {
  const xArray = values_column1;
  const yArray = values_column2;
  const colors = [
    'red',
    'green',
    'blue',
    'orange',
    'pink',
    'yellow',
    'black',
    'brown',
    'violet',
  ];
  const trace1 = {
    x: xArray,
    y: yArray,
    mode: 'markers',

    marker: {
      color: Array.from(
        { length: xArray.length },
        (_, i) => colors[i % colors.length]
      ),
      // size: Array.from({ length: xArray.length }, (_, i) => (i + 1) * 4),
      size: 15,
    },
  };

  const dataForPlotly = [trace1];

  const layout = {
    title: {
      text: 'Plotting Bubbles',
      font: {
        color: 'purple',
        size: 24, // Set the color of the main title
      },
    },
    xaxis: {
      title: {
        text: selected_column1.toLowerCase(),
        font: {
          color: 'green',
          size: 22, // Set the color of the x-axis title
        },
      },
    },
    yaxis: {
      title: {
        text: selected_column2.toLowerCase(),
        font: {
          color: 'blue',
          size: 22, // Set the color of the y-axis title
        },
      },
    },
  };

  Plotly.newPlot('myPlot', dataForPlotly, layout);
}
