function onload(){
    document.getElementById("loading").style.display="none";
    alert("haha");
}

function cloneTable(){
  var $clone = $TABLE.find('button.hide').clone(true).removeClass('hide');
  $TABLE.find('table').append($clone);
}

$('.clone').click(function () {
  alert("clicked");
  cloneTable();
});
