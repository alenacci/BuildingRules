document.getElementById('manageButton').onclick = function() {
    window.open('http://10.0.2.15:5004/buildings/CSE/rooms');
};


var updateWindow = function() {

    document.location.reload();
};

setTimeout(updateWindow,60000);



