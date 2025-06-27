document.addEventListener('DOMContentLoaded', function () {
    const iconeCurtir = document.querySelector('.like');
    const iconeComentar = document.querySelector('.comentar');
    const foto = document.querySelector('.foto img');
    const formularioComentario = document.querySelector('.formulario');
    const inputComentario = document.getElementById('txtComentario');
    const botaoComentar = document.getElementById('btnComentar');
    const listaComentarios = document.querySelector('.comentarios');

    let curtido = false;

    formularioComentario.style.display = 'none';

    function alternarCurtir() {
        curtido = !curtido;
        iconeCurtir.src = curtido ? 'icones/coracao_red.png' : 'icones/coracao.png';
    }

    iconeCurtir.addEventListener('click', alternarCurtir);

    foto.addEventListener('dblclick', function () {
        if (!curtido) {
            alternarCurtir();
        }
    });

    iconeComentar.addEventListener('click', function () {
        if (formularioComentario.style.display === 'none') {
            formularioComentario.style.display = 'flex';
            inputComentario.focus();
        } else {
            formularioComentario.style.display = 'none';
        }
    });

    function adicionarComentario(texto) {
        if (!texto.trim()) return;
        const divComentario = document.createElement('div');
        divComentario.className = 'comentario';

        const spanAutor = document.createElement('span');
        spanAutor.textContent = 'Seu Nome';

        const pComentario = document.createElement('p');
        pComentario.textContent = texto;

        divComentario.appendChild(spanAutor);
        divComentario.appendChild(pComentario);

        listaComentarios.appendChild(divComentario);
    }

    botaoComentar.addEventListener('click', function () {
        adicionarComentario(inputComentario.value);
        inputComentario.value = '';
        inputComentario.focus();
    });

    inputComentario.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            botaoComentar.click();
        }
    });
});
