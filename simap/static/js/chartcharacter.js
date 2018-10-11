    var data = [];
    var data2 = [];
    var dataset, dataset2;
    var totalPoints = 50;
    var updateInterval = 1000;
    var now = new Date().getTime();
    var count = 0;
    var count2 = 1;

    function GetData1() {
        $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/simap/info/cpu-ram',
                dataType: 'json',
                success: function(result){
                  if(data.length > totalPoints){
                    data.shift();
                    data2.shift();
                  }
                    var w = result.time;
                    var y = result.cpu;
                    var x = result.ram;
                    var temp = [now += updateInterval, y];
                    var temp2 = [now += updateInterval, x];
                    data.push(temp);
                    data2.push(temp2);

                    if(y > 75){
                        if(count<5)
                        {
                            count++;
                         }
                        else
                        {
                            count++;
                            var id = '#div_'+ count2;
                            var id2 = '#a_' + count2;
                            $(id).remove();
                            $(id2).remove();
                            count2++;
                        }
                        var html = '<div class="dropdown-divider" id="div_' + count + '"></div>';
                            html += '<a class="dropdown-item" id="a_' + count + '" href="log.html">';
                            html += '<span class="text-danger">';
                            html += '<strong>';
                            html += '<i class="fa fa-long-arrow-up fa-fw"></i>CPU 75% 이상 사용!</strong>';
                            html += '</span>';
                            html += '<span class="small float-right text-muted">' + w + '</span>';
                            html += '<div class="dropdown-message small">This is an automated server response message. All systems are online.</div></a>';

                        $("#starting").prepend(html);
                    }

                    if(x > 75){
                        if(count<5)
                         {
                            count++;
                         }
                        else
                        {
                            count++;
                            var id = '#div_'+ count2;
                            var id2 = '#a_' + count2;
                            $(id).remove();
                            $(id2).remove();
                            count2++;
                        }
                        var html = '<div class="dropdown-divider" id="div_' + count + '"></div>';
                            html += '<a class="dropdown-item" id="a_' + count + '" href="#">';
                            html += '<span class="text-success">';
                            html += '<strong>';
                            html += '<i class="fa fa-long-arrow-up fa-fw"></i>메모리 75% 이상 사용!</strong>';
                            html += '</span>';
                            html += '<span class="small float-right text-muted">' + w + '</span>';
                            html += '<div class="dropdown-message small">This is an automated server response message. All systems are online.</div></a>';
                            $("#starting").prepend(html);
                    }
                }
         });
    }

    var options = {
        series: {
            lines: {
                show: true,
                lineWidth: 1.2,
                fill: true
            }
        },
        xaxis: {
            mode: "time",
            tickSize: [2, "second"],
            tickFormatter: function(v, axis) {
                var date = new Date(v);
                return "";
                /*
                if (date.getSeconds() % 20 == 0) {
                    var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                    var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
                    var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

                   // return hours + ":" + minutes + ":" + seconds;
                   return "";
                } else {
                    return "";
                }
                */
            },

            axisLabel: "Time",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 10
        },
        yaxis: {
            min: 0,
            max: 100,
            tickSize: 5,
            tickFormatter: function(v, axis) {
                if (v % 10 == 0) {
                    return v + "%";
                } else {
                    return "";
                }
            },
            axisLabel: "CPU loading",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        },
        legend: {
            labelBoxBorderColor: "#fff"
        },
        grid: {
            backgroundColor: "#000000",
            tickColor: "#008040"
        }
    };

    $(document).ready(function() {

        GetData1();
        dataset = [{
            label: "CPU",
            data: data,
            color: "#00FF00"
        }];



        dataset2 = [{
            label: "RAM",
            data: data2,
            color: "#00FF00"
        }];
        var nowTime = new Date().getTime();
        for(var i = 0 ; i < totalPoints ; i++){
            var temp = [nowTime - updateInterval*(totalPoints-i), 0];
            data.push(temp);
            data2.push(temp);
        }

        $.plot($("#flot-placeholder1"), dataset, options);
        $.plot($("#flot-placeholder2"), dataset2, options);

         $.ajax({
                type: 'GET',
                url: 'http://127.0.0.1:8000/Log_five',
                dataType: 'json',
                success: function(result){
                    var i;
                    for(i=4;i>=0;i--)
                     {
                            var w = result[i].time;
                            var y = result[i].cpu;
                            var x = result[i].ram;
                            z = result[i].check;

                            if(z === true){
                                if(y > 75){
                                    count++;
                                var html = '<div class="dropdown-divider" id="div_' + count + '"></div>';
                                    html += '<a class="dropdown-item" id="a_' + count + '" href="log.html">';
                                    html += '<span class="text-danger">';
                                    html += '<strong>';
                                    html += '<i class="fa fa-long-arrow-up fa-fw"></i>CPU 75% 이상 사용!</strong>';
                                    html += '</span>';
                                    html += '<span class="small float-right text-muted">' + w + '</span>';
                                    html += '<div class="dropdown-message small">This is an automated server response message. All systems are online.</div></a>';

                                $("#starting").prepend(html);
                            }

                            if(x > 75){
                                    count++;
                                var html = '<div class="dropdown-divider" id="div_' + count + '"></div>';
                                    html += '<a class="dropdown-item" id="a_' + count + '" href="#">';
                                    html += '<span class="text-success">';
                                    html += '<strong>';
                                    html += '<i class="fa fa-long-arrow-up fa-fw"></i>메모리 75% 이상 사용!</strong>';
                                    html += '</span>';
                                    html += '<span class="small float-right text-muted">' + w + '</span>';
                                    html += '<div class="dropdown-message small">This is an automated server response message. All systems are online.</div></a>';
                                    $("#starting").prepend(html);
                              }
                            }
                      }
                }
         });
        function update() {
            GetData1();

            $.plot($("#flot-placeholder1"), dataset, options);
            $.plot($("#flot-placeholder2"), dataset2, options);
            setTimeout(update, updateInterval);
        }

        update();
    });
/*
var jsonData = $.ajax({
                type: 'GET',
                url: 'simap/info/cpu_memory.html',
                dataType: 'json',
            });
         yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
*/