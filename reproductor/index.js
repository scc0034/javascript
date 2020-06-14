													/*MUSICA*/
function musica(){
//Creamos el objeto
	xhr= new objetoXHR();
//Comprobamos que lo ha creado
	if(xhr){
		xhr.open('POST','multimedia/multimedia.json', true ); //true==asincrono
		//escuchamos el estado de la petición
		xhr.onreadystatechange=escuchaMusica;
		//Enviamos la consulta (en este caso no hacemos ninguna consulta porque el phph solo devuelve la fecha)
		xhr.send(null);
	}
}//fin de la funcion comienza

function escuchaMusica(){
	if (xhr.readyState==4){
		if((xhr.status==200) ||(xhr.status==304)){
			datos = eval( '(' +this.responseText+')'); //Para tratar los datos que me llegan de un json lo convertimos a un objeto con eval, tiene dentro un array de mi_multimedia que es un array
			contenido = "Selecciona una cancion: <select id='cancion' onchange=\"multimediaMusica()\"><option>Selecciona una opcion</option>"
			for(i=0;i<datos.mi_multimedia.length;i++){ //recorro el array mi_multimedia que es un atbo de datos
				//alert(datos.mi_multimedia[i].titulo); //muestro por pantallas los titulos
				contenido += "<option value=\"" + datos.mi_multimedia[i].titulo + "\" >" + datos.mi_multimedia[i].titulo + "</option>"; 
			}
			contenido += "</select>";
			document.getElementById("mu").innerHTML=contenido; //muestro el contenido de la select
			document.getElementById("vi").innerHTML=""; //quito el contenido del video
			document.getElementById("reproductorVideo").innerHTML=""; //quito el contenido del video
			document.getElementById("tablaVideo").innerHTML=""; //quito la tabla del video
		}else{
			alert("Ha habido un error de recepcion");
		}
	}
}//fin de la funcion escuchaMusica

//funcion para sacar el reproductor con sus botones
function multimediaMusica(){
	//tabla
	datos=eval( '(' +xhr.responseText+')');
	tabla="<br><table border='1'><tr><th>Titulo</th><th>Artista</th><th>Año</th></tr>";
	for(i=0;i<datos.mi_multimedia.length;i++){
		if (document.getElementById("cancion").value==datos.mi_multimedia[i].titulo) {
			ruta = "multimedia\\audio\\" + datos.mi_multimedia[i].titulo;
				tabla += "<tr>";
				try	{
					tabla+="<td>" + datos.mi_multimedia[i].titulo + "</td>";
				}catch (er){
					tabla+= "<td>&nbsp;</td>";
				}
				try	{
					tabla+="<td>" + datos.mi_multimedia[i].artist + "</td>";
				}catch (er){
					tabla+= "<td>&nbsp;</td>";
				}
				try	{
					tabla+="<td>" + datos.mi_multimedia[i].ano + "</td>";
				}catch (er){
					tabla+= "<td>&nbsp;</td>";
				}
				tabla += "</tr>";
			}
		}
	tabla += "</table>";


	//reproductor
	src=document.getElementById("cancion").value; //selecciona el id del select seleccionado
	reproductor = "<div class='audio'>";
	reproductor += "<audio id='adel' controls src='./multimedia/audio/"+src+"' type='audio/mp3'</audio>";
	reproductor +=	"</audio><br/>";
	reproductor +=	"<input type='button' value='<<' class='atrasar' id='atrasar' onclick='atrasar()'>";
	reproductor +=	"<input type='button' value='Play/Pause' class='play' id='reproduce' onclick='reproducirAudio(this.id)'>";
	reproductor +=	"<input type='button' value='>>' class='adelantar' id='adelantar' onclick='adelantar()'>";
	reproductor +=	"<input type='button' value='-' class='menos' id='-' onclick='bajar()'>";
	reproductor +=	"<input type='button' value='+' class='mas' id='+' onclick='subir()'>";
	reproductor +=	"<input type='button' value='Mute' class='silencio' id='mute' onclick='mute()'>";
	reproductor +=	"<input type='button' value='No Mute' class='nosilencio' id='nomute'  onclick='noMuteAudio()'>";
	reproductor +=	"</div>";
	document.getElementById("reproductorMusica").innerHTML=reproductor; //muestro el contenido de la select
	document.getElementById("tablaMusica").innerHTML=tabla; //muestro el contenido de la select
} 

