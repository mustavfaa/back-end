axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

Vue.component("form-boocks", {
  props: ["index", "datamodel", "ttt", "sucsess", "warning2", "add"],
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      summ: false,
      in_warehouse: false
    };
  },
  template: "#form-boocks",

  methods: {

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
      number_books: [],
      study_directions: [],
      metodology_complexs: [],

    };
  },

  mounted() {

    axios
      .get(document.location.href, {
          params: {
              all: true
          }
      })
      .then(response => {
          (this.number_books = response.data.number_books),
          (this.boocks = response.data.books),
          (this.warning = response.data.warning),
          (this.languages = response.data.languages),
          (this.klasss = response.data.klasss),
          (this.subjects = response.data.subjects),
          (this.years = response.data.years),
          (this.authors = response.data.authors),
          (this.publishers = response.data.publishers),
          (this.metodology_complexs = response.data.metodology_complex),
          (this.study_directions = response.data.study_direction),
          (this.not = function () {
              if (response.data.books.length === 0) {
                  return true;
              } else return false;
          })
        }
      )
      .catch(function (error) {
        this.not = true;
        console.log(error);
      });
  },

  computed: {
    filterNames: function () {
      let ids = this.number_books
      let all  = this.boocks.filter(function (item) {
          if (!(ids.indexOf(item.id) != -1)){
              return item
          }
      })
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

    aAdd(item) {
      data = {
        add: true,
        book: {
          edition: item.id,
          summ: Number(item.summ),
          in_warehouse: Number(item.in_warehouse)
        }
      };
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time = datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      this.sucsess = false;
      axios
        .post(document.location.href, data)
        .then(response => {
          this.number_books.push(response.data.edition);
          this.danger = false;
          this.sucsess = true;
          this.ttt = true;
          console.log(response.data)
        })
        .catch(function (errors) {
          console.log(errors, 'fff')
          this.sucsess = false;
          this.danger = true;
        });

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