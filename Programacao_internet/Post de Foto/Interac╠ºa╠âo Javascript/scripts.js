document.addEventListener('DOMContentLoaded', function () {
    const iconeCurtir = document.querySelector('.like');
    const iconeComentar = document.querySelector('.comentar');
    const foto = document.querySelector('.foto img');
    const formularioComentario = document.querySelector('.formulario');
    const inputComentario = document.getElementById('txtComentario');
    const botãoComentar = document.getElementById('btnComentar');
    const listaComentários = document.querySelector('.comentarios');

    let curtido = false;

    formularioComentario.style.display = 'none';
    listaComentários.style.display = 'none';

    function alternarCurtir() {
        curtido = !curtido;
        iconeCurtir.src = curtido ? 'icones/coracao_red.png' : 'icones/coracao.png';
    }

    iconeCurtir.addEventListener('click', alternarCurtir);

    foto.addEventListener('click', function () {
        alternarCurtir();
    });

    iconeComentar.addEventListener('click', function () {
        const comentariosVisiveis = listaComentários.style.display !== 'none';
        if (comentariosVisiveis) {
            listaComentários.style.display = 'none';
            formularioComentario.style.display = 'none';
        } else {
            listaComentários.style.display = '';
            formularioComentario.style.display = 'flex';
            inputComentario.focus();
        }
    });

    function adicionarComentario(texto) {
        if (!texto.trim()) return;
        const divComentario = document.createElement('div');
        divComentario.className = 'comentario';

        const spanAutor = document.createElement('span');
        spanAutor.textContent = 'Roberto Buiatti';

        const pComentario = document.createElement('p');
        pComentario.textContent = texto;

        divComentario.appendChild(spanAutor);
        divComentario.appendChild(pComentario);

        listaComentários.appendChild(divComentario);
    }

    botãoComentar.addEventListener('click', function () {
        adicionarComentario(inputComentario.value);
        inputComentario.value = '';
        inputComentario.focus();
    });

    inputComentario.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            botãoComentar.click();
        }
    });
});