//funcion para atrasar
function atrasar(){
	document.getElementById("adel").currentTime = document.getElementById("adel").currentTime-10;
}

//funcion que reproduce o pausa un audio
function reproducirAudio(id){
	reproductor = document.getElementById('adel');
	boton = document.getElementById(id);
	if(reproductor.paused){
		reproductor.play();			
	}else{
		reproductor.pause();
	}
}

//funcion para adelantar 
function adelantar(){
	document.getElementById("adel").currentTime = document.getElementById("adel").currentTime+10;
}

//funcion para subir el volumen
function subir(){
	document.getElementById("adel").volume+=0.1;
}

//funcion para bajar el volumen
function bajar(){
	document.getElementById("adel").volume-=0.1;
}

//funcion para poner el volumen en mute
function mute(){
	if(document.getElementById("adel").muted){
		document.getElementById("adel").muted=false;
	}else{
		document.getElementById("adel").muted=true;
	}
}

//funcion para quitar el mute
function noMuteAudio(){
	document.getElementById('adel').muted=false;
}

														

														/*VIDEO*/
function video(){
//Creamos el objeto
	xhr2= new objetoXHR();
//Comprobamos que lo ha creado
	if(xhr2){
		xhr2.open('POST','multimedia/datos.xml', true ); //true==asincrono
		//escuchamos el estado de la petición
		xhr2.onreadystatechange=escuchaVideo;
		//Enviamos la consulta (en este caso no hacemos ninguna consulta porque el phph solo devuelve la fecha)
		xhr2.send(null);
	}
}//fin de la funcion comienza

function escuchaVideo(){
	if (xhr2.readyState==4){
		if((xhr2.status==200) ||(xhr2.status==304)){
			vid = xhr2.responseXML.documentElement.getElementsByTagName("VIDEO");
			contenido = "";
			for (i=0;i<vid.length;i++){
				contenido += "<input type='radio' onclick='multimediaVideo()' name='vid' value=\"" + vid[i].getElementsByTagName("TITULO")[0].firstChild.nodeValue + "\"> " + vid[i].getElementsByTagName("TITULO")[0].firstChild.nodeValue + "<br>";
			}
			document.getElementById("reproductorMusica").innerHTML=""; //quito la select de la musica
			document.getElementById("mu").innerHTML=""; //quito el reproductor de la musica
			document.getElementById("tablaMusica").innerHTML=""; //quito la tabla de la musica
			document.getElementById("vi").innerHTML=contenido; //muestro el contenido de los radiobutton
		}else{
			alert("Ha habido un error de recepcion");
		}
	}
}//fin de la funcion escucha

