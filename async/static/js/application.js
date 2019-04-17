$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = 0;

    //receive details from server
    socket.on('new', function(msg) {

        numbers_received = msg.el_numero + 1000



        $('#log').text('Received ' + numbers_received);

        // text('new' + '<p>' + numbers_string + 'BAsura de mierda' + '<p>' );
        // text('Received #' + msg.count + ': ' + msg.data)
        // $("#results").text(data.color);
        // $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

});