/*DATA TABLE*/
$(document).ready(function() {
  $('#profesor-table').DataTable({
      "pagingType": "full_numbers",
      "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
      responsive: true,
      language: {
          "sProcessing":     "Procesando...",
          "sLengthMenu":     "Mostrar _MENU_ profesores",
          "sZeroRecords":    "No se encontraron resultados",
          "sEmptyTable":     "Ningún dato disponible en esta tabla",
          "sInfo":           "Mostrando _START_ al _END_ de un total de _TOTAL_ profesores",
          "sInfoEmpty":      "Mostrando 0 al 0 de un total de 0 profesores",
          "sInfoFiltered":   "(filtrado de un total de _MAX_ profesores)",
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
$(document).ready(function() {
  $('#profesor-curso-table').DataTable({
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
        $("#modal-profesor").modal("show");
      },
      success: function (data) {
        $("#modal-profesor .modal-content").html(data.html_form);
        $('#id_profesion').select2({ width: 'resolve' ,theme: "bootstrap"}); 
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
        if (data.form_is_valid) {
          $("#profesor-table tbody").html(data.html_profesor_list);
          $("#modal-profesor").modal("hide");
        }
        else {
          $("#modal-profesor .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create profesor
  $(".js-create-profesor").click(loadForm);
  $("#modal-profesor").on("submit", ".js-profesor-create-form", saveForm);

  // Update profesor
  $("#profesor-table").on("click", ".js-update-profesor", loadForm);
  $("#modal-profesor").on("submit", ".js-profesor-update-form", saveForm);

  // Delete profesor
  $("#profesor-table").on("click", ".js-delete-profesor", loadForm);
  $("#modal-profesor").on("submit", ".js-profesor-delete-form", saveForm);

});


  $(function () {
  var loadDetalleprofesorForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-profesor-cursos").modal("show");
      },
      success: function (data) {
        $("#modal-profesor-cursos .modal-content").html(data.html_form);
        $('#id_profesor').select2({ width: 'resolve' ,theme: "bootstrap"});
        $('#id_curso').select2({ width: 'resolve' ,theme: "bootstrap"});
      }
    });
  };

  var saveDetalleprofesorForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#profesor-cursos-table tbody").html(data.html_profesor_cursos_list);
          $("#modal-profesor-cursos").modal("hide");
        }
        else {
          $("#modal-profesor-cursos .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create aula
  $(".js-create-profesor-cursos").click(loadDetalleprofesorForm);
  $("#modal-profesor-cursos").on("submit", ".js-profesor-cursos-create-form", saveDetalleprofesorForm);

  // Update aula
  $("#profesor-cursos-table").on("click", ".js-update-profesor-cursos", loadDetalleprofesorForm);
  $("#modal-profesor-cursos").on("submit", ".js-profesor-cursos-update-form", saveDetalleprofesorForm);

  // Delete aula
  $("#profesor-cursos-table").on("click", ".js-delete-profesor-cursos", loadDetalleprofesorForm);
  $("#modal-profesor-cursos").on("submit", ".js-profesor-cursos-delete-form", saveDetalleprofesorForm);

});
