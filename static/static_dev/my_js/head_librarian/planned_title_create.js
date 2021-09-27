axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
  el: "#create_plan_title",
  delimiters: ["{(", ")}"],
  components: {
    multiselect: VueMultiselect.Multiselect
  },

  data: function () {
    return {
      pk: null,
      number: null,
      school: null,
      dataTable: null,
      model_titul: null,
      not: false,
      one: true,
      edit: false,
      list: false,
      print: false,
      modal: false,
      danger: false,
      warning: false,
      oneclik: true,
      notshow: false,
      sucsess: false,
      for_plan: false,
      get_modal: false,
      plantitul: false,
      showResults: false,
      name_year: {},
      schoolTitulForm: {},
      study_direction: "",
      time: "",
      year: "",
      token: "",
      block: "none",
      plan_year: "",
      datas: [],
      years: [],
      liters: [],
      klasses: [],
      get_plan: [],
      languages: [],
      plan_tituls: [],
      school_tituls: [],
      school_tituls_p: [],
      directions_s: [],
      year_school_titul: []
    };
  },

  computed: {
    sortPlanTituls() {
      return this.get_plan.sort(function (a, b) {
        var x = a.klass;
        var y = b.klass;
        return x < y ? -1 : x > y ? 1 : 0;
      });
    }

  },

  mounted() {
    const el = document.getElementById("token");
    const self = this;
    var token = el.dataset.token;
    self.token = token;

    axios
      .get(urlLanguage + "cabinet/head_librarian/planned_title_create/api/", {
        headers: {
          token: self.token
        }
      })
      .then(
        response => (
          (self.year_school_titul = response.data.plan_years),
          (self.school_tituls = response.data.school_tituls.map(function (sh) {
            sh.school_titul = sh.id;
            sh.send = false;
            delete sh.id;
            delete sh.deleted;
            delete sh.date_added;
            delete sh.exchange;
            delete sh.comment;
            sh.planned_quantity = 0;
            // sh.klass++;
            return sh;
          })),
          (self.languages = response.data.languages),
          (self.klasses = response.data.klasses.map(function (item) {
            if (item.name.length > 7) {
              item.name = item.name.slice(0, 7);
            }
            return item;
          })),
          (self.directions_s = response.data.studyDirections),
          (self.liters = response.data.liters),
          (self.years = response.data.years),
          (self.datas = response.data.datas),
          (self.warning = response.data.warning),
          (self.not = true)
        )
      )
      .catch(function (error) {
        console.log(error);
      });
  },

  methods: {
    // методы при создании планового титула
    ValidIn({
      name,
      id
    }) {
      var m = " Учебный год уже существует";
      var mes = "";
      this.datas.map(function (item) {
        if (item.id == id) {
          return (mes = m);
        }
        return item;
      });
      if (mes) {
        name = name + mes;
      }
      return `${name}`;
    },

    // Удаление планового титула
    deletePlan(pk) {
      const self = this;
      var id = pk.id;

      axios
        .delete(
          urlLanguage + "cabinet/head_librarian/planned_title_create/api/", {
            headers: {
              token: this.token
            },
            params: {
              plan_year: id
            }
          }
        )
        .then(function (response) {
          self.datas.splice(self.datas.indexOf(pk), 1);
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    // Создание планового титула
    cReate(number, year) {
      const self = this;
      this.school = this.school_tituls[0].school;
      var count = this.school_tituls.length - 1;
      var tituls = _.sortBy(this.school_tituls, 'klass');
      var last = tituls[count].klass;
      var first = tituls[0].klass;
      // получение первого элемента в массиве и добавление
      const newData = [];
      if (this.plan_year !== "") {

        tituls.map(function (el) {
          if (el.year.id === self.plan_year.id && el.klass == first) {
            const titul = {
              ...el
            }
            titul.students = 0
            newData.push({
              ...titul
            });
            const titul2 = {
              ...el
            }
            titul2.klass = titul2.klass + 1;
            newData.push({
              ...titul2
            });

          }
          if (el.year.id === self.plan_year.id && el.klass != first && el.klass < last) {
            const titul = {
              ...el
            }
            titul.klass = titul.klass + 1;
            newData.push({
              ...titul
            });
          }
          return el
        })

        this.school_tituls_p = newData.map(function (sh) {
          (sh.planned_quantity = parseInt(
            (sh.students * number) / 100 + sh.students
          )),
          (sh.year = self.year.id),
          (self.showResults = true);
          self.plantitul = false;
          const show = true;
          return sh;
        });

        this.notshow = false;
        this.list = false;
        if (this.one) {
          this.one = false;
        }
      }
      if (this.oneclik) {
        this.oneclik = false;
      }
      this.get_modal = true;
    },

    delTitul(item) {
      const self = this;
      self.school_tituls_p.splice(self.school_tituls_p.indexOf(item), 1);
    },

    addPlanTitul(number) {
      this.schoolTitulForm.klass = this.schoolTitulForm.klass.id;
      this.schoolTitulForm.students = Number(this.schoolTitulForm.students);
      const self = this;
      this.schoolTitulForm.year = this.school_tituls_p[0].year;
      this.schoolTitulForm.planned_quantity = parseInt(
        (this.schoolTitulForm.students * number) / 100 +
        this.schoolTitulForm.students
      );
      this.schoolTitulForm.school = this.school_tituls[0].school;
      this.schoolTitulForm.study_direction = this.schoolTitulForm.study_direction.id;
      const titul = this.schoolTitulForm;
      self.school_tituls_p.push(titul);
      this.schoolTitulForm = {};
      this.block = "none";
    },

    editPlanTitul(titul) {
      const self = this;
      this.edit = true;
      this.modal = true;
      this.block = "block";
      var schoolTitulForm = {};
      this.klasses.map(function (item) {
        if (Number(titul.klass) == item.id) {
          schoolTitulForm.klass = item;
        }
        return item;
      });
      this.directions_s.map(function (item) {
        if (Number(titul.study_direction) == item.id) {
          schoolTitulForm.study_direction = item;
        }
        return item;
      });
      // schoolTitulForm.klass = titul.klass;
      schoolTitulForm.liter = titul.liter;
      schoolTitulForm.language = titul.language;
      schoolTitulForm.students = Number(titul.students);
      schoolTitulForm.planned_quantity = parseInt(
        (schoolTitulForm.students * self.number) / 100 +
        schoolTitulForm.students
      );
      this.schoolTitulForm = schoolTitulForm;
    },
    sendEdit() {
      const self = this;
      this.school_tituls_p.map(function (el) {
        if (el.send == true) {
          el.klass = self.schoolTitulForm.klass.id;
          el.liter = self.schoolTitulForm.liter;
          el.language = self.schoolTitulForm.language;
          el.study_direction = self.schoolTitulForm.study_direction.id;
          el.students = Number(self.schoolTitulForm.students);
          el.planned_quantity = self.schoolTitulForm.planned_quantity;
          el.send = false;
          return el;
        } else return el;
      });
      this.schoolTitulForm = {};
      this.edit = false;
      this.modal = false;
      this.block = "none";
    },

    sEnd() {
      var data = {
        token: this.token,
        school_tituls: this.school_tituls_p.map(function (sh) {
          if (sh.liter != null && sh.language != null) {
            sh.liter = sh.liter.id;
            sh.language = sh.language.id;
            return sh;
          } else if (sh.liter == null) {
            sh.language = sh.language.id;
            return sh;
          }
        })
      };
      axios
        .post(
          urlLanguage + "cabinet/head_librarian/planned_title_create/api/",
          data
        )
        .then(function (response) {
          location.reload();
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    cLear() {
      this.number = null;
      this.showResults = false;
    },

    // Созданные плановые титулы
    getPlan(pk) {
      const self = this;
      this.get_modal = true;
      this.name_year = pk;
      this.for_plan = true
      this.pk = pk.id;
      var all = [];
      axios
        .get(
          urlLanguage + "cabinet/head_librarian/planned_title_list/api/list/", {
            headers: {
              token: this.token
            },
            params: {
              pk: pk.id
            }
          }
        )
        .then(function (response) {
          self.get_plan = response.data.school_tituls;
          self.list = true;
        })
        .catch(function (error) {
          console.log(error);
        });
      this.notshow = true;
      if (this.one == true) {
        this.one = false;
      }
    },

    addForPlanTitul(number) {
      const self = this;
      this.schoolTitulForm.students = Number(this.schoolTitulForm.students);
      this.schoolTitulForm.year = this.get_plan[0].year;
      this.schoolTitulForm.planned_quantity = parseInt(
        (this.schoolTitulForm.students * number) / 100 +
        this.schoolTitulForm.students
      );
      this.schoolTitulForm.school = this.get_plan[0].school;
      this.schoolTitulForm.study_direction = this.schoolTitulForm.study_direction.id;
      var post_titul = {
        ...this.schoolTitulForm
      }

      post_titul.klass = post_titul.klass.id
      post_titul.language = post_titul.language.id
      post_titul.liter = post_titul.liter.id
      post_titul.year = post_titul.year.id
      post_titul.school = post_titul.school
      post_titul.study_direction = post_titul.study_direction.id
      var add_plan_titil = {
        ...this.schoolTitulForm
      }
      add_plan_titil.klass = add_plan_titil.klass.id

      data = {
        token: this.token,
        plan_titul: post_titul
      };
      axios
        .post(urlLanguage + "cabinet/head_librarian/planned_title_list/api/list/", data)
        .then(function (response) {
          self.schoolTitulForm.id = response.data.id;
          self.schoolTitulForm.klass = response.data.klass.id;
          self.get_plan.push(add_plan_titil);
          self.schoolTitulForm = {};
          self.block = "none";
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    deleteGetplan(item) {
      const self = this;
      axios
        .delete(urlLanguage + "cabinet/head_librarian/planned_title_list/api/list/", {
          headers: {
            token: self.token
          },
          params: {
            titul: item.id
          }
        })
        .then(
          response => (
            self.get_plan.splice(self.get_plan.indexOf(item), 1)
          )
        )
        .catch(function (error) {
          console.log(error);
        });


    },

    uPdateList() {
      const self = this;
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time =
        datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      var list = [];
      this.get_plan.map(item => {
        list.push({
          id: item.id,
          planned_quantity: item.planned_quantity
        });
        return item;
      });
      data = {
        token: this.token,
        school_tituls: list
      };
      axios
        .post(
          urlLanguage + "cabinet/head_librarian/planned_title_list/api/list/",
          data
        )
        .then(function (response) {
          self.sucsess = true;
          self.danger = false;
        })
        .catch(function (error) {
          self.sucsess = false;
          self.danger = true;
          console.log(error);
        });
    },

    computeMyBind() {
      var sum = 0
      this.school_tituls_p.map(item => {
        sum = sum + item.planned_quantity
        return item
      })
      return sum
    },

    computeMyBind2() {
      var sum = 0
      this.get_plan.map(item => {
        sum = sum + item.planned_quantity
        return item
      })
      return sum
    },

    exspotB() {
      const self = this

      function print() {
        $("#table2excel").table2excel({
          exclude: ".noExl",
          name: "Worksheet Name",
          fileext: ".xls",
          filename: "Плановый титул " + self.name_year.name + ".xls" //do not include extension
        })
      }

      var a = setTimeout(print, 1500)
      var b = setTimeout(() => self.print = false, 2000)

    }
  }
});

Vue.component("school-tituls", {
  props: ["index", "datamodel", "deltitul", "editplantitul", "deletegplan", "print"],
  delimiters: ["{(", ")}"],
  data: function () {
    return {};
  },
  template: "#school-tituls"
});

Vue.component("years-list", {
  props: ["index", "year", "getplan", "name_year", "deletefn", "warningp"],
  delimiters: ["{(", ")}"],
  data: function () {
    return {};
  },
  template: "#years_list"
});
