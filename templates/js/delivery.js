function onload(){
    document.getElementById("loading").style.display="none";
}

function cloneTable(count){
  var div = document.getElementById('duplicate');
  var clone = div.cloneNode(true);

  var but = clone.getElementsByTagName("button")[0];
  but.innerHTML="testing";
  but.setAttribute('data-target','#demo'+String(count));

  var divc = clone.getElementsByTagName("div")[0];
  divc.setAttribute("id", "demo"+String(count));

  var main=document.getElementById('dup main');
  main.appendChild(clone);

}

$('.clone').click(function () {
  alert("clicked");
  cloneTable(1);
});
