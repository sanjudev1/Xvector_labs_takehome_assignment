$(document).ready(function () {
  function fetchmethod(selectedId, selected_data) {
    $.ajax({
      url: '/dataset/' + selectedId + '/compute',
      type: 'GET',
      success: function (data) {
        // Clear the existing options
        // Construct the HTML string for all options
        var optionsHtml = '';
        $.each(data.integer_columns, function (index, item) {
          optionsHtml += '<option value="' + item + '">' + item + '</option>';
        });

        // Append the HTML string to the select dropdown
        if (selected_data === 'selected_data1') {
          $('#result-list').empty();
          $('#result-list').append(optionsHtml);
        } else if (selected_data === 'selected_data2') {
          $('#result-list1').empty();
          $('#result-list2').empty();
          $('#result-list1').append(optionsHtml);
          $('#result-list2').append(optionsHtml);
        }
      },
      error: function (error) {
        console.error('Error fetching data:', error);
        // Handle the error, e.g., display an alert
      },
    });
  }
  $('#selected_data1').on('change', function () {
    var selectedId = $(this).val();
    fetchmethod(selectedId, 'selected_data1');
  });
  $('#selected_data2').on('change', function () {
    var selectedId = $(this).val();
    fetchmethod(selectedId, 'selected_data2');
  });

  // Trigger the change event on page load for the initially selected option

  $('#selected_data1').trigger('change');
  $('#selected_data2').trigger('change');

  // Bind the click event handler for compute-btn

  $('#compute-btn').on('click', function () {
    var selectedColumn = $('#result-list :selected').val();
    var selectedOperation = $('#operation').val();
    var selectedId = $('#selected_data1').val();

    // Perform the computation based on selectedColumn and selectedOperation
    $.ajax({
      url: '/dataset/' + selectedId + '/compute',
      type: 'POST',
      data: {
        selected_column: selectedColumn,
        operation: selectedOperation,
      },
      success: function (data) {
        $('#computation-result').text('Computation Result: ' + data.result);
        $('#computation-result').addClass('card');
      },
      error: function (error) {
        console.error('Error performing computation:', error);
      },
    });
  });

  $('#plot-btn').on('click', function () {
    var selectedColumn1 = $('#result-list1 :selected').val();
    var selectedColumn2 = $('#result-list2 :selected').val();
    var selectedId = $('#selected_data2').val();

    // Perform the computation based on selectedColumn and selectedOperation
    $.ajax({
      url: '/dataset/' + selectedId + '/plot',
      type: 'GET',
      data: {
        selected_column1: selectedColumn1,
        selected_column2: selectedColumn2,
      },
      success: function (data) {
        Bubbleplot(
          data.values_column1,
          data.values_column2,
          data.selected_column1,
          data.selected_column2
        );
        // Handle the result as needed, e.g., display it on the page
      },
      error: function (error) {
        console.error('Error performing computation:', error);
        // Handle the error, e.g., display an alert
      },
    });
  });
});
