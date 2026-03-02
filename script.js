const video = document.getElementById('camera');

navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => video.srcObject = stream);

function baterPonto(){

let nome = document.getElementById("nome").value;
let data = new Date();

let hora = data.toLocaleString();

let registro = nome + " - " + hora;

let historico = JSON.parse(localStorage.getItem("pontos")) || [];

historico.push(registro);

localStorage.setItem("pontos", JSON.stringify(historico));

mostrarHistorico();

}

function mostrarHistorico(){
let lista = JSON.parse(localStorage.getItem("pontos")) || [];
document.getElementById("historico").innerHTML = lista.join("<br>");
}

mostrarHistorico();
