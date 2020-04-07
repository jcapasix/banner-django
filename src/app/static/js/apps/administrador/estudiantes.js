/*DATA TABLE*/
$(document).ready(function() {
  $('#estudiante-table').DataTable({
      "pagingType": "full_numbers",
      "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
      responsive: true,
      language: {
          "sProcessing":     "Procesando...",
          "sLengthMenu":     "Mostrar _MENU_ estudiantes",
          "sZeroRecords":    "No se encontraron resultados",
          "sEmptyTable":     "Ningún dato disponible en esta tabla",
          "sInfo":           "Mostrando _START_ al _END_ de un total de _TOTAL_ estudiantes",
          "sInfoEmpty":      "Mostrando 0 al 0 de un total de 0 estudiantes",
          "sInfoFiltered":   "(filtrado de un total de _MAX_ estudiantes)",
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
        $("#modal-estudiante").modal("show");
      },
      success: function (data) {
        $("#modal-estudiante .modal-content").html(data.html_form);
        $('#id_username').numeric({ decimal: false, negative: false }, function() { alert("Positive integers only"); this.value = ""; this.focus(); });
        $('#id_username').attr('maxlength','8');   
        $('#id_aula').select2({ width: 'resolve' ,theme: "bootstrap"}); 
        $('#id_apoderado').select2({ width: 'resolve' ,theme: "bootstrap"}); 
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
        if (data.form_is_valid) {
          $("#estudiante-table tbody").html(data.html_estudiante_list);
          $("#modal-estudiante").modal("hide");
        }
        else {
          $("#modal-estudiante .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create estudiante
  $(".js-create-estudiante").click(loadForm);
  $("#modal-estudiante").on("submit", ".js-estudiante-create-form", saveForm);

  // Update estudiante
  $("#estudiante-table").on("click", ".js-update-estudiante", loadForm);
  $("#modal-estudiante").on("submit", ".js-estudiante-update-form", saveForm);

  // Delete estudiante
  $("#estudiante-table").on("click", ".js-delete-estudiante", loadForm);
  $("#modal-estudiante").on("submit", ".js-estudiante-delete-form", saveForm);

});
