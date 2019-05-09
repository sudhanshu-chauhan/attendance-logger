var web_socket_url = "ws://localhost:8001/get_attendance_data/";
var data_set = [];
var table_columns = [
            {title:"id"},
            {title:"name"},
            {title:"designation"},
            {title:"in_out"},
            {title:"department"},
            {title:"check-in time"}
           ];

$(document).ready(function(){
    var ws = new WebSocket(web_socket_url);
    console.log("testing");

    ws.onmessage = function(event){
        //logic to process incoming push messages
        //goes here
        console.log(event.data);
        $('#attendance-live-table').dataTable().fnDestroy();
        var current_data_obj = JSON.parse(event.data);
        var current_array = [
            current_data_obj["checkin_id"],
            current_data_obj["name"],
            current_data_obj["designation"],
            current_data_obj["in_out"],
            current_data_obj["department"],
            current_data_obj["checkin_time"]
        ];
        data_set.push(current_array);

        $("#attendance-live-table").DataTable({
        data: data_set,
        columns: table_columns});

    };

    $("#attendance-live-table").DataTable({
        data: data_set,
        columns: table_columns});
});