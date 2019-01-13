$(document).ready(function(){
  $('.modal-link').on('click', function(){
    if(this.id == 'word-freq'){
      $('.modal-title').text("Diversidade Lexical");
      $('.modal-body').text(
        "Diversidade lexical é a medida da amplitude do vocabulário do autor. " +
        "Correspondendo à riqueza de vocabulário."
      );
    }
    else if(this.id == 'dist-lex'){
      $('.modal-title').text("Distribuição Lexical");
      $('.modal-body').text(
        "Através da distribuição lexical é possível saber quando ou onde certas " +
        "palavras foram usadas no texto"
      );
    }
    else if(this.id == 'tag-cloud'){
      $('.modal-title').text("Nuvem de Tags");
      $('.modal-body').text(
        "A nuvem de tags representa as palavras mais frequentes no texto. " +
        "O tamanho, a cor e a distribuição das palavras estão diretamente " +
        "relacionadas com a sua frequência."
      );
    }
    else if(this.id == 'treemap'){
      $('.modal-title').text("Treemap");
      $('.modal-body').text(
        "No treemap cada retângulo grande representa uma categoria (emoção), também " +
        "representada por diferentes cores. O tamanho do retângulo refere-se " +
        "à sua frequência no texto. Ao clicar em uma categoria é possível visualizar " +
        "suas subcategorias. Nesse caso, as palavras que denotam aquela emoção."
      );
    }
    else if(this.id == 'emo-dist'){
      $('.modal-title').text("Distribuição de Emoção ao Longo do Livro");
      $('.modal-body').text(
        "Este gráfico de dispersão mostra como as emoções estão distribuídas ao " +
        "longo do livro. Cada trecho analisado corresponde a 1000 palavras do texto."
      );
    }
  });
});
