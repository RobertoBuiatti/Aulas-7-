
imprime("Olá, mundo!")
imprime("Olá, mundo!", false)
// Função para imprimir texto na página
function imprime(texto, bl=true){
    let box = document.getElementById("box")
    box.innerHTML += texto + (bl ? "<br>" : "")
}

// variaveis, tipos de variaveis: number, string, boolean, array, object, function, null, undefined
let nome = "João"
let sobrenome = "Silva"
let idade = 30
let altura = 1.85
let casado = false
let veiculo = null
const cpf = "123456789" // const cpf = "Maria" // Erro: não é possível reatribuir uma constante

imprime( nome + " " + sobrenome )
idade += 1
imprime(`Nome: ${nome} ${sobrenome}. Idade: ${idade}`) // diferença entre as aspas é que as aspas crase permitem interpolação de variáveis

imprime("")
imprime("operadores matemáticos")
// operadores matemáticos: +, -, *, /, %, ** (exponenciação)
let num1 = 10
let num2 = 5
let soma = num1 + num2
let subtracao = num1 - num2
let multiplicacao = num1 * num2
let divisao = num1 / num2
let resto = num1 % num2
let potencia = num1 ** num2
imprime(`Soma: ${soma}`)
imprime(`Subtração: ${subtracao}`)
imprime(`Multiplicação: ${multiplicacao}`)
imprime(`Divisão: ${divisao}`)
imprime(`Resto: ${resto}`)
imprime(`Potência: ${potencia}`)

imprime("")
imprime("operadores de comparação")
// operadores de comparação: ==, ===, !=, !==, >, <, >=, <=
let a = 10
let b = "10"
let comparacaoIgual = (a == b) // compara valor
let comparacaoIdentico = (a === b) // compara valor e tipo
let comparacaoDiferente = (a != b) // compara valor
let comparacaoNaoIdentico = (a !== b) // compara valor e tipo
let comparacaoMaior = (a > b)
let comparacaoMenor = (a < b)
let comparacaoMaiorOuIgual = (a >= b)
let comparacaoMenorOuIgual = (a <= b)
imprime(`Comparação Igual: ${comparacaoIgual}`)
imprime(`Comparação Idêntico: ${comparacaoIdentico}`)
imprime(`Comparação Diferente: ${comparacaoDiferente}`)
imprime(`Comparação Não Idêntico: ${comparacaoNaoIdentico}`)
imprime(`Comparação Maior: ${comparacaoMaior}`)
imprime(`Comparação Menor: ${comparacaoMenor}`)
imprime(`Comparação Maior ou Igual: ${comparacaoMaiorOuIgual}`)
imprime(`Comparação Menor ou Igual: ${comparacaoMenorOuIgual}`)

imprime("")
imprime("operadores lógicos")
// operadores lógicos: && (AND), || (OR), ! (NOT)
let condicao1 = true
let condicao2 = false
let and = condicao1 && condicao2 // verdadeiro se ambos forem verdadeiros
let or = condicao1 || condicao2 // verdadeiro se pelo menos um for verdadeiro
let not = !condicao1 // inverte o valor da condição
imprime(`AND: ${and}`)
imprime(`OR: ${or}`)
imprime(`NOT: ${not}`)

imprime("")
imprime("operadores de atribuição")
// operadores de atribuição: =, +=, -=, *=, /=, %=, **=
let x = 10
x += 5 // x = x + 5
x -= 3 // x = x - 3
x *= 2 // x = x * 2
x /= 4 // x = x / 4
x %= 3 // x = x % 3
x **= 2 // x = x ** 2
imprime(`Atribuição: ${x}`)

imprime("")
imprime("operadores de incremento e decremento")
// operadores de incremento e decremento: ++, --
let y = 5
y++ // y = y + 1
y-- // y = y - 1
imprime(`Incremento: ${y}`) // 5
imprime(`Decremento: ${y}`) // 4

