 $(document).ready(function() {
    $('#dataTable2').DataTable( {
        "order": [[ 0, "desc" ]]
    });
 });

 $('#table_delete').click(function(){

        $('#card_body').empty();
        $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/log/table'
        });
 });