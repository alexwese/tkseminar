var trigger1 = 0.5;
var trigger1Sign = 1;
var prob1 = 0.1;
var trigger2 = 0.5;
var trigger2Sign = 1;
var prob2 = 0.1;



var re2 = 0.1;

var myLine1 = new LeaderLine(
    document.getElementById('trigger1'),
    document.getElementById('re1')
);

myLine1.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel(String(trigger1))})
function updateWeight1(val) {
    myLine1.middleLabel = LeaderLine.pathLabel(String(val)); 
    trigger1 = val;
    updateRE1();
}

function updateProb1(val) {
    prob1 = val;
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
      document.getElementById('trigger2'),
      document.getElementById('re1')
);

myLine2.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel(String(trigger2))})

function updateWeight2(val) {
    myLine2.middleLabel = LeaderLine.pathLabel(String(val)); 
    trigger2 = val;
    updateRE1();
}

function updateProb2(val) {
    prob2 = val;
    updateRE1();
}

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
    document.getElementById('re1'),
    document.getElementById('price')
);

myLine3.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel("0.3")})

var myLine4 = new LeaderLine(
    document.getElementById('re2'),
    document.getElementById('price')
);
  
myLine4.setOptions({color: '#89B0AE', middleLabel: LeaderLine.pathLabel("0.7")})
