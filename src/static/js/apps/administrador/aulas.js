/*DATA TABLE*/
$(document).ready(function() {
    $('#aula-table').DataTable({
        "pagingType": "full_numbers",
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        responsive: true,
        language: {
            "sProcessing":     "Procesando...",
            "sLengthMenu":     "Mostrar _MENU_ aulas",
            "sZeroRecords":    "No se encontraron resultados",
            "sEmptyTable":     "Ningún dato disponible en esta tabla",
            "sInfo":           "Mostrando _START_ al _END_ de un total de _TOTAL_ aulas",
            "sInfoEmpty":      "Mostrando 0 al 0 de un total de 0 aulas",
            "sInfoFiltered":   "(filtrado de un total de _MAX_ aulas)",
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
    $('#aula-cursos-table').DataTable({
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

$(document).ready(function() {
    $('#aula-profesores-table').DataTable({
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


 /* Functions */

$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-aula").modal("show");
      },
      success: function (data) {
        $("#modal-aula .modal-content").html(data.html_form);
        $('#id_nivel').select2({ width: 'resolve' ,theme: "bootstrap"});
        $('#id_grado').select2({ width: 'resolve' ,theme: "bootstrap"});
        $('#id_seccion').select2({ width: 'resolve' ,theme: "bootstrap"});
        $('#id_profesor').select2({ width: 'resolve' ,theme: "bootstrap"});
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
          $("#aula-table tbody").html(data.html_aula_list);
          $("#modal-aula").modal("hide");
        }
        else {
          $("#modal-aula .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create aula
  $(".js-create-aula").click(loadForm);
  $("#modal-aula").on("submit", ".js-aula-create-form", saveForm);

  // Update aula
  $("#aula-table").on("click", ".js-update-aula", loadForm);
  $("#modal-aula").on("submit", ".js-aula-update-form", saveForm);

  // Delete aula
  $("#aula-table").on("click", ".js-delete-aula", loadForm);
  $("#modal-aula").on("submit", ".js-aula-delete-form", saveForm);


});

  $(function () {
  var loadDetalleCursoForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-aula-cursos").modal("show");
      },
      success: function (data) {
        $("#modal-aula-cursos .modal-content").html(data.html_form);
        $('#id_curso').select2({ width: 'resolve' ,theme: "bootstrap"});
      }
    });
  };

  var saveDetalleCursoForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#aula-cursos-table tbody").html(data.html_aula_cursos_list);
          $("#modal-aula-cursos").modal("hide");
        }
        else {
          $("#modal-aula-cursos .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create aula
  $(".js-create-aula-cursos").click(loadDetalleCursoForm);
  $("#modal-aula-cursos").on("submit", ".js-aula-cursos-create-form", saveDetalleCursoForm);

  // Update aula
  $("#aula-cursos-table").on("click", ".js-update-aula-cursos", loadDetalleCursoForm);
  $("#modal-aula-cursos").on("submit", ".js-aula-cursos-update-form", saveDetalleCursoForm);

  // Delete aula
  $("#aula-cursos-table").on("click", ".js-delete-aula-cursos", loadDetalleCursoForm);
  $("#modal-aula-cursos").on("submit", ".js-aula-cursos-delete-form", saveDetalleCursoForm);

});


  $(function () {
  var loadDetalleprofesorForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-aula-profesores").modal("show");
      },
      success: function (data) {
        $("#modal-aula-profesores .modal-content").html(data.html_form);
        $('#id_profesor').select2({ width: 'resolve' ,theme: "bootstrap"});
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
          $("#aula-profesores-table tbody").html(data.html_aula_profesores_list);
          $("#modal-aula-profesores").modal("hide");
        }
        else {
          $("#modal-aula-profesores .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create aula
  $(".js-create-aula-profesores").click(loadDetalleprofesorForm);
  $("#modal-aula-profesores").on("submit", ".js-aula-profesores-create-form", saveDetalleprofesorForm);

  // Update aula
  $("#aula-profesores-table").on("click", ".js-update-aula-profesores", loadDetalleprofesorForm);
  $("#modal-aula-profesores").on("submit", ".js-aula-profesores-update-form", saveDetalleprofesorForm);

  // Delete aula
  $("#aula-profesores-table").on("click", ".js-delete-aula-profesores", loadDetalleprofesorForm);
  $("#modal-aula-profesores").on("submit", ".js-aula-profesores-delete-form", saveDetalleprofesorForm);

});
