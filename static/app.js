$('.remove-button').on('click', function(event) {
  event.preventDefault();
  trackingNumber = $(event.target).data('id');
  removeUrl = "http://localhost:5000/delete"
  data = {"number": trackingNumber}

  $.ajax({
    url: removeUrl,
    contentType: "application/json",
    type: 'DELETE',
    data: JSON.stringify(data),
    success: function() {$(event.target).closest('tr').remove();}
  });
});
