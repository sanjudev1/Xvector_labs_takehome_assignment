function Bubbleplot(values_column1, values_column2) {
  const xArray = values_column1;
  const yArray = values_column2;
  console.log('after ', xArray);

  const colors = ['red', 'green', 'blue', 'orange', 'pink', 'white', 'yellow'];
  const trace1 = {
    x: xArray,
    y: yArray,
    mode: 'markers',
    margin: { t: -10, l: 0, r: 0, b: 10 },
    marker: {
      color: Array.from(
        { length: xArray.length },
        (_, i) => colors[i % colors.length]
      ),
      size: Array.from({ length: xArray.length }, (_, i) => (i + 1) * 4),
    },
  };

  const dataForPlotly = [trace1];

  const layout = {
    title: 'Plotting Bubbles',
  };

  Plotly.newPlot('myPlot', dataForPlotly, layout);
}
