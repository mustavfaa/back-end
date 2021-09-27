axios.defaults.xsrfHeaderName = 'X-CSRFToken';

//Компонент таблицы
Vue.component('blog-item', {
  delimiters: ["{(", ")}"],
  props: ['item', 'index', 'removefn', 'edit', 'tokens'],
  template: '#boocks-template',
  data: function () {
    return {
      showModal: false
    }
  }
});


//компонент модуля
Vue.component('blog-post', {
  delimiters: ["{(", ")}"],
  props: ['item', 'token'],
  data: function () {
    return {
      fItem: {
        in_warehouse: null,
        on_hands: null
      }
    }
  },
  template: '#modal-template',
  methods: {
    eDit() {
      const self = this;
      data1 = {
        token: this.token,
        id: Number(this.item.id),
        edition: Number(this.item.edition.id),
        on_hands: Number(this.fItem.on_hands),
        in_warehouse: Number(this.fItem.in_warehouse),
      };
      axios.post('/cabinet/head_librarian/api/books/delete/' + self.item.id, data1).then(function (response) {
          // self.numberBooks = response.data;
          location.reload();
          self.$emit('close')
        })
        .catch(function (error) {
          console.log(error);
        })
    }
  }

});


new Vue({
  el: "#app",
  delimiters: ["{(", ")}"],
  data: {
    showModal: false,
    token: "",
    numberBooks: [],
    itemform: {
      id: 0,
      school: 1,
      edition: {},
      on_hands: 0,
      in_warehouse: 0
    }
  },
  methods: {
    remove: function (index, item) {
      self = this
      // this.numberBooks.splice(index, 1);
      axios({
          method: 'POST',
          url: '/cabinet/head_librarian/api/books/delete/' + item.id + '/',
          data: {
            token: self.token
          },
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          location.reload();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    computeMyBind() {
      var sum = this.numberBooks.reduce(function (acc, equity) {
        return acc + parseInt(equity.on_hands);
      }, 0);
      return sum;
    },
    computeMyBind1() {
      var sum = this.numberBooks.reduce(function (acc, equity) {
        return acc + parseInt(equity.in_warehouse);
      }, 0);
      return sum;
    },
    aAdd() {
      const self = this;
      data1 = {
        token: this.token,
        edition: Number(this.itemform.edition),
        on_hands: Number(this.itemform.on_hands),
        in_warehouse: Number(this.itemform.in_warehouse),
        ammaut: {
          on_hands: this.computeMyBind(),
          in_warehouse: this.computeMyBind(),
          amaunts: Number(this.computeMyBind() + this.computeMyBind())
        }
      };
      axios.post('/cabinet/head_librarian/api/books/add/demo/', data1).then(function (response) {
          // self.numberBooks = response.data;
          location.reload();
        })
        .catch(function (error) {
          console.log(error);
        })
    }
  },

  computed: {
    isComplete() {
      return this.itemform.edition && this.itemform.on_hands && this.itemform.in_warehouse;
    }
  },

  mounted() {
    const el = document.getElementById('token');
    var token = el.dataset.token;
    this.token = token
    const self = this;
    axios
      .get(
        urlLanguage + "cabinet/head_librarian/api/books/demo/?token=" + token
      )
      .then(response => (this.numberBooks = response.data)).catch(function (error) {
        console.log(error);
      });
  }
});