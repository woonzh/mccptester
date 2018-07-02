var $TABLE = $('#table');
var $BTN = $('#export-btn');
var $EXPORT = $('#export');


function onload(){
    var shopid = <?php echo $_POST['shopid'] ?>;
    alert(shopid);
    document.getElementById("loading").style.display="none";
}

function shopeeRedirect(){
    alert("testing");
}
