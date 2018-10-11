$(document).ready(function () {
    $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/system/ip-netmask-gateway',
                dataType: 'json',
                success: function(result){
                     x = result.netmask;
                     z = result.gateway;
                     y = result.wan;
                    document.getElementById("wan_net").value = x;
                    document.getElementById("wan_gate").value = z;
                    document.getElementById("wan_ip").value = y;
                }
          });

        $('#good').click(function(){
          $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/wan_IP/IP_address',
                data: {'a': document.getElementById("local_ip").value},
                dataType: 'json',
                success: function(result) {
                    alert(result.Result);
                }
           });
           alert("IP 주소가 수동설정 되었습니다.");
        });

        $('input:radio[name="optradio"]').click(function(){
        if ($(this).is(':checked') && $(this).val() == 'auto') {
            $('#good').addClass('btn-disabled');
            $('#good').attr('disabled', 'disabled');
            $('#good').prop('disabled', true);
            setTimeout(function(){ alert("IP 주소가 DHCP 클라이언트에 의해 자동할당되었습니다."); }, 0);
            $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/system/ip-netmask-gateway',
                dataType: 'json',
                success: function(result){
                     y = result.lan;
                    document.getElementById("local_ip").value = y;
                }
          });
            document.getElementById("local_ip").disabled = true;
        }else {
            $('#good').prop('disabled', false);
            document.getElementById("local_ip").disabled = false;
        }
});
});