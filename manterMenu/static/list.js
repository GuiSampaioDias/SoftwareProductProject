function funcao1(itemIndex) {
    var r = confirm("Tem certeza que deseja excluir esse produto?");
    if (r == true) {
        window.location.href = "/produto/delete/" + itemIndex;
    } else {
        document.getElementById("demo").innerHTML = "Você pressionou Cancelar!";
    }
}

function funcao2(itemIndex) {
    var r = confirm("Tem certeza que deseja excluir esse produto?");
    if (r == true) {
        window.location.href = "/produto/delete/" + itemIndex;
    } else {
        document.getElementById("demo").innerHTML = "Você pressionou Cancelar!";
    }
}