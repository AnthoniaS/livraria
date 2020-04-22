new Vue({
  el: "#app",
  data() {
    return {
      livros: null,
      livro: {
        id: null,
        nome: null,
        autor: null,
        edicao: null,
        ano: null,
        paginas: null,
      },
      filtro: "",
      erros: [],
    };
  },
  mounted() {
    this.listar();
  },
  methods: {
    listar() {
      axios
        .get("http://127.0.0.1:5000/livros")
        .then((response) => (this.livros = response.data));
      this.filtro = "";
    },

    salvar() {
      if (!this.verificaForm()) {
        return;
      }
      if (this.livro.id) {
        axios
          .put(`http://127.0.0.1:5000/livros/${this.livro.id}`, this.livro)
          .then((response) => {
            alert(`Seu Livro Foi Alterado com Sucesso!!`);
            this.listar();
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/livros", this.livro)
          .then((response) => {
            alert(`Seu Livro Foi Cadastrado com Código: ${response.data.id}`);
            this.listar();
          });
      }
      this.livro = {};
    },

    editar(id) {
      axios
        .get("http://127.0.0.1:5000/livros/" + id)
        .then((response) => (this.livro = response.data));
      this.$refs.nome.focus();
    },

    excluir(id, nome) {
      if (confirm(`Confirma exclusão do livro '${nome}'?`)) {
        axios.delete("http://127.0.0.1:5000/livros/" + id).then((response) => {
          alert(`O Livro '${nome}' foi excluído com sucesso!`);
          this.listar();
        });
      }
    },

    pesquisar() {
      if (this.filtro.length == 0) {
        this.listar();
      } else {
        axios
          .get(`http://127.0.0.1:5000/livros/pesq/${this.filtro}`)
          .then((response) => (this.livros = response.data));
      }
    },

    verificaForm() {
      // limpa vetor de erros
      this.erros = [];
      if (
        this.livro.nome &&
        this.livro.autor &&
        this.livro.edicao &&
        this.livro.ano &&
        this.livro.paginas
      ) {
        return true;
      }

      if (!this.livro.nome) {
        this.erros.push("Nome do livro é obrigatório.");
      }
      if (!this.livro.autor) {
        this.erros.push("Autor é obrigatório.");
      }
      if (!this.livro.edicao) {
        this.erros.push("Edição é obrigatório.");
      }
      if (!this.livro.ano) {
        this.erros.push("Ano é obrigatório.");
      }
      if (this.livro.paginas) {
        this.erros.push("A quantidade de páginas dos livros é obrigatória");
      }
      return false;
    },
  },
  /**
  filters: {
    formataNota(value) {
      return value.toFixed(1);
    },
    formataDuracao(value) {
      var hora = parseInt(value / 60);
      var min = value % 60;
      if (hora == 0) {
        return `${min}min`;
      } else if (min == 0) {
        return `${hora}h`;
      } else {
        return `${hora}h${min}min`;
      }
    },
  },
  */
});
