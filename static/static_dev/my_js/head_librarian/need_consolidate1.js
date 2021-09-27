axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
  el: "#Reestr",
  delimiters: ["{(", ")}"],
  data: {
    ru: true,
    kk: false,
    not: false,
    modal: false,
    token: false,
    loading: false,
    show_table: false,
    show_access: false,
    group: 8,
    all_students: 0,
    year: "",
    language: "",
    years: [],
    datas: [],
    klasses: [],
    en_datas: [],
    b_klasses: [],
    klasses_t: [],
    teacher_classes: []
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
      .get(urlLanguage + "cabinet/head_librarian/consolidated_registry/api/", {
        headers: {
          token: self.token
        },
        params: {
          get_years: true
        }
      })
      .then(
        response => (
          (self.years = response.data.years),
          (self.not = true)
        )
      )
      .catch(function(error) {
        console.log(error);
      });
  },

  computed: {
    filterTeacher() {
      const self = this;
      var datas = [];
      this.teacher_classes.forEach(function(item) {
        self.datas[0].editions.filter(function(el) {
          if (item.edition.id == el.edition.id) {
            item.order = item.quantity;
          } else {
            item.order = item.quantity;
          }
          return el;
        });
        datas.push(item);
        return item;
      });
      return datas;
    },

    filtetBrif() {
      var all = [];
      for (klass in this.b_klasses) {
        var obj = {
          klass: this.b_klasses[klass],
          language: {},
          editions: [],
          klasses: [],
          students: 0
        };
        this.en_datas.map(item => {
          if (obj.klass == item.klass) {
            obj.students = obj.students + item.students;
            obj.language = item.language;
            obj.klasses = obj.klasses.concat(item.klasses);
            obj.editions = obj.editions.concat(item.editions);
          }
          return item;
        });
        all.push(obj);
      }
      function compare(a, b) {
        if (a.edition.id < b.edition.id) {
          return -1;
        }
        if (a.edition.id > b.edition.id) {
          return 1;
        }
        return 0;
      }
      var sall = all.map(item => {
        item.editions.sort(compare);
        return item;
      });

      const addEditions = (knownEditions, edition) => {
        const {
          need,
          edition: { id }
        } = edition;

        const knownEdition = knownEditions.find(n => n.edition.id === id);

        if (!knownEdition) return [...knownEditions, { ...edition }];
        knownEdition.need += need;
        return knownEditions;
      };

      const prepareBooksData = sall =>
        sall.map(sall => ({
          ...sall,
          editions: sall.editions.reduce(addEditions, [])
        }));
      var datas = this.datas;
      var b_all = prepareBooksData(sall);
      var b2_all = b_all.map(item => {
        item.editions.map(e => {
          e.order = e.need - e.availability;
          return e;
        });
        return item;
      });
      var a_all = datas.concat(b2_all);

      function sortClass(a, b) {
        if (a.klass < b.klass) {
          return -1;
        }
        if (a.klass > b.klass) {
          return 1;
        }
        return 0;
      }
      return a_all.sort(sortClass);
    }
  },

  methods: {
    endAccess(){
      const self =this
      data = {
        token: this.token,
        access: true
      };
      axios.post(urlLanguage + "cabinet/head_librarian/consolidated_registry/api/", data).then((response) => {
        if (response.data.access_success === true) {
          this.modal = true
        }
      }).catch(function (error) {
          console.log(error);
        });
    },

    getGroup(klass) {
      return this.filterTeacher
        .filter(
          item =>
            item.klass === klass.edition__klass &&
            item.language === klass.edition__language
        )
        .map(item => item);
    },
    getReestr() {
      const self = this;
      this.loading = true
      var uniq = {};
      axios
        .get(
          urlLanguage + "cabinet/head_librarian/consolidated_registry/api/",
          {
            headers: {
              token: self.token
            },
            params: {
              get_reestr_year: this.year.id
            }
          }
        )
        .then(
          response => (
            (self.all_students = response.data.all_students),
            (self.b_klasses = response.data.b_klasses),
            (self.en_datas = response.data.tables.map(item => {
              var a = item.editions.filter(function(t) {
                if (t.edition.language.id == 3) {
                  return item;
                }
              });
              item.editions = a;
              item.language = response.data.lang_en;
              return item;
            })),
            (self.datas = response.data.table.map(item => {
              var a = item.editions.filter(function(t) {
                if (t.edition.language.id != 3) {
                  return item;
                }
              });
              item.editions = a;
              return item;
            })),
            (self.teacher_classes = response.data.teacher_classes.map(function(
              item
            ) {
              item.klass = item.edition.klass;
              item.language = item.edition.language.id;
              return item;
            })),
            (self.klasses_t = response.data.klasses_t.sort(
              (a, b) => a.edition__klass - b.edition__klass
            )),
            (self.loading = false),
            (self.show_access = true),
            (self.show_table = true)
          )
        )
        .catch(function(error) {
          console.log(error);
        });
    }
  }
});
