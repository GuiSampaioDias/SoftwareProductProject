function funcao1(itemIndex) {
    var r = confirm("Tem certeza que deseja excluir esse produto?");
    if (r == true) {
        window.location.href = "/produto/delete/" + itemIndex;
    } else {
        document.getElementById("demo").innerHTML = "Você pressionou Cancelar!";
    }
}

function funcao2(itemIndex) {
<<<<<<< HEAD
    var r = confirm("Tem certeza que deseja excluir essa categoria?");
    if (r == true) {
        window.location.href = "/excluir_categoria/" + itemIndex;
=======
    var r = confirm("Tem certeza que deseja excluir esse produto?");
    if (r == true) {
        window.location.href = "/produto/delete/" + itemIndex;
>>>>>>> 709298c71b4ed5010b5a2ac875b37e532d9c027d
    } else {
        document.getElementById("demo").innerHTML = "Você pressionou Cancelar!";
    }
}