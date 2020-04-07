/*DATA TABLE*/
$(document).ready(function() {
  $('#apoderado-table').DataTable({
      "pagingType": "full_numbers",
      "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
      responsive: true,
      language: {
          "sProcessing":     "Procesando...",
          "sLengthMenu":     "Mostrar _MENU_ apoderados",
          "sZeroRecords":    "No se encontraron resultados",
          "sEmptyTable":     "Ningún dato disponible en esta tabla",
          "sInfo":           "Mostrando _START_ al _END_ de un total de _TOTAL_ apoderados",
          "sInfoEmpty":      "Mostrando  0 al 0 de un total de 0 apoderados",
          "sInfoFiltered":   "(filtrado de un total de _MAX_ apoderados)",
          "sInfoPostFix":    "",
          "sSearch":         "Buscar:",
          "sUrl":            "",
          "sInfoThousands":  ",",
          "sLoadingRecords": "Cargando...",
          "oPaginate": {
              "sFirst":    "Primero",
              "sLast":     "Último",
              "sNext":     "Siguiente",
              "sPrevious": "Anterior"
          },
          "oAria": {
              "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
              "sSortDescending": ": Activar para ordenar la columna de manera descendente"
          }
      }
  });
});

 /* Functions */

$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-apoderado").modal("show");
      },
      success: function (data) {
        $("#modal-apoderado .modal-content").html(data.html_form);
        $('#id_username').numeric({ decimal: false, negative: false }, function() { alert("Positive integers only"); this.value = ""; this.focus(); });
        $('#id_username').attr('maxlength','8');        

      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("success")
        if (data.form_is_valid) {
          console.log("for is valid")
          $("#apoderado-table tbody").html(data.html_apoderado_list);
          console.log("for is valid tbody")
          $("#modal-apoderado").modal("hide");
        }
        else {
          $("#modal-apoderado .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create apoderado
  $(".js-create-apoderado").click(loadForm);
  $("#modal-apoderado").on("submit", ".js-apoderado-create-form", saveForm);

  // Update apoderado
  $("#apoderado-table").on("click", ".js-update-apoderado", loadForm);
  $("#modal-apoderado").on("submit", ".js-apoderado-update-form", saveForm);

  // Delete apoderado
  $("#apoderado-table").on("click", ".js-delete-apoderado", loadForm);
  $("#modal-apoderado").on("submit", ".js-apoderado-delete-form", saveForm);

});
