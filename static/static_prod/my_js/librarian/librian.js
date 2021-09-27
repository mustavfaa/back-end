axios.defaults.xsrfHeaderName = 'X-CSRFToken';
new Vue({
el: "#app",
delimiters: ["{(", ")}"],
data: {
  token: "",
  numberBooks: [],
  itemform: {
    id: 0,
    school: 1,
    edition: 0,
    on_hands: 0,
    in_warehouse: 0
  }
},
methods: {
  remove: function(index, item) {
    self = this
    // this.numberBooks.splice(index, 1);
    axios({
      method: 'DELETE',
      url: '/cabinet/librarian/api/books/delete/' + item.id,
      data: {token: self.token},
      headers: {'Content-Type': 'application/json'}
    }).then(function (response) {
      self.numberBooks.splice(index, 1);
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  },
  computeMyBind() {
    var sum = this.numberBooks.reduce(function(acc, equity) {
      return acc + parseInt(equity.on_hands);
    }, 0);
    return sum;
  },
  computeMyBind1() {
    var sum = this.numberBooks.reduce(function(acc, equity) {
      return acc + parseInt(equity.in_warehouse);
    }, 0);
    return sum;
  },
  aAdd() {
    const self = this;
    data1 = {
      token: this.token,
      on_hands: Number(this.itemform.on_hands),
      in_warehouse: Number(this.itemform.in_warehouse),
      ammaut: {
          on_hands: this.computeMyBind(),
          in_warehouse: this.computeMyBind(),
          amaunts:  Number(this.computeMyBind() + this.computeMyBind())
      }
    };
    console.log(data1.ammaut.amaunts);
    axios.post('/cabinet/librarian/api/books/add/', data1).then(function (response) {
       self.numberBooks = response.data;
  })
  .catch(function (error) {
    console.log(error);
  })
  }
},
mounted() {
  const el = document.getElementById('token');
  var token = el.dataset.token;
  this.token = token
  const self = this;
  axios
    .get(
      "/cabinet/librarian/api/books/?token=" + token
    )
    .then(response => (this.numberBooks = response.data)).catch(function (error) {
    console.log(error);
  });
}
});
