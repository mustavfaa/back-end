axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
  el: "#Appset",
  delimiters: ["{(", ")}"],
  data: {
    ru: true,
    kk: false,
    not: false,
    books: false,
    modal: false,
    danger: false,
    loading: false,
    worning: false,
    sucsess: false,
    create_b: false,
    formView: false,
    addBooks: false,
    get_portfel: false,
    show_briefcases: false,
    briefcase_status: false,
    view_edition_list: false,
    info_post_briefcase: false,
    year: "",
    time: "",
    token: "",
    klass: "",
    edition: "",
    language: "",
    briefcase: "",
    menu_edition: "",
    datas: [],
    years: [],
    liters: [],
    klasses: [],
    editions: [],
    edition_s: [],
    languages: [],
    b_editions: [],
    class_list: [],
    briefcases: [],
    schoolTitul: [],
    editionsTeacher: [],
    studyDirections: [],
    schoolTitulForm: {},
    gcase: {
      name: "",
      description: "",
      editions: []
    },
    form_briefcase: {
      name: "",
      description: "",
      klass: "",
      language: ""
    }
  },


  components: {
    multiselect: VueMultiselect.Multiselect
  },

  mounted() {
    const el = document.getElementById("token");
    var token = el.dataset.token;
    this.token = token;
    const self = this;

    if (urlLanguage === "/kk/") {
      this.kk = true;
      this.ru = false;
    }

    axios
      .get(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
        headers: {
          token: self.token
        },
        params: {
          briefcase: true
        }
      })
      .then(
        response => (
          (self.worning = response.data.worning),
          (self.briefcases = response.data.briefcases),
          (self.schoolTitul = response.data.klasses),
          (this.languages = response.data.languages),
          (this.studyDirections = response.data.studyDirections),
          (this.class_list = response.data.class_list),
          (this.datas = response.data.datas),
          (this.liters = response.data.liters),
          (self.not = true)
          // (this.schoolTitulForm.year = response.data.datas),
        )
      )
      .catch(function (error) {
        console.log(error);
      });
  },

  computed: {
    // фильтр книг
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
    },

    filterEditions2() {
      var array = [];
      this.b_editions.map(function (item) {
        array.push(item.edition.id);
        return item;
      });
      var p = [];
      p = Array(...this.editions);

      var all = p.filter(item => {
        if (array.includes(item.id)) {
          item.style = true;
          return item;
        } else {
          return item;
        }
      });

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
    },

    filterEditions3() {
      var array = [];
      this.editionsTeacher.map(function (item) {
        array.push(item.edition.id);
        return item;
      });
      var p = [];
      p = Array(...this.editions);

      var all = p.filter(item => {
        if (array.includes(item.id)) {
          item.style = true;
          return item;
        } else {
          return item;
        }
      });

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
    },

    arrayBcaseEditions() {
      var all = [];
      this.beditions.map(item => {
        all.push(item.id);
        return item;
      });
      return all;
    },

    sortedBcaseEditions() {
      return this.b_editions.sort(function (a, b) {
        var x = a.edition.name.toLowerCase();
        var y = b.edition.name.toLowerCase();
        return x < y ? -1 : x > y ? 1 : 0;
      });
    },
    sortedBriefcases() {

      return this.briefcases.sort(function (a, b) {
        var x = a.klass;
        var y = b.klass;
        return x < y ? -1 : x > y ? 1 : 0;
      });
    },

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
          filter.klass = this.schoolTitulForm.klass.id;
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

    filterSubject() {
      var array = [];
      this.b_editions.map(item => {
        array.push(item.edition.subject);
        return item;
      });
      uniq = [...new Set(array)];
      return uniq;
    },

    nameB() {
      if (this.form_briefcase.klass){
        var klass = this.form_briefcase.klass
        if (klass.id <= 12) {

          klass.name = klass.name.slice(0, 7)
        }


        if (this.form_briefcase.klass) {
          this.form_briefcase.name = klass.name + " ";
        }
        if (this.form_briefcase.klass && this.form_briefcase.language) {
          this.form_briefcase.name =
            klass.name +
            " " +
            this.form_briefcase.language.name +
            " ";
        }
        if (
          this.form_briefcase.klass &&
          this.form_briefcase.language &&
          this.form_briefcase.description
        ) {
          this.form_briefcase.description = this.form_briefcase.description.toLowerCase();
          this.form_briefcase.name =
            klass.name +
            " " +
            this.form_briefcase.language.name +
            " " +
            this.form_briefcase.description;
        }
        return this.form_briefcase.name;
      }
    }
  },

  methods: {
    formBriefcase(){
      this.form_briefcase = {
        name: "",
        description: "",
        klass: "",
        language: ""
      }
    },
    nameKlass({
      id,
      name
    }) {
      var names = name
      if (id <= 12) {
        names = names.slice(0, 7)
      }
      return `${names}`
    },

    getCreate() {
      const self = this;
      axios
        .get(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            get_create: true
          }
        })
        .then(
          response => (
            (self.editions = response.data.editions.map(function (item) {
              item.checked = false;
              item.style = false;
              item.surplus = 100;
              return item;
            })),
            (self.klasses = response.data.klasses),
            (self.languages = response.data.languages)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    postBriefcase() {
      const el = document.getElementById("token");
      var token = el.dataset.token;
      this.loading = true;
      this.briefcase = "";
      var self = this;

      data = {
        token: self.token,
        briefcase: this.form_briefcase
      };

      const a = this.briefcases;

      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time =
        datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      axios
        .post(urlLanguage + "cabinet/head_librarian/briefcase/api/", data)
        .then(function (response) {
          if (response.data.error) {
            self.info_post_briefcase = true;
            self.loading = false;
          } else {
            self.menu_edition = response.data.name;
            self.briefcases.push(response.data);
            self.briefcase = response.data;
            self.formView = false;
            self.books = true;
            self.form_briefcase = {};
            form = "";
            self.loading = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    // Добавление книг
    addEdition(id, value) {
      var all = this.edition_s;
      if (this.edition_s.length > 0) {
        if (
          all.every(function (obj) {
            return obj.edition != id;
          })
        ) {
          this.edition_s.push({
            edition: id,
            surplus: value
          });
        } else
          this.edition_s.pop({
            edition: id,
            surplus: value
          });
      } else {
        this.edition_s.push({
          edition: id,
          surplus: value
        });
      }
    },

    sendEdition() {
      var Data = [];
      const self = this;
      this.editions.map(function (item) {
        if (item.checked) {
          var a = {};
          a.edition = item.id;
          a.surplus = item.surplus;
          a.briefcase = self.briefcase.id;
          Data.push(a);
          item.surplus = 100;
          item.checked = false;
          return item;
        } else return item;
      });
      this.loading = true;
      data = {
        token: self.token,
        editions: Data
      };
      axios
        .post(urlLanguage + "cabinet/head_librarian/briefcase/api/", data)
        .then(function (response) {
          self.b_editions = response.data;
          self.books = false;
          self.create_b = false;
          self.addBooks = false;
          self.loading = false;
          self.edition_s = [];
          self.language = "";
          self.klass = "";
          self.edition = "";
          self.getBriefcase((item = self.briefcase));
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    sendEdition2() {
      var Data = [];
      const self = this;
      this.editions.map(function (item) {
        if (item.checked) {
          var a = {};
          a.edition = item.id;
          a.quantity = Number(item.quantity);
          a.year = self.year.id;
          Data.push(a);
          item.checked = false;
          return item;
        } else return item;
      });
      this.loading = true;
      data = {
        token: self.token,
        teacher_editions: Data
      };

      axios
        .post(urlLanguage + "cabinet/head_librarian/briefcase/api/", data)
        .then(function (response) {
          self.editionsTeacher = response.data;
          self.books = false;
          self.create_b = false;
          self.addBooks = false;
          self.loading = false;
          self.language = "";
          self.klass = "";
          self.edition = "";
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    getBriefcase(item) {

      this.get_portfel = true;
      const self = this;
      axios
        .get(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            get_briefcase: item.id
          }
        })
        .then(
          response => (
            (self.briefcase = response.data.briefcases),
            (self.menu_edition = response.data.briefcases.name),
            (self.b_editions = response.data.beditions),
            (self.editions = response.data.editions.map(function (item) {
              item.checked = false;
              item.style = false;
              item.surplus = 100;
              return item;
            })),
            (self.klasses = response.data.klasses),
            (self.languages = response.data.languages)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    delEdBriefcase(id) {
      const self = this;

      axios
        .delete(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            edition: id.id
          }
        })
        .then(
          response => (
            self.b_editions.splice(self.b_editions.indexOf(id), 1)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    delTEdition(item) {
      const self = this;
      axios
        .delete(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            teacher_edition: item.id
          }
        })
        .then(response =>
          self.editionsTeacher.splice(self.editionsTeacher.indexOf(item), 1)
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    computeMyBind() {
      var sum = 0;
      this.filterNames.map(item => {
        sum = sum + item.planned_quantity;
        return item;
      });
      return sum;
    },

    delBriefcaseC(id) {
      const self = this;
      this.loading = true;
      axios
        .delete(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            param: id
          }
        })
        .then(
          response => (
            self.schoolTitul.map(function (obj) {
              if (obj.id == id) {
                obj.briefcase = null;
                return obj;
              } else {
                return obj;
              }
            }),
            (self.loading = false)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    addBriefcaseC(klass, model) {
      var self = this;

      data = {
        token: this.token,
        add_briefcase: {
          plan_titul: klass,
          briefcase: model
        }
      };
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time =
        datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];

      axios
        .post(urlLanguage + "cabinet/head_librarian/briefcase/api/", data)
        .then(function (response) {
          self.schoolTitul.filter(function (item) {
            if (item.id == klass) {
              item.briefcase = response.data;
              return item;
            } else {
              return item;
            }
          });
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    deleteBriefcase(item) {
      const self = this;
      this.loading = true;
      axios
        .delete(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            briefcase: item.id
          }
        })
        .then(
          response => (
            self.briefcases.splice(self.briefcases.indexOf(item), 1),
            (self.schoolTitul = response.data.data),
            (self.loading = false)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    },

    cLear() {
      this.schoolTitulForm = {};
    },

    cHeckid() {
      var es = false;
      this.editions.map(function (item) {
        if (item.checked == true) {
          es = true;
        }
        return item;
      });
      return es;
    },

    getETiacher() {
      this.get_portfel = true;
      this.view_edition_list = true;
      const self = this;
      axios
        .get(urlLanguage + "cabinet/head_librarian/briefcase/api/", {
          headers: {
            token: self.token
          },
          params: {
            editions_teacher: true
          }
        })
        .then(
          response => (
            (self.editions = response.data.editions.map(function (item) {
              item.checked = false;
              item.style = false;
              item.quantity = 0;
              return item;
            })),
            (self.editionsTeacher = response.data.teacherEditions),
            (self.klasses = response.data.klasses),
            (self.languages = response.data.languages),
            (self.years = response.data.years)
          )
        )
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});

Vue.component("EditionsList", {
  props: ["datamodel", "index", "datas", "addfn"],
  template: "#editions-list",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      checked: false,
      value: 100
    };
  }
});

Vue.component("BriefcaseList", {
  props: ["item", "index", "bgetfn", "deletefn", "worning"],
  template: "#briefcase-list",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      checked: false
    };
  }
});

//Компонент таблицы
Vue.component("klass-item", {
  delimiters: ["{(", ")}"],
  props: ["item", "index", "delelefn", "addfn", "briefcases", "worning"],
  template: "#klasses-template",
  data: function () {
    return {
      model: ""
    };
  },

  components: {
    multiselect: VueMultiselect.Multiselect
  }
});