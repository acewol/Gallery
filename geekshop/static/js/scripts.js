window.onload = function() {
  $('.basket-list').on('change', 'input[type="number"]', function(event) {
    var inputObject = event.target;
    
    $.ajax({
      url: `/basket/update/${inputObject.name}/${inputObject.value}/`,

      success: function(data) {
        $('.basket-list').html(data.result);
      },
    });
  });
}