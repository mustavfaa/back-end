axios.defaults.xsrfHeaderName = 'X-CSRFToken';
Vue.component('vue-multiselect', window.VueMultiselect.default);
Vue.config.devtools = true;

Vue.component('form-boocks', {
  props: ['datamodel', 'index'],
  delimiters: ["{(", ")}"],
  data: function () {
    return {

    }
  },
  template: '#form-boocks'
});

new Vue({
  el: "#appBoock",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      download: true,
      getss: false,
      ru: true,
      kk: false,
      token: '',
      display: 'None',
      name: '',
      publisher: '',
      author: '',
      publish_date: '',
      klass: '',
      language: '',
      series_by_year: '',
      subject: '',
      computeMyBind: 0,
      computeMyBind1: 0,
      metodology_complex: '',
      study_direction: '',
      boocks: [],
      languages: [],
      klasss: [],
      subjects: [],
      editions: [],
      years: [],
      authors: [],
      publishers: [],
      metodology_complexs: [],
      study_directions: []
    }
  },

  components: {
    multiselect: VueMultiselect.Multiselect
  },

  mounted() {
    const el = document.getElementById('token');
    // const self = this;
    if (urlLanguage === '/kk/') {
      this.kk = true
      this.ru = false
    }
    // var token = el.dataset.token;
    // this.token = token
    axios
      .get(
          document.location.href, {
          params: {
            all: true
          }
        }).then(response => {
            this.boocks = response.data.books,
            this.languages = response.data.languages,
            this.klasss = response.data.klasss,
            this.subjects = response.data.subjects,
            this.editions = response.data.editions.filter(function (item) {
                if (response.data.number_books.indexOf(item.id) > -1) {
                    return item
                }
            }),
            this.years = response.data.years,
            this.authors = response.data.authors,
            this.publishers = response.data.publishers,
            this.metodology_complexs = response.data.metodology_complex,
            this.study_directions = response.data.study_direction,
            this.download = false,
            this.getss = true,
            window.setTimeout(show_popup, 2000)
      })
      .catch(function (error) {
        console.log(error);
      })

  },

  computed: {
    filterNames: function () {
      var all = this.boocks;
      this.computeMyBind = 0
          this.computeMyBind1 = 0
      filter = {
        edition: {}
      };

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
          filter.edition.name = this.name.edition.name;
        }
        if (this.klass) {
          filter.edition.klass = this.klass.name;
        }
        if (this.language) {
          filter.edition.language = this.language.name;
        }
        if (this.subject) {
          filter.edition.subject = this.subject.name;
        }
        if (this.series_by_year) {
          filter.edition.series_by_year = this.series_by_year.year;
        }
        if (this.publish_date) {
          filter.edition.publish_date = this.publish_date.year;
        }
        if (this.publisher) {
          filter.edition.publisher = this.publisher.name;
        }
        if (this.author) {
          filter.edition.author = this.author.name;
        }
        if (this.metodology_complex) {
          filter.edition.metodology_complex = this.metodology_complex.name;
        }
        if (this.study_direction) {
          filter.edition.study_direction = this.study_direction.name;
        }
        Object.keys(filter.edition).forEach(
          key => filter.edition[key] == null && delete filter.edition[key]
        );
        all = _.filter(all, filter);

        all.forEach(item => {
          this.computeMyBind += item.summ
          this.computeMyBind1 += item.in_warehouse
        })
        return all;
      } else {
        all.forEach(item => {
          this.computeMyBind += item.results.summ
          this.computeMyBind1 += item.results.quantity
        })
        return all;
      }
    }
  },

  methods: {
    nameKlass({
      name
    }) {
      var names = name.slice(0, 7)
      return `${names}`
    },

    nameWithLang(option) {
      return `${option.edition.name}`
    },


    cLear: function () {
      this.name = '';
      this.klass = '';
      this.language = '';
      this.series_by_year = '';
      this.subject = '';
      this.author = '';
      this.publisher = '';
      this.publish_date = '';
      this.metodology_complex = '';
      this.study_direction = '';
    }
  },
});