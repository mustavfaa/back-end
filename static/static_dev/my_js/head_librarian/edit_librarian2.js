axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

Vue.component("FormBoocks", {
  props: ["ttt", "datamodel", "index", "mouseleave"],
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      summ: false,
      in_warehouse: false
    };
  },
  methods: {
    getClassesHands: function () {
      if (
        this.datamodel.summ === "" ||
        (this.datamodel.summ <= 0 && this.datamodel.in_warehouse <= 0)
      ) {
        return {
          "alert-inform": true
        };
      }
    },

    getClassesWarehouse: function () {
      if (
        this.datamodel.in_warehouse === "" ||
        (this.datamodel.summ <= 0 && this.datamodel.in_warehouse <= 0)
      ) {
        return {
          "alert-inform": true
        };
      }
    }
  },
  template: "#form-boocks"
});

new Vue({
  el: "#appBoock",
  delimiters: ["{(", ")}"],
  data: function () {
    return {
      computeMyBind: 0,
      computeMyBind1: 0,
      ru: true,
      kk: false,
      ttt: false,
      not: false,
      push: false,
      send: false,
      danger: false,
      loading: false,
      sucsess: false,
      notGood: false,
      modalBox: false,
      time: "",
      item: "",
      name: "",
      token: "",
      klass: "",
      index: "",
      author: "",
      subject: "",
      language: "",
      publisher: "",
      publish_date: "",
      series_by_year: "",
      study_direction: "",
      metodology_complex: "",
      display: "None",
      years: [],
      boocks: [],
      klasss: [],
      errors: [],
      authors: [],
      del_data: [],
      subjects: [],
      editions: [],
      languages: [],
      publishers: [],
      study_directions: [],
      metodology_complexs: []
    };
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
    console
    axios
      .get(urlLanguage + "cabinet/head_librarian/list/", {
        headers: {
          token: self.token
        }
      })
      .then(
        response => (
          (self.boocks = response.data.books.map(function (item) {
            try{
              if (item.edition.klass && item.edition.klass.length > 7){
               item.edition.klass = item.edition.klass.slice(0, 7)
            }}
            catch(e) {
                console.log(item, 'item')
            }
            return item
          })),
          (self.languages = response.data.languages),
          (self.klasss = response.data.klasss.map(function (item) {
            item.name = item.name.slice(0, 7)
            return item
          })),
          (self.subjects = response.data.subjects),
          (self.editions = response.data.editions),
          (self.years = response.data.years),
          (self.authors = response.data.authors),
          (self.publishers = response.data.publishers),
          (self.metodology_complexs = response.data.metodology_complex),
          (self.study_directions = response.data.study_direction),
          (self.not = true)
        )
      )
      .catch(function (error) {
        console.log(error, 'error');
      });
  },

  computed: {
    filterNames: function () {
      var all = this.boocks;

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
        this.computeMyBind = all.reduce(function (acc, equity) {
          return acc + parseInt(equity.summ);
        }, 0);
        this.computeMyBind1 = all.reduce(function (acc, equity) {
          return acc + parseInt(equity.in_warehouse);
        }, 0);
        return all;
      } else {

        this.computeMyBind = all.reduce(function (acc, equity) {
          return acc + parseInt(equity.summ);
        }, 0);
        this.computeMyBind1 = all.reduce(function (acc, equity) {
          return acc + parseInt(equity.in_warehouse);
        }, 0);
        return all;
      }
    }
  },

  methods: {
    nameWithLang(option) {
      return `${option.edition.name}`;
    },


    aAdd(books) {
      this.loading = true
      this.send = true
      var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
      this.time = datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
      const self = this
      if (
        this.boocks.find(obj => obj.summ === "") ||
        this.boocks.find(obj => obj.in_warehouse === "")
      ) {
        this.notGood = true;
      } else {

        //  создание нового масива
        const newData = new Array(...this.boocks)
        var add_datas = []
        var del_data = []
          var datas = []
        this.boocks.forEach(currentValue => {
          if (
            currentValue.summ !== '' && currentValue.in_warehouse !== '' && (currentValue.summ > 0 && currentValue.in_warehouse >= 0 || currentValue.summ >= 0 && currentValue.in_warehouse > 0)
          ) {
            data = {
              id: Number(currentValue.id),
              summ: Number(currentValue.summ),
              in_warehouse: Number(currentValue.in_warehouse),
              edition: Number(currentValue.edition.id)
            }
            datas.push(currentValue)
            add_datas.push(data)
            return currentValue;
          }else {
            del_data.push(Number(currentValue.id))
          }

        });

        data1 = {
          token: this.token,
          boocks: add_datas,
          del_data: del_data,
        };

        this.not = false;
        axios
          .post(urlLanguage + "cabinet/head_librarian/list/", data1)
          .then(function (response) {
            self.errors = response.data.errors,
            self.danger = false;
            self.sucsess = true;
            self.boocks =datas
            self.send = false;
            self.not = true;
            self.loading = false;
            // location.reload();
          })
          .catch(function (error) {
            self.sucsess = false;
            self.danger = true;
            self.send = false;
            self.loading =false;
            console.log(error, 'NOT SEND');
            // location.reload();
          });

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