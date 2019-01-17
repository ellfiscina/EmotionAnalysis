$(document).ready(function(){
  $('.modal-link').on('click', function(){
    if(this.id == 'word-freq'){
      $('.modal-title').text("Diversidade Lexical");
      $('.modal-body').text(
        "Diversidade lexical é a medida da amplitude do vocabulário do autor, " +
        "correspondendo à sua riqueza de vocabulário. Em outras palavras, é a " +
        "quantidade de tokens únicos em relação ao total de tokens no livro."
      );
    }
    else if(this.id == 'dist-lex'){
      $('.modal-title').text("Distribuição Lexical");
      $('.modal-body').text(
        "Através da distribuição lexical é possível saber quando ou onde certas " +
        "palavras foram usadas no texto. Nesta visualização, cada linha representa " +
        "uma instância da palavra, e o eixo x representa o texto inteiro. As cinco " +
        "palavras escolhidas são as mais frequentes no texto."
      );
    }
    else if(this.id == 'tag-cloud'){
      $('.modal-title').text("Nuvem de Tags");
      $('.modal-body').text(
        "A nuvem de tags representa as palavras mais frequentes no texto. " +
        "O tamanho, a cor e a distribuição das palavras estão diretamente " +
        "relacionadas com a sua frequência.\n" +
        "A nuvem em formato de espiral dispõe as palavras mais frequentes no centro " +
        "e as menos frequentes na parte mais externa. Além disso, palavras com a mesma " +
        "frequência são representadas pela mesma cor. Ao passar o mouse por cima da " +
        "palavra é possível ver ainda a quantidade de vezes que ela aparece no texto."
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
    else if(this.id == 'collocations'){
      $('.modal-title').text("Colocações");
      $('.modal-body').text(
        "Essencialmente, colocações são bigramas (pares de palavras) que ocorrem " +
        "com frequência maior do que a esperada, baseado na frequência das palavras " +
        "individualmente. As colocações que aparecem são muito específicas do gênero " +
        "do texto."
      );
    }
    else if(this.id == 'concordance'){
      $('.modal-title').text("Concordância");
      $('.modal-body').text(
        "A concordância refere-se ao contexto das ocorrências de uma dada palavra. " +
        "A palavra escolhida é a mais frequente do texto que remete a uma emoção."
      );
    }
    else if(this.id == 'n-grams'){
      $('.modal-title').text("5-Grams");
      $('.modal-body').text(
        "N-grams de um texto são conjuntos de palavras co-ocorrentes, de forma que n " +
        "é a quantidade de palavras na sentença."
      );
    }
    else if(this.id == 'treeword'){
      $('.modal-title').text("Árvore de Palavras");
      $('.modal-body').text(
        "Essa visualização permite observar o contexto de determinada palavra. " +
        "Duas palavras foram escolhidas: a primeira (marcada em verde) corresponde " +
        "ao token mais frequente no texto; enquanto a segunda (roxo) refere-se à " +
        "palavra remetente a uma emoção que mais se repete."
      );
    }
  });
});
