axios.defaults.xsrfHeaderName = 'X-CSRFToken';
Vue.component('vue-multiselect', window.VueMultiselect.default);


//Компонент таблицы
Vue.component('blog-item', {
  delimiters: ["{(", ")}"],
  props: ['item', 'index', 'tokens', 'language', 'study', 'klass', 'data', 'liters'],
  template: '#boocks-template',
  data: function () {
    return {
      showModal: false,
    }
  }
});


//компонент модуля
Vue.component('blog-post', {
  delimiters: ["{(", ")}"],
  props: ['item', 'token', 'languages', 'directions', 'klasss', 'datas', 'liters'],

  components: {
    multiselect: VueMultiselect.Multiselect
  },

  data: function () {
    return {
      schoolTitulForm: {
        klass: this.item.klass,
        liter: this.item.liter,
        students: this.item.students,
        year: this.item.year,
        language: this.item.language,
        study_direction: this.item.study_direction
      }
    }
  },
  template: '#modal-template',
});



new Vue({
  el: "#appS",
  delimiters: ["{(", ")}"],
  data: {
    token: "",
    schoolTitul: [],
    liters: [],
    languages: [],
    studyDirections: [],
    klasss: [],
    datas: [],
    amaunt: '',
    schoolTitulForm: {
      klass: 0,
      liter: 0,
      students: 0,
      year: 0,
      language: 0,
      study_direction: 0
    }
  },

  components: {
    multiselect: VueMultiselect.Multiselect
  },

  methods: {

    computeMyBind() {
      var sum = this.schoolTitul.reduce(function (acc, equity) {
        return acc + parseInt(equity.students);
      }, 0);
      return sum;
    },

  },

  computed: {
    isComplete() {
      return this.schoolTitulForm.klass && this.schoolTitulForm.liter && this.schoolTitulForm.students && this.schoolTitulForm.year && this.schoolTitulForm.language && this.schoolTitulForm.study_direction;
    }
  },

  mounted() {
    const el = document.getElementById('token');
    var token = el.dataset.token;
    this.token = token
    const self = this;
    axios
      .get(
        urlLanguage + "cabinet/head_science/school_titul_list/", {
          headers: {
            token: self.token
          }
        })
      .then(response => (
        this.schoolTitul = response.data.data,
        this.languages = response.data.languages,
        this.studyDirections = response.data.studyDirections,
        this.klasss = response.data.klasss,
        this.datas = response.data.datas,
        this.liters = response.data.liters
      )).catch(function (error) {
        console.log(error);
      });
  }

});