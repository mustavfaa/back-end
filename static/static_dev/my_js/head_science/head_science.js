axios.defaults.xsrfHeaderName = 'X-CSRFToken';
Vue.component('vue-multiselect', window.VueMultiselect.default);


//Компонент таблицы
Vue.component('blog-item', {
  delimiters: ["{(", ")}"],
  props: ['item', 'index', 'removefn', 'edit', 'tokens', 'language', 'study', 'klass', 'data', 'liters', 'userss', 'nameWithLangs', 'worning'],
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
  props: ['item', 'token', 'languages', 'directions', 'klasss', 'datas', 'liters', 'users', 'nameWithLang'],

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
        study_direction: this.item.study_direction,
        class_teacher: this.item.class_teacher

      }
    }
  },
  template: '#modal-template',
  methods: {
    eDit() {
      const self = this;
      data = {
        token: this.token,
        id: Number(self.item.id),
        klass: Number(self.schoolTitulForm.klass.id),
        liter: Number(self.schoolTitulForm.liter.id),
        students: Number(self.schoolTitulForm.students),
        year: Number(self.schoolTitulForm.year.id),
        language: Number(self.schoolTitulForm.language.id),
        study_direction: Number(self.schoolTitulForm.study_direction.id)
        // class_teacher: Number(self.schoolTitulForm.class_teacher.id)
      };
      axios.put(urlLanguage + 'cabinet/head_science/api/delete/' + self.item.id, data).then(function (response) {
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
  el: "#appS",
  delimiters: ["{(", ")}"],
  data: {
    send: false,
    worning: false,
    danger: false,
    warning1: false,
    token: "",
    amaunt: '',
    datas: [],
    users: [],
    liters: [],
    klasss: [],
    languages: [],
    schoolTitul: [],
    studyDirections: [],
    user: {
      last_name: "Имя",
      first_name: "Фамилия",
      username: "Email"
    },
    schoolTitulForm: {
      klass: '',
      liter: '',
      students: '',
      year: '',
      language: '',
      study_direction: '',
      user: ''
    }
  },

  components: {
    multiselect: VueMultiselect.Multiselect
  },

  methods: {
    cLear: function () {
      this.schoolTitulForm = {
        klass: {},
        liter: {},
        students: {},
        year: {},
        language: {},
        study_direction: {},
        class_teacher: {}
      }
    },

    nameKlass({
      name
    }) {
      var names = name.slice(0, 7)
      return `${names}`
    },

    nameWithLang({
      last_name,
      first_name,
      username
    }) {
      return `${last_name} ${first_name} / ${username}`;
    },

    remove: function (index, item) {
      self = this
      axios({
          method: 'DELETE',
          url: urlLanguage + 'cabinet/head_science/api/delete/' + item.id,
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
      var sum = 0
      this.filterNames.map(item => {
        sum = sum + item.students
        return item
      })
      return sum
    },

    aAdd() {
      this.send = true
      filter = {
        klass: this.schoolTitulForm.klass,
        language: this.schoolTitulForm.language,
        liter: this.schoolTitulForm.liter,
        year: this.schoolTitulForm.year,
        study_direction: this.schoolTitulForm.study_direction

      };

      if (_.filter(this.schoolTitul, filter).length >= 1) {
        this.danger = true
        this.send = false
      } else {
        this.danger = false
        const self = this;
        if (this.schoolTitulForm.klass &&
            this.schoolTitulForm.liter &&
            this.schoolTitulForm.students &&
            this.schoolTitulForm.year &&
            this.schoolTitulForm.language &&
            this.schoolTitulForm.study_direction
            // && this.schoolTitulForm.user
        ) {
          data1 = {
            token: this.token,
            klass: Number(this.schoolTitulForm.klass.id),
            liter: Number(this.schoolTitulForm.liter.id),
            students: Number(this.schoolTitulForm.students),
            year: Number(this.schoolTitulForm.year.id),
            language: Number(this.schoolTitulForm.language.id),
            study_direction: Number(this.schoolTitulForm.study_direction.id),
            // class_teacher: Number(this.schoolTitulForm.user.id)
          }
          axios.post(urlLanguage + 'cabinet/head_science/api/school_titul/add/', data1).then(function (response) {
              location.reload();
            })
            .catch(function (error) {
              console.log(error);
            })
        } else {
          this.worning = true

        }
      }
    },
  },

  computed: {
    filterNames() {
      var all = this.schoolTitul;

      var filter = {};
      if (
        this.schoolTitulForm.klass ||
        this.schoolTitulForm.language ||
        this.schoolTitulForm.liter ||
        this.schoolTitulForm.year ||
        this.schoolTitulForm.study_direction
      ) {
        if (this.schoolTitulForm.klass) {
          filter.klass = this.schoolTitulForm.klass;
        }
        if (this.schoolTitulForm.language) {
          filter.language = this.schoolTitulForm.language;
        }
        if (this.schoolTitulForm.liter) {
          filter.liter = this.schoolTitulForm.liter;
        }
        if (this.schoolTitulForm.year) {
          filter.year = this.schoolTitulForm.year;
        }
        if (this.schoolTitulForm.study_direction) {
          filter.study_direction = this.schoolTitulForm.study_direction;
        }

        all = _.filter(all, filter);
        return all;
      } else {
        return all;
      }
    },

    isComplete() {
      if (this.schoolTitulForm.klass &&
          this.schoolTitulForm.liter &&
          this.schoolTitulForm.students &&
          this.schoolTitulForm.year &&
          this.schoolTitulForm.language &&
          this.schoolTitulForm.study_direction
          // && this.schoolTitulForm.user
      ) {
        return true;
      }

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
        this.liters = response.data.liters,
        // this.schoolTitulForm.year = response.data.datas[0],
        (this.warning1 =response.data.warning),
        (this.users = response.data.users.map(user => {
          return Object.assign({}, user.user, {
            avatar: "https://eportfolio.kz/static/images" + user.avatar.substr(6)
          });
        })),
        window.setTimeout(show_popup, 3000)
      )).catch(function (error) {
        console.log(error);
      });
  }

});