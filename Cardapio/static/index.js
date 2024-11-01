// const imageFolder = '/static/img/';
    
// // Número total de imagens (1 a 10)
// var tamanhoImagens = document.querySelector(".lenArquivos").innerHTML;
// tamanhoImagens -= 1;
// const totalImages = tamanhoImagens
// // Seleciona o contêiner onde as imagens serão exibida
// // Itera sobre os contêineres de imagem gerados por Jinja

//   for (let i = 1; i <= totalImages; i++) {


// // Seleciona o contêiner de imagem atual baseado no loop index
//     const imageContainer = document.getElementById(`image-container-${i}`);
//     const imageUrl = `${imageFolder}${i}.jpg`
// // Cria um novo elemento <img>
//     const img = document.createElement('img');
//     img.src = imageUrl;  // Define o caminho da imagem
//     img.alt = `Imagem ${i}`;  // Define o texto alternativo
//     img.style.width = '200px';
//     img.style.height = '200px'  // Define o tamanho da imagem (opcional
// // Adiciona a imagem ao contêiner
//     imageContainer.appendChild(img);
//   }




  const imageFolder = '/static/img/';

// Função para buscar a lista de imagens
async function carregarImagens() {
  try {
    const response = await fetch('/imagens');
    const imagens = await response.json();
    console.log(imagens)


    imagens.sort((a, b) => {
      // Extrai os números dos nomes dos arquivos
      const numA = parseInt(a.match(/\d+/), 10);
      const numB = parseInt(b.match(/\d+/), 10);
      return numA - numB;
    });

    imagens.forEach((nomeArquivo, index) => {
      // Seleciona o contêiner de imagem com base no índice (ou crie um novo)
      const imageContainer = document.getElementById(`image-container-${index + 1}`);
      if (imageContainer) {
        const imageUrl = `${imageFolder}/${nomeArquivo}`;

        // Cria um novo elemento <img>
        const img = document.createElement('img');
        img.src = imageUrl;          // Define o caminho da imagem
        img.alt = `Imagem ${index + 1}`;  // Define o texto alternativo
        img.style.width = '200px';
        img.style.height = '200px';  // Define o tamanho da imagem

        // Adiciona a imagem ao contêiner
        imageContainer.appendChild(img);
      }
    });
  } catch (error) {
    console.error('Erro ao carregar as imagens:', error);
  }
}

// Chama a função para carregar as imagens ao carregar a página
carregarImagens();