$(() => {

    var socket = io({autoConnect: false})
    socket.connect()
    socket.on('notification', (notification_data) => {
        var data = JSON.parse(notification_data)
        alert(data)
     })
    
})

