function onload(){
    document.getElementById("loading").style.display="none";
}

function cloneTable(count, items, type, track, status, create, deliver, address, url){
  var div = document.getElementById('duplicate');
  var clone = div.cloneNode(true);
  clone.classList.remove("hide");
  clone.classList.add("delete");

  var but = clone.getElementsByTagName("button")[0];
  if (type="UF deliver"){
    but.setAttribute('onclick',url);
  }else{
    but.setAttribute('onclick','');
    but.innerHTML="No tracking";
  }

  var divc = clone.getElementsByTagName("div")[0];

  clone.getElementsByClassName("products")[0].innerHTML=("<b>products: </b>"+items);
  clone.getElementsByClassName("tn")[0].innerHTML=("<b>tracking number: </b>"+track);
  clone.getElementsByClassName("ship")[0].innerHTML=("<b>Delivery mode: </b>"+type);
  clone.getElementsByClassName("status")[0].innerHTML=("<b>Status: </b>"+status);
  clone.getElementsByClassName("create")[0].innerHTML=("<b>created date: </b>"+create);
  clone.getElementsByClassName("deliver")[0].innerHTML=("<b>delivered date: </b>"+deliver);

  var main=document.getElementById('dup main');
  main.appendChild(clone);

}

$('.clone').click(function () {
  alert("clicked");
  cloneTable(1);
});



function refresh(){
  var div = document.getElementsByClassName('delete');
  count=0
  while (count<div.length){
    div[0].parentNode.removeChild(div[0]);
  }

}

function getShipments(){
  document.getElementById("loading").style.display="block";
  refresh();
  var orderno=document.getElementById("orderno").value;
  count=0;
  url='https://mccptester.herokuapp.com/deliverycheck';
  $.ajax({
    url: url,
    type: 'GET',
    data: {
      increment_id:orderno
      },
    success: function (data) {
      var df = JSON.parse(data);

      var summary=df["summary"];
      document.getElementById("info").innerHTML="<b>"+summary+"</b>";

      var outstanding=df["outstanding items"];
      document.getElementById("outstanding").innerHTML=("<b>"+"outstanding items: "+"</b>"+outstanding);

      var count=df["count"];

      if (count >0){
        var shipments=df["shipments"];
        for (var i in shipments){
          if (i=="summary"){
            var summary=shipments[i];
            document.getElementById("info").innerHTML="<b>"+summary+"</b>";
          }else{
            var ship=shipments[i];
            var items=ship['items'];
            var type = ship['shipType'];
            var track = ship['tracking'];
            var url="https://www.urbanfox.asia/courier-tracking/tracking/?tracking_number="+track;
            var urlFunc="window.open('"+url+"')";
            var info=ship['info'];
            var status=ship['activity'];
            var create=ship['create_date'];
            var deliver=ship['delivr_date'];
            var address=ship['dst_addr'];
            cloneTable(count, items, type, track, status, create, deliver, address, urlFunc);
            count+=1;
          }
        }
      }

      document.getElementById("loading").style.display="none";
    },
    error: function(data) {
        alert(data);
        document.getElementById("loading").style.display="none";
    }
  });
}