//funcion del reproductor del video
function multimediaVideo(){
	//tabla 
	vid = xhr2.responseXML.documentElement.getElementsByTagName("VIDEO");
	salida="<br><table border='1'><tr><th>Titulo</th><th>Artista</th><th>Año</th></tr>";
	for (i=0;i<vid.length;i++){
		if (getRadioValue("vid")==vid[i].getElementsByTagName("TITULO")[0].firstChild.nodeValue) {
			ruta = vid[i].getElementsByTagName("RUTA")[0].firstChild.nodeValue;
			salida+="<tr>";
			try	{
				salida+="<td>" + vid[i].getElementsByTagName("TITULO")[0].firstChild.nodeValue + "</td>";
			}
			catch (er){
				salida+= "<td>&nbsp;</td>";
			}
			try	{
				salida+="<td>" + vid[i].getElementsByTagName("ARTIST")[0].firstChild.nodeValue + "</td>";
			}
			catch (er){
				salida+= "<td>&nbsp;</td>";
			}
			try	{
				salida+="<td>" + vid[i].getElementsByTagName("ANO")[0].firstChild.nodeValue + "</td>";
			}
			catch (er){
				salida+= "<td>&nbsp;</td>";
			}
			salida+="</tr>";
		}
	}
	salida+="</table>";

	//reproductor
	srcVideo=document.getElementsByName("vid"); //selecciona el id del radiobutton seleccionado
	for (i=0;i<srcVideo.length;i++){
		if (srcVideo[i].checked){
			titulo=srcVideo[i].value;
			break;
		}
	}
	
	reproductor="<video id='video' width='500' src='./multimedia/video/"+titulo+"' type='video/mp4' onmouseover='document.getElementById('todo').setAttribute('style','display:block');'>";
	reproductor+="</video>";
	reproductor+="<div id='todo'>";
	reproductor+="<meter value='0' min='0' max='1' id='barra'></meter>";
	reproductor+="<div id='tiempo'>00:00 / 00:00</div>";
	reproductor+="<div id='botones'>";
	reproductor+="<input type='button'class='atrasar' id='atr' value='<<' onclick='atrasarVideo()'>";
	reproductor+="<input type='button'class='play' id='reproductor1' value='Play/Pause' onClick='reproduceVideo(this.id)'>";
	reproductor+="<input type='button'class='adelantar' id='ade' value='>>' onclick='adelantarVideo()'>";
	reproductor+="<input type='button'class='menos' id='menos' value='-' onclick='bajarVideo()'>";
	reproductor+="<input type='button'class='mas' id='mas' value='+' onclick='subirVideo()'>";
	reproductor+="<input type='button'class='silencio' id='silencio' value='Mute' onclick='muteVideo()'>";
	reproductor+="<input type='button' class='nosilencio' id='nosilencio' value='No Mute' onclick='noMuteVideo()'>";
	reproductor+="</div>";
	reproductor+="</div>";
	document.getElementById("reproductorVideo").innerHTML=reproductor; //muestro el contenido de la select
	document.getElementById("tablaVideo").innerHTML=salida; //muestro el contenido de la select
}

//funcion radio buttons para la tabla
function getRadioValue(theRadioGroup){
    var elements = document.getElementsByName(theRadioGroup);
    for (var i = 0; i < elements.length; i++){
        if (elements[i].checked){
            return elements[i].value;
        }
    }
}

//funcion que reproduce o pausa un video
function reproduceVideo(id){
	reproductor = document.getElementById('video');
	boton = document.getElementById(id);
	if(reproductor.paused){
		reproductor.play();
		var derp = setInterval(
			function(){
				document.getElementById('tiempo').innerHTML=formatTime(reproductor.currentTime) + " / " + formatTime(reproductor.duration);
				current=reproductor.currentTime/reproductor.duration;
				document.getElementsByTagName('meter')[0].setAttribute('value',current);					
			},100);				
	}else{
		reproductor.pause();
		clearInterval(derp)
	}		
}

function formatTime(seconds) {
	minutes = Math.floor(seconds / 60);
	minutes = (minutes >= 10) ? minutes : "0" + minutes;
	seconds = Math.floor(seconds % 60);
	seconds = (seconds >= 10) ? seconds : "0" + seconds;
	return minutes + ":" + seconds;
}

//funcion para adelantar 
function adelantarVideo(){
	document.getElementById("video").currentTime = document.getElementById("video").currentTime+10;
}

//funcion para atrasar
function atrasarVideo(){
	document.getElementById("video").currentTime = document.getElementById("video").currentTime-10;
}

//funcion para subir el volumen
function subirVideo(){
	document.getElementById("video").volume+=0.1;
}

//funcion para bajar el volumen
function bajarVideo(){
	document.getElementById("video").volume-=0.1;
}

//funcion para poner el volumen en mute
function muteVideo(){
	if(document.getElementById("video").muted){
		document.getElementById("video").muted=false;
	}else{
		document.getElementById("video").muted=true;
	}
}

//funcion para quitar el mute
function noMuteVideo(){
	document.getElementById('video').muted=false;
}