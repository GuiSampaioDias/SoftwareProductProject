const imageFolder = '/static/img/';
    
// Número total de imagens (1 a 10)
const tamanhoImagens = document.querySelector(".lenArquivos").innerHTML;
  const totalImages = tamanhoImagens
// Seleciona o contêiner onde as imagens serão exibida
// Itera sobre os contêineres de imagem gerados por Jinja
  for (let i = 1; i <= totalImages; i++) {
// Seleciona o contêiner de imagem atual baseado no loop index
    const imageContainer = document.getElementById(`image-container-${i}`);
    console.log(i);
    const imageUrl = `${imageFolder}${i}.jpg`
// Cria um novo elemento <img>
    const img = document.createElement('img');
    img.src = imageUrl;  // Define o caminho da imagem
    img.alt = `Imagem ${i}`;  // Define o texto alternativo
    img.style.width = '200px';
    img.style.height = '200px'  // Define o tamanho da imagem (opcional
// Adiciona a imagem ao contêiner
    imageContainer.appendChild(img);
  }