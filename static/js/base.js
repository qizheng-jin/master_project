function division(){
    var a = parseInt(document.getElementById("numOfParticipants").value);
    var b = parseInt(document.getElementById("classSize").value);
    if (b != 0){
        var c = (Math.round(a/b * 10000)/100.00 + "%");
    }else{
        var c = 'null'
    }
    document.getElementById("rates").value = c;
}

function divisionTwo(){
    var a = parseInt(document.getElementById("numOfParticipants").value);
    var b = parseInt(document.getElementById("bTwo").value);
    if (b != 0){
        var c = (Math.round(a/b * 10000)/100.00 + "%");
    }else{
        var c = 'null'
    }
    document.getElementById("cTwo").value = c;
}