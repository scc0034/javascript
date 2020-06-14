function comienza(){
//Creamos el objeto
	xhr= new objetoXHR();
//Comprobamos que lo ha creado
	if(xhr){
		xhr.open('GET','datos.xml',true);//true==asincrono
		//Escuchamos el estado de la peticion
		xhr.onreadystatechange=escucharesumida;
		
		//Enviamos la consulta (en este caso no hacemos ninguna consulta porque el phph solo devuelve la fecha)
		xhr.send();
	}
}//fin de la funcion comienza


function escucharesumida(){
	if(xhr.readyState==4){
		if((xhr.status==200) ||(xhr.status==304)){
		//Llamada a la funcion que recorre el docmento XML
		datos=xhr.responseXML;
		recorrePintores();
		}else{
			alert("Ha habido un error");
		}
	}
}//Fin de la funcion



//Funcion para recorrrer el XML
function recorrePintores(){

pintores=datos.documentElement.getElementsByTagName("PINTORES");
cadena="";
array_anos= new Array();
	try{
	cadena+="<select id='pintores'  onclick='mostrarDatos();'>";
		for (i=0;i<pintores.length;i++){ 
		nombre=pintores[i].getElementsByTagName("ARTIST");
		cadena+="<option value='"+nombre[0].firstChild.nodeValue+"'>"
		+nombre[0].firstChild.nodeValue+"</option>";
		}//Fin del for
	

	}catch(er){
	
	}//fin del try
	cadena+="</select>";
		document.getElementById('desplegablePintores').innerHTML=cadena;
}//Fin de la funcion

function mostrarDatos(){
	//obtengo el dato pasado por el boton seleccionar
	pintor=document.getElementById("pintores").value;

	texto2="";
	document.getElementById("datosPintor").innerHTML="";
	//comparo este dato con todo lo que hay dentro del archivo xml
	for(i=0;i<pintores.length;i++){
		obra=pintores[i].getElementsByTagName("OBRA");
		anio=pintores[i].getElementsByTagName("ANO");
		ruta=pintores[i].getElementsByTagName("RUTA");
		valor=datos.getElementsByTagName('ARTIST')[i].childNodes[0].nodeValue;
		
			if(pintor==valor){
				texto2="";
				//artista=datos.getElementsByTagName('ARTIST')[i].childNodes[0].nodeValue;	
				//precio=datos.getElementsByTagName('PRICE')[i].childNodes[0].nodeValue;	
				texto2+="<b>Artista</b>: "+ pintor+"<b> Obra</b>: "+ obra[0].firstChild.nodeValue+
				"<b> Año</b>:"+ anio[0].firstChild.nodeValue+"<br>";
				texto2+="<img src='"+ruta[0].firstChild.nodeValue+"' heigth='300' width='300'/>"
				document.getElementById("datosPintor").innerHTML+=texto2;
					
			}//fin de if
			
		}//fin del for
	
}//Fin de la funcion








/*function escucha(){
	switch(xhr.readyState){
		case 0: document.getElementById('estado').innerHTML+="Petición sin inicializar</br>";
		break;
		case 1: document.getElementById('estado').innerHTML += "1 Petición abierta.<br/>";
		break;
		case 2: document.getElementById('estado').innerHTML += "2 Cargado.<br/>";
		break;
		case 3: document.getElementById('estado').innerHTML += "3 Cargando.<br/>";
		break;
		case 4: document.getElementById('estado').innerHTML += "4 Completado.";
			//Comprobamos que ha recibido la informacion correctamente
			if((xhr.status==200) ||(xhr.status==304)){
				document.getElementById('resultados').innerHTML=xhr.responseText;
			}else{
				alert("Ha habido un error");
			}
		break;
	}
}//fin de la funcion escucha*/