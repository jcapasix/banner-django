/*DATA TABLE*/
$(document).ready(function() {
    $('#curso-table').DataTable({
        "pagingType": "full_numbers",
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        responsive: true,
        language: {
            "sProcessing":     "Procesando...",
            "sLengthMenu":     "Mostrar _MENU_ cursos",
            "sZeroRecords":    "No se encontraron resultados",
            "sEmptyTable":     "Ningún dato disponible en esta tabla",
            "sInfo":           "Mostrando _START_ al _END_ de un total de _TOTAL_ cursos",
            "sInfoEmpty":      "Mostrando 0 al 0 de un total de 0 cursos",
            "sInfoFiltered":   "(filtrado de un total de _MAX_ cursos)",
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
        $("#modal-curso").modal("show");
      },
      success: function (data) {
        $("#modal-curso .modal-content").html(data.html_form);
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
          $("#curso-table tbody").html(data.html_curso_list);
          $("#modal-curso").modal("hide");
        }
        else {
          $("#modal-curso .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create curso
  $(".js-create-curso").click(loadForm);
  $("#modal-curso").on("submit", ".js-curso-create-form", saveForm);

  // Update curso
  $("#curso-table").on("click", ".js-update-curso", loadForm);
  $("#modal-curso").on("submit", ".js-curso-update-form", saveForm);

  // Delete curso
  $("#curso-table").on("click", ".js-delete-curso", loadForm);
  $("#modal-curso").on("submit", ".js-curso-delete-form", saveForm);

});
