function recherche() {
$('div').remove('.suppression');
var val = document.getElementById('search').value;
const regex = new RegExp('[0-9]{4,5}');

if (regex.test(val)==false){
	document.getElementById('abruti').innerText='Attention votre requête n\'est pas valide !';
}
else {
	$('div').remove('.suppression2');
	$('#loading').show();
	document.getElementById('Commentaire').innerText='';
}
}
