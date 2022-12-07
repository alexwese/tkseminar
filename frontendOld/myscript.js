var base1 = 200;
var base1 = 259.85;
var base1 = 5850;


var change1 = 0;
var change2 = 0;
var change3 = 0;

var prob1 = 100;
var prob2 = 100;
var prob3 = 100;

var trigger1Sign = 1;
var trigger2Sign = 1;
var trigger3Sign = 1;

var coeff1 = 0.5;
var coeff2 = 4.1;
var coeff3 = 0.13;

var aluPrice = 3245.79


var myLine1 = new LeaderLine(
    document.getElementById('trigger1'),
    document.getElementById('re1')
);

myLine1.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel(String(coeff1))})
function updateWeight1(val) {
    myLine1.middleLabel = LeaderLine.pathLabel(String(val)); 
    trigger1 = val;
    updateRE1();
}



function changeSign1(checked) {
    if (checked) {
        trigger1Sign = -1;
        myLine1.color = '#FFAF79';
    } else {
        trigger1Sign = 1;
        myLine1.color = '#89B0AE';
    }
    updateRE1();
}

function updateRE1() {
    var result = trigger1Sign*trigger1*prob1+trigger2Sign*trigger2*prob2;
    result = Math.round(result * 100) / 100
    re2 = result;
    document.getElementById("re1factor").innerHTML = String(result);
    var endResult = re2*0.7+0.12*0.3;
    endResult = Math.round(endResult * 100) / 100
    document.getElementById("endPrice").innerHTML = String(endResult);
}

var myLine2 = new LeaderLine(
      document.getElementById('re1'),
      document.getElementById('price')
);

myLine2.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel(String(coeff2))})


function changeSign2(checked) {
    if (checked) {
        trigger2Sign = -1;
        myLine2.color = '#FFAF79';
    } else {
        trigger2Sign = 1;
        myLine2.color = '#89B0AE';
    }
    updateRE1();
}

var myLine3 = new LeaderLine(
    document.getElementById('re2'),
    document.getElementById('price')
);

myLine3.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel(String(coeff3))})

function changeSign3(checked) {
    if (checked) {
        trigger3Sign = -1;
        myLine3.color = '#FFAF79';
    } else {
        trigger3Sign = 1;
        myLine3.color = '#89B0AE';
    }
    updateRE1();
}


