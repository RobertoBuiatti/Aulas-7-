let mensagens = document.getElementById("mensagens")
let txtMsg = document.querySelector("#txtMsg")
let btnEnviar = document.querySelector("#btnEnviar")
// inserir texto
// mensagens.innerHTML = "Olá, Mundo!"
// mensagens.innerHTML += "<h1>Olá, Mundo!</h1>"

// alterar o stilo
mensagens.style.backgroundColor = "black"
mensagens.style.color = "white"

btnEnviar.addEventListener("click", enviarMensagem)

let pos = "esquerda"

function enviarMensagem() {
    let msg = txtMsg.value
    mensagens.innerHTML += `<div class = "balao">${msg}</div>`
    alert(msg)
}