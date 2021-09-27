axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
    el: "#RequestEditio",
    delimiters: ["{(", ")}"],
    data: {
        rstatus: 0,
        quantity: 0,
        modal: false,
        createI: false,
        loading: true,
        loading2: false,
        add_modal: false,
        request_edition: false,
        id: null,
        modelr: null,
        year: "",
        time: "",
        token: "",
        klass: "",
        count3: 0,
        count2: "",
        edition: "",
        subject: "",
        language: "",
        formStyle: "form-control",
        briefcase: "",
        menu_edition: "",
        scheckids: {},
        datas: [],
        years: [],
        liters: [],
        klasses: [],
        invoices: [],
        editions: [],
        editionss: [],
        subjects: [],
        providers: [],
        edition_s: [],
        languages: [],
        class_list: [],
        my_checkid: [],
        editions_val: [],
        my_request_edition: []
    },

    components: {
        multiselect: VueMultiselect.Multiselect
    },
    computed:{
        filterEditions() {
            var all = this.my_request_edition;
            filter = {
                edition: {}
            };
            // this.count1 = all.length
            if (this.klass || this.language || this.subject || this.edition) {
                if (this.klass) {
                  filter.edition.klass = this.klass.name;
                }
                if (this.language) {
                  filter.edition.language = this.language.name;
                }
                if (this.subject) {
                    filter.edition.subject = this.subject.name
                }
                if (this.edition) {
                  filter.edition.name = this.edition.name;
                }

                all = _.filter(all, filter);
                return all;
              } else {

                return all;
              }

        },

        filterEditions() {
            var all = this.my_request_edition;
            filter = {
                edition: {}
            };
            // this.count1 = all.length
            if (this.klass || this.language || this.subject || this.edition) {
                if (this.klass) {
                  filter.edition.klass = this.klass.name;
                }
                if (this.language) {
                  filter.edition.language = this.language.name;
                }
                if (this.subject) {
                    filter.edition.subject = this.subject.name
                }
                if (this.edition) {
                  filter.edition.name = this.edition.name;
                }

                all = _.filter(all, filter);
                return all;
              } else {

                return all;
              }

        },

        filterEditions2() {
            var all = this.editionss;
            filter = {};
            if (this.klass || this.language || this.subject || this.edition) {
                if (this.klass) {
                  filter.klass = this.klass.name;
                }
                if (this.language) {
                  filter.language = this.language.name;
                }
                if (this.subject) {
                    filter.subject = this.subject.name
                }
                if (this.edition) {
                  filter.name = this.edition.name;
                }

                console.log(filter, "");
                all = _.filter(all, filter);
                return all;
              } else {
                return all;
              }

        },

        filterEditions3() {
            var all = this.my_checkid;
            filter = {
                edition: {}
            };
            // this.count1 = all.length
            if (this.klass || this.language || this.subject || this.edition) {
                if (this.klass) {
                  filter.edition.klass = this.klass.name;
                }
                if (this.language) {
                  filter.edition.language = this.language.name;
                }
                if (this.subject) {
                    filter.edition.subject = this.subject.name
                }
                if (this.edition) {
                  filter.edition.name = this.edition.name;
                }

                all = _.filter(all, filter);
                return all;
              } else {

                return all;
              }

        },
    },

    mounted() {
        const self = this;
        axios
            .get(document.location.href, {
                params: {
                    all_edition: true
                }
            })
            .then(response => {
                (this.my_request_edition=response.data.my_request_edition),
                (this.editionss=response.data.editions),
                (this.klasses=response.data.klasses),
                (this.languages=response.data.languages),
                (this.subjects=response.data.subjects),
                (this.years=response.data.years),
                (this.loading=false),
                (this.count2=response.data.count2),
                (this.count3=response.data.count3)
            })
            .catch(function(error) {
                console.log(error);
            });
    },
    methods: {
        count1(){
            return this.filterEditions.length
        },

        // CountfilterEditions(){
        //     let s = this.filterEditions().length;
        //     return s
        // },
        //
        // CountfilterEditions2(){
        //     les s = this.filterEditions2().length;
        //     return s
        // },

        reLoad(){location.reload();},

        thisCheck(id){
            data = {
                this_request: id,

            }
            axios
              .post(document.location.href, data).then(response => {
                this.my_request_edition = response.data,
                this.scheckids=[],
                this.modal=false
              })
              .catch(error => {
                  console.log(error, "rrrr");
            });

        },

        getMyCheckid(){
            this.loading=true
            axios
            .get(document.location.href, {
                params: {
                    get_my_checkid: true
                }
            })
            .then(response => {
                (this.my_checkid=response.data.map(item=>{
                    item.edition = item.request_edition.edition
                    return item
                })),
                (this.loading=false);
            })
            .catch(function(error) {
                console.log(error);
            });
        },

        DeleteCheck(id){
            axios
            .delete(document.location.href, {
                params: {
                    my_check_del: id
                }
            })
            .then(response => {
                (this.my_checkid=this.my_checkid.filter(item => item.id != id))
                this.count3--
            })
            .catch(function(error) {
                console.log(error);
            });
        },

        getEditionR(){
            this.loading=true
            axios
            .get(document.location.href, {
                params: {
                    get_edition_r: true
                }
            })
            .then(response => {
                (this.my_request_edition=response.data),
                (this.loading=false);
            })
            .catch(function(error) {
                console.log(error);
            });
        },


        getEdition(datamodel){
          if (datamodel.scheckids.length > 0){
              this.scheckids = datamodel;
              this.modal = true
          }
        },

        addCheck(id, quantity, s, status) {
            if (quantity > 0 && quantity <= s || !status){
                data = {
                add_request:{
                    request_edition: id,
                    check: status,
                    quantity: Number(quantity)
                }
                };
                axios
                  .post(document.location.href, data).then(response => {
                    this.my_request_edition = this.my_request_edition.filter(item => item.id != id)
                    this.count2--
                    this.count3++

                  })
                  .catch(error => {
                      console.log(error, "rrrr");
                });
            }


        },


        addEdition(datamodel){
          if (this.request_edition == 1){
              this.modelr = datamodel;
              this.add_modal = true;
              console.log(this.add_modal)
              // this.modelr.quantity = 0
              // this.request_edition = 3
          }
          if (this.request_edition == 4 && this.modelr.quantity > 0){
              data = {
                  add_request_edition:{
                      edition: this.modelr.id,
                      quantity: Number(this.modelr.quantity),
                  }
              };

              axios
                  .post(document.location.href, data).then(response => {
                    (this.my_request_edition.push(response.data)),
                    (this.request_edition=0),
                    (this.add_modal=false)
                  })
                  .catch(error => {
                        this.request_edition = 4,
                        (this.satus = "error"),
                        console.log(error, "rrrr");
                  });
          }



        },

        nameKlass({ id, name }) {
            var names = name;
            if (id <= 12) {
                names = names.slice(0, 7);
            }
            return `${names}`;
        }

    }
});

Vue.component("Button", {
    props: ["item", "getinvoice"],
    template: "#button_g",
    delimiters: ["{(", ")}"],
    data: function() {
        return {
            loading: false,
        };
    }

});

Vue.component("EditionsList", {
    props: ["datamodel", "index", "datas", "addedition", "deletecheck"],
    template: "#editions-list",
    delimiters: ["{(", ")}"],
    data: function() {
        return {
            satus: null,
            sends: 0
        };
    },

});

Vue.component("EditionsList2", {
    props: ["datamodel", "index", "datas", "addedition", "request_edition", "get_edition", "addcheck", "deletecheck"],
    template: "#editions-list2",
    delimiters: ["{(", ")}"],
    data: function() {
        return {
            quantity2: 0,
            satus: null,
            sends: 0
        };
    },
    methods:{
        getSum(){
            let s = 0
            this.datamodel.scheckids.forEach(item => s = s + item.quantity)
            let val = this.datamodel.quantity - s
            return val
        }
    }

});