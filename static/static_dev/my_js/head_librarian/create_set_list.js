axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

Vue.component("EditionsList", {
  props: ["datamodel", "index", "datas", "addfn"],
  template: "#editions-list",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      checked: false
    };
  },
});

new Vue({
  el: "#Appset",
  delimiters: ["{(", ")}"],
  data: {
    ru: true,
    kk: false,
    not: true,
    EditL: false,
    status: false,
    danger: false,
    worning: false,
    sucsess: false,
    addtitul: false,
    isDisabled: false,
    isDisabled1: false,
    time: '',
    token: "",
    klass: "",
    edition: "",
    language: "",
    datas: [],
    tituls: [],
    klasses: [],
    editions: [],
    languages: [],
    plan_tituls: [],
    addeditions: []
  },

  components: {
    multiselect: VueMultiselect.Multiselect
  },

  mounted() {
    const el = document.getElementById("token");
    if (urlLanguage === "/kk/") {
      this.kk = true;
      this.ru = false;
    }
    const self = this;
    var token = el.dataset.token;
    this.token = token;
    axios
      .get(
        urlLanguage + "cabinet/head_librarian/create_sets/api/?token=" + token
      )
      .then(
        response => (
          (self.languages = response.data.languages),
          (self.klasses = response.data.klasss),
          (self.editions = response.data.editions),
          (self.plan_tituls = response.data.tituls),
          (self.not = false)
        )
      )
      .catch(function (error) {
        console.log(error);
      });
  },

  computed: {
    filterTituls() {
      var all = this.plan_tituls;
      if (this.klass || this.language) {
        filter = {};
        if (this.klass) {
          filter.klass = Number(this.klass.id);
        }
        if (this.language) {
          filter.language = this.language;
        }
        all = _.filter(all, filter);
        return all;
      } else {
        return all;
      }
    },

    filterEditions() {
      var all = this.editions;
      if (this.klass || this.language || this.edition) {
        filter = {};
        if (this.klass) {
          filter.klass = this.klass.name;
        }
        if (this.language) {
          filter.language = this.language.name;
        }
        if (this.edition) {
          filter.name = this.edition.name;
        }
        all = _.filter(all, filter);
        return all;
      } else {
        return all;
      }
    }
  },

  methods: {
    addEdition(id) {
      var all = this.addeditions;
      if (this.addeditions.length > 0) {
        if (
          all.every(function (obj) {
            return obj != id;
          })
        ) {
          this.addeditions.push(id);
        } else this.addeditions.pop(id);
      } else {
        this.addeditions.push(id);
      }
    },

    addTitul: function (id, value) {
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time = datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      item = {
        plan_title: id,
        amount: value
      };
      var all = this.tituls;
      if (this.tituls.length > 0) {
        if (
          all.every(function (obj) {
            return obj.plan_title != item.plan_title;
          })
        ) {
          this.tituls.push(item);
        } else this.tituls.pop(item);
      } else {
        this.tituls.push(item);
      }
      if (this.tituls.length > 0) {
        this.addtitul = true
      } else {
        this.addTitul = false
      }

    },

    postAll() {
      const self = this
      var all = [];
      var index = 0
      this.tituls.forEach(klass => {
        if (index != klass.plan_title) {
          this.addeditions.forEach(edition => {
            all.push({
              plan_title: klass.plan_title,
              edition: edition,
              amount: klass.amount
            });
          });
          index = klass.plan_title
        }
      });
      data = {
        token: this.token,
        sets: all
      }
      axios
        .post(urlLanguage + "cabinet/head_librarian/create_sets/api/", data)
        .then(function (response) {
          self.danger = false;
          self.sucsess = true;
        })
        .catch(function (error) {
          self.sucsess = false;
          self.danger = true;
        });
    },

    nameWithLang({
      name
    }) {
      return `${name.slice(0, 7)}`;
    },

    onSelect(option) {
      if (option) this.isDisabled = true;
    },

    onSelect1(option) {
      if (option) this.isDisabled1 = true;
    },

    onClear() {
      this.isDisabled = false;
      this.isDisabled1 = false;
      this.datas = [];
      this.klass = "";
      this.language = "";
    }
  }
});

Vue.component("ClassList", {
  props: ["item", "index", "addfn", "cLear"],
  template: "#class-list",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      checked: false
    };
  },

  methods: {
    onclick() {
      this.checked = true
      if (this.$emit('clickCheck')) {
        console.log('tag', '11')
      }
    }
  },

});