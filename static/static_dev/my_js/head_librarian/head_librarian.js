axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

Vue.component("form-boocks", {
  props: ["index", "datamodel", "ttt", "sucsess", "warning2"],
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      on_hands: false,
      in_warehouse: false
    };
  },
  template: "#form-boocks",

  methods: {
    getClassesHands: function () {
      if (
        this.ttt &&
        this.datamodel.on_hands === undefined &&
        this.datamodel.in_warehouse != undefined &&
        this.datamodel.in_warehouse > 0
      ) {
        return {
          "alert-inform": true
        };
      } else if (
        this.ttt &&
        this.datamodel.on_hands <= 0 &&
        this.datamodel.in_warehouse <= 0
      ) {
        return {
          "alert-inform": true
        };
      }
    },

    getClassesWarehouse: function () {
      if (
        this.ttt &&
        this.datamodel.in_warehouse === undefined &&
        this.datamodel.on_hands != undefined &&
        this.datamodel.on_hands > 0
      ) {
        return {
          "alert-inform": true
        };
      } else if (
        this.ttt &&
        this.datamodel.in_warehouse <= 0 &&
        this.datamodel.on_hands <= 0
      ) {
        return {
          "alert-inform": true
        };
      }
    }
  }
});

new Vue({
  el: "#appBoock",
  delimiters: ["{(", ")}"],
  components: {
    multiselect: VueMultiselect.Multiselect
  },

  data: function () {
    return {
      ru: true,
      kk: false,
      not: false,
      danger: false,
      sucsess: false,
      warning: false,
      ttt: false,
      time: "",
      name: "",
      token: "",
      klass: "",
      search: "",
      author: "",
      display: "None",
      language: "",
      subject: "",
      publisher: "",
      publish_date: "",
      series_by_year: "",
      study_direction: "",
      metodology_complex: "",
      years: [],
      klasss: [],
      boocks: [],
      authors: [],
      subjects: [],
      languages: [],
      publishers: [],
      study_directions: [],
      metodology_complexs: [],

    };
  },

  mounted() {
    const el = document.getElementById("token");
    const self = this;
    if (urlLanguage === "/kk/") {
      this.kk = true;
      this.ru = false;
    }
    var token = el.dataset.token;
    self.token = token;
    axios
      .get(urlLanguage + "cabinet/head_librarian/editions_list/", {
        headers: {
          token: self.token
        }
      })
      .then(
        response => (
          (self.boocks = response.data.books.filter(function (item) {
            if (!(response.data.number_books.indexOf(item.id) > -1)) {
              return item
            }
          })),
          (self.warning = response.data.warning),
          (self.languages = response.data.languages),
          (self.klasss = response.data.klasss),
          (self.subjects = response.data.subjects),
          (self.years = response.data.years),
          (self.authors = response.data.authors),
          (self.publishers = response.data.publishers),
          (self.metodology_complexs = response.data.metodology_complex),
          (self.study_directions = response.data.study_direction),
          (self.not = function () {
            if (response.data.books.length === 0) {
              return true;
            } else return false;
          })
        )
      )
      .catch(function (error) {
        self.not = true;
        console.log(error);
      });
  },

  computed: {
    filterNames: function () {
      var all = this.boocks;
      filter = {};

      if (
        this.klass ||
        this.name ||
        this.language ||
        this.subject ||
        this.series_by_year ||
        this.publish_date ||
        this.publisher ||
        this.author ||
        this.metodology_complex ||
        this.metodology_complex ||
        this.study_direction
      ) {
        if (this.name) {
          filter.name = this.name.name;
        }
        if (this.klass) {
          filter.klass = this.klass.name;
        }
        if (this.language) {
          filter.language = this.language.name;
        }
        if (this.subject) {
          filter.subject = this.subject.name;
        }
        if (this.series_by_year) {
          filter.series_by_year = this.series_by_year.year;
        }
        if (this.publish_date) {
          filter.publish_date = this.publish_date.year;
        }
        if (this.publisher) {
          filter.publisher = this.publisher.name;
        }
        if (this.author) {
          filter.author = this.author.name;
        }
        if (this.metodology_complex) {
          filter.metodology_complex = this.metodology_complex.name;
        }
        if (this.study_direction) {
          filter.study_direction = this.study_direction.name;
        }
        Object.keys(filter).forEach(
          key => filter[key] == null && delete filter[key]
        );
        all = _.filter(all, filter);
        return all;
      } else {
        return all;
      }
    }
  },

  methods: {

    Сomplete(){
      data = {
        token: this.token,
        close: 1
      }
    },

    nameKlass({
      name
    }) {
      var names = name.slice(0, 7)
      return `${names}`
    },

    aAdd() {
      const self = this;
      data1 = {
        token: this.token,
        books: this.boocks.filter(function (item) {
          if (
            (item.on_hands > 0 && item.in_warehouse > 0) ||
            (item.on_hands > 0 && item.in_warehouse >= 0) ||
            (item.on_hands >= 0 && item.in_warehouse > 0)
          ) {
            return item;
          }
        })
      };
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time =
        datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      data1.books.forEach(item => delete item.name);
      if (data1.books.length != 0) {
        this.sucsess = false;
        axios
          .post(urlLanguage + "cabinet/head_librarian/api/add/", data1)
          .then(function (response) {
            (
            function (){if(response.data.warning > 0){
              self.warning = false
              }
              else self.warning = true
            }),
            self.danger = false;
            self.sucsess = true;
            self.ttt = true;
            self.boocks = self.boocks.filter(function (item) {
              if (
                !item.on_hands ||
                !item.in_warehouse ||
                item.on_hands === 0 ||
                item.in_warehouse === 0
              ) {
                return item;
              }
            });
          })
          .catch(function (errors) {
            console.log(errors, 'fff')
            self.sucsess = false;
            self.danger = true;
          });
        // setTimeout(function(){
        //     self.sucsess = false;
        //     self.danger = false;
        //     self.ttt = false;
        // }, 5000);
      } else {
        this.sucsess = false;
        this.danger = true;
        this.ttt = true;
        // setTimeout(function(){
        //     self.sucsess = false;
        //     self.danger = false;
        //     self.ttt = false;
        // }, 5000);
      }
    },

    Get_books() {
      if (this.boocks.length == 0) {
        return (this.not = true);
      }
    },

    cLear: function () {
      this.name = "";
      this.klass = "";
      this.language = "";
      this.series_by_year = "";
      this.subject = "";
      this.author = "";
      this.publisher = "";
      this.publish_date = "";
      this.metodology_complex = "";
      this.study_direction = "";
    }
  }
});