imprime("")
imprime("Estruturas de controle")
// estrutura de controle: if, else if, else, ?
let numero = 10
if (numero > 0 || numero === 0 && numero !== null) {
    imprime("Número positivo")
} else if (numero < 0) { // gambiarra com um if dentro do else resultando no else if
    imprime("Número negativo")
} else {
    imprime("Número é zero")
}

numero > 0 ? imprime("Número positivo") : imprime("Número não é positivo")

// array
imprime("")
imprime("Estruturas de dados")
let frutas = ["maçã", "banana", "laranja", "uva"]
imprime("Frutas: " + frutas.join(", ")) // join para transformar o array em string
imprime("Frutas: " + frutas) // imprime o array como string
let numeros = [1, 2, 3, 4, 5]
imprime("Números: " + numeros[0]) // acessa o primeiro elemento do array
imprime("Números: " + numeros[(numeros.length)-1]) // acessa o último elemento do array

//objeto
imprime("")
imprime("Objetos")
let pessoa = {
    nome: "Maria",
    idade: 25,
    profissao: "Desenvolvedora"
}

let pessoa1 = new Object() // outra forma de criar um objeto
pessoa1.nome = "Carlos"
pessoa1.idade = 28
pessoa1.profissao = "Designer"
pessoa1["nome"] = "Ana" // acessa a propriedade do objeto usando colchetes
pessoa1["idade"] = 22
pessoa1["profissao"] = "Gerente de Projetos"

imprime(`Nome: ${pessoa1.nome}, Idade: ${pessoa1.idade}, Profissão: ${pessoa1.profissao}`) // acessa as propriedades do objeto


imprime(`Nome: ${pessoa.nome}, Idade: ${pessoa.idade}, Profissão: ${pessoa.profissao}`) // acessa as propriedades do objeto
imprime(`Nome: ${pessoa["nome"]}, Idade: ${pessoa["idade"]}, Profissão: ${pessoa["profissao"]}`) // acessa as propriedades do objeto usando colchetes

// new objeto e constructor
imprime("Criando objetos com constructor")
function Carro(marca, modelo, ano) {
    this.marca = marca;
    this.modelo = modelo;
    this.ano = ano;
}
Carro.prototype.exibirInfo = function() {
    return `Marca: ${this.marca}, Modelo: ${this.modelo}, Ano: ${this.ano}`;
}
let carro1 = new Carro("Toyota", "Corolla", 2020);
let carro2 = new Carro("Honda", "Civic", 2021);


imprime("")
imprime("Estruturas de repetição")
// estrutura de repetição: for, while, do while
for (let i = 0; i < 5; i++) {
    imprime(`For: ${i}`)
}

for ( let i = 0; i < frutas.length; i++ ) {
    imprime(`For com array: ${frutas[i]}`)
}

imprime("For of e For in")
// for of e for in a diferença é que o for of itera sobre os valores do array, enquanto o for in itera sobre os índices do array
for (let fruta of frutas) {
    imprime(`For of: ${fruta}`)
}

for (let indice in frutas) {
    imprime(`For in: ${indice} - ${frutas[indice]}`)
}

let j = 0

while (j < 5) {
    imprime(`While: ${j}`)
    j++
}

let k = 0

do {
    imprime(`Do While: ${k}`)
    k++
}while (k < 5);

imprime("")
imprime("Switch case")
// estrutura de controle switch case
let dia = 3
switch (dia) {
    case 1:
        imprime("Domingo")
        break
    case 2:
        imprime("Segunda-feira")
        break
    case 3:
        imprime("Terça-feira")
        break
    case 4:
        imprime("Quarta-feira")
        break
    case 5:
        imprime("Quinta-feira")
        break
    case 6:
        imprime("Sexta-feira")
        break
    case 7:
        imprime("Sábado")
        break
    default:
        imprime("Dia inválido")
}

switch (dia) {
    case 1:
    case 7:
        imprime("Fim de semana")
        break
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
        imprime("Dia da semana")
        break
    default:
        imprime("Dia inválido")
}