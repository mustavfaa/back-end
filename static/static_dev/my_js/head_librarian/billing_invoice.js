axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
    el: "#Invoice",
    delimiters: ["{(", ")}"],
    data: {
        formStyle: "form-control",
        createI: false,
        ru: vdp_translation_ru.js,
        disabledDates: {
            to: new Date(2019, 1, 1),
            from: new Date(2030, 1, 26)
        },
        formCreate: {
            date_write: null,
            idx: null,
            footing: null,
            members_of_commission: null,

        },
        EditNnumber: 0,
        sendsShipper: 0,
        sendsconfidant: 0,
        sendsShipperr: 0,
        sendsProviderr: 0,
        datepickerClosed: 0,
        datepickerClosed2: 0,
        EditNumberProvider2: 0,
        sendsfreight_carrier: 0,
        EditNumberProvider23: 0,
        addE: false,
        mylist: false,
        ready_s: false,
        loading: true,
        loading2: false,
        loading3: false,
        id: null,
        number: null,
        date_write: null,
        footing: null,
        members_of_commission: null,
        statusInvoice: false,
        number_provider: null,
        freight_carrier: null,
        power_of_attorney: null,
        EditNumberProvider: false,
        date_power_of_attorney: null,
        year: "",
        time: "",
        token: "",
        klass: "",
        edition: "",
        subject: "",
        language: "",
        briefcase: "",
        menu_edition: "",
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
        portfolios: [],
        editions_val: []
    },

    components: {
        multiselect: VueMultiselect.Multiselect,
        vuejsDatepicker
    },

    computed: {


        filterEditions2() {
            let alls = new Array(...this.editionss);
            this.editions_val.forEach(el =>{
                alls.forEach(item => {
                    if (item.id === el.edition.id){
                        item.style=true
                    }
                    return item
                })
            })

            let all = alls

            if (this.klass || this.language || this.edition || this.subject) {
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
                if (this.subject) {
                    filter.subject = this.subject.name;
                }
                all = _.filter(all, filter);
                return all;
            } else {
                return all;
            }
        },


        Summs() {
            var sums = 0;
            this.invoices.map(item => {
                sums = sums + item.sum;
                return item;
            });
            return sums;
        },

        SummEditions() {
            var sum = {
                q_amount: 0,
                amount: 0
            };
            this.filterEditions2.map(item => {
                sum.amount += Number(item.amount) * Number(item.quantity);
                sum.q_amount += Number(item.quantity);

                return item;
            });
            return sum;
        }
    },
    mounted() {
        const self = this;
        axios
            .get(document.location.href, {
                params: {
                    all_invoices: true
                }
            })
            .then(response => {
                (this.invoices = response.data.invoices.map(item => {
                    item.sum = 0;
                    // item.editions_val.map(ed => {
                    //     item.sum = item.sum + ed.amount * ed.quantity;
                    //     return ed;
                    // });
                    return item;
                })),
                (this.klasses=response.data.klasses),
                (this.providers=response.data.providers),
                (this.languages=response.data.languages),
                (this.portfolios=response.data.portfolios),
                (this.subjects=response.data.subjects),
                (this.years=response.data.years),
                (this.loading=false);
            })
            .catch(function(error) {
                console.log(error);
            });
    },

    methods: {
        load33(){
            this.loading3 = true
            console.log(this.loading3)
            setTimeout(this.loading3=false, 10000);
        },

        send(datamodel) {
            if (datamodel.id > 0 && datamodel.quantity > 0){
                data = {
                id: datamodel.id,
                quantity: datamodel.quantity
                };
                axios
                    .post(document.location.href, data)
                    .then(response => {
                        this.editions_val.map(item =>{
                            if (item.id == datamodel.id){
                                item.sends = 1
                            }
                            return item
                        })
                    })
                    .catch(error => {
                        this.editions_val.map(item =>{
                            if (item.id == datamodel.id){
                                item.sends = 2
                            }
                            return item
                        })
                    });

            }

        },

        SendAmaunt(datamodel) {
            if (datamodel.id > 0 && datamodel.amount > 0){
                data = {
                id: datamodel.id,
                amount: datamodel.amount
                };
                axios
                    .post(document.location.href, data)
                    .then(response => {
                        this.editions_val.map(item =>{
                            if (item.id == datamodel.id){
                                item.sends_amount = 1
                            }
                            return item
                        })
                    })
                    .catch(error => {
                        this.editions_val.map(item =>{
                            if (item.id == datamodel.id){
                                item.sends_amount = 2
                            }
                            return item
                        })
                    });

            }

        },

        delEinvoice(datamodel){
            this.editions_val.forEach(item =>{
                if (item.id == datamodel.id){
                    item.loading = true
                }
            })
            datas ={
                delete_e: Number(datamodel.id)
            }
            axios
                .post(document.location.href, datas).then(response => {
                    this.editions_val = response.data.editions_val
                })
                .catch(function(error) {
                    console.log(error, "error");
                });
        },


        editionsVal2(data){
            this.editions_val = data
        },

        editionsVal(){
            return this.editions_val
        },

        getStatus(data){
            this.status_r = data
        },

        Deleted(id){
            data = {
             deleted: id
            };
             axios
                .post(document.location.href, data)
                .then((response) => {
                    this.invoices = this.invoices.filter(item => item.id != id)
                })
                .catch(function(error) {

            });
        },


        doRady(){
            return this.ready_s
        },


        Ready(){
            this.loading2 = true;
            data = {
             ready: this.invoice.id,
             status_r: this.invoice.status
            };
            axios
                .post(document.location.href, data)
                .then((response) => {
                    (this.invoice=response.data),
                    (this.ready_s=response.data.status),
                    (this.loading2=false)
                })
                .catch(function(error) {
            });
        },

        getPush(item){
            this.editions_val.forEach((el, index) =>{
                if (item.id == el.edition.id){
                    item.idx = el.id;
                    item.quantity = el.quantity;
                    item.amount = el.amount
                    return item
                }
            });
            return item
        },

         getPush2(item){
            this.editions_val = this.editions_val.push(item)
        },

        // Получение инвойса
        GetInvoice(id) {
            this.id = id;
            axios
                .get(document.location.href, {
                    params: {
                        e_invoices: id
                    }
                })
                .then(response => {
                    (this.editions_val = response.data.invoice.editions_val.map(item =>{
                        if (response.data.editions_id.indexOf(item.edition.id) != -1){
                            item.status2 = false
                        }else {
                            item.status2 = true
                        }
                        item.sends_amount = 0
                        item.sends = 0
                        item.loading2 = false
                        item.loading = false
                        return item
                    }));
                    (this.editionss=response.data.editions.map(item =>{
                        item.style = false;
                        item.quantity = 0;
                        item.amount = 0;
                        return item
                    })),
                    // (this.editions = response.data.editions),
                    (this.ready_s=response.data.invoice.status),
                    (this.number = response.data.invoice.number),
                    (this.power_of_attorney = response.data.invoice.power_of_attorney),

                    (this.invoice = response.data.invoice),
                    (this.createI = false),
                    (this.statusInvoice = true),
                    (this.mylist=response.data.invoice.status),
                    (this.loading=false),
                    (this.getInv=true)
                })
                .catch(function(error) {
                    console.log(error);
                });
        },

        getMylist(){
            if (this.mylist){
                this.mylist = false
            }else {
                this.mylist = true
            }

        },

        Clear(){
          this.createI = false,
          this.formCreate = {
            date: null,
            idx: null,
            provider: null,
            shipper: null,
            freight_carrier: null,
            number: null,
            power_of_attorney: null,
            date_power_of_attorney: null,
            confidant: null,
            year: null
            }
        },

        createInvoice(){
          this.loading = true
          data = {
            create_i: {
                date_write: moment(this.formCreate.date).format('YYYY-MM-DD'),
                idx: this.formCreate.idx,
                footing: this.formCreate.footing,
                members_of_commission: this.formCreate.members_of_commission,
            }
          };
          const self = this
          axios
                .post(document.location.href, data)
                .then((response) => {
                    (console.log(response.data)),
                    (self.invoices.push(response.data)),
                    (this.formCreate = {
                        date_write: null,
                        idx: null,
                        footing: null,
                        members_of_commission: null,
                    }),
                    (this.GetInvoice(response.data.id))
                })
                .catch(function(error) {
                });


        },

        SendConfidant() {
            var id = null;
            if (this.confidant) {
                id = this.confidant.id;
            }
            data = {
                id: this.invoice.id,
                confidant: id
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsconfidant = 1;
                })
                .catch(function(error) {
                    this.sendsconfidant = 2;
                });
        },

        nameWithLang({ last_name, first_name }) {
            return `${first_name} ${last_name}`;
        },

        datepickerClosedFunction2() {
            var time = moment(this.date_power_of_attorney).format("YYYY-MM-DD");
            data = {
                id: this.invoice.id,
                date_power_of_attorney: time
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.datepickerClosed2 = 1;
                })
                .catch(function(error) {
                    this.datepickerClosed2 = 2;
                });
        },

        customFormatter(date) {
            return moment(date).format("DD.MM.YYYY");
        },

        Sendshipper() {
            var id = null;
            if (this.shipper) {
                id = this.shipper.id;
            }
            data = {
                invoice: this.invoice.id,
                shipper: id
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsShipperr = 1;
                })
                .catch(function(error) {
                    this.sendsShipperr = 2;
                    console.log(error, "shipper");
                });
        },

        Sendprovider() {
            var id = null;
            if (this.provider) {
                id = this.provider.id;
            }
            data = {
                invoice: this.invoice.id,
                provider: id
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsProviderr = 1;
                })
                .catch(function(error) {
                    this.sendsProviderr = 2;
                    console.log(error, "shipper");
                });
        },

        EditNumberProviderFn2() {
            data = {
                id: this.invoice.id,
                number: this.number
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.EditNumberProvider23 = 1;
                }).catch(function(error) {
                    this.EditNumberProvider23 = 2;
                    console.log(error, "shipper");
                });

        },

        EditNumberProviderFn() {
            data = {
                id: this.invoice.id,
                power_of_attorney: this.power_of_attorney
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.EditNumberProvider2 = 1;
                })
                .catch(function(error) {
                    this.EditNumberProvider2 = 2;
                });
        },

        SendfFeightCarrier() {
            var id = null;
            if (this.freight_carrier) {
                id = this.freight_carrier.id;
            }
            data = {
                invoice: this.invoice.id,
                freight_carrier: id
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsfreight_carrier = 1;
                })
                .catch(function(error) {
                    this.sendsfreight_carrier = 2;
                    console.log(error, "shipper");
                });
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
            loading: false
        };
    }
});

Vue.component("EditionsList", {
    props: ["datamodel", "index", "datas", "invoice", "addfn", "editions_val", "getpush", "editions_val", "loading3", "ready_s"],
    template: "#editions-list",
    delimiters: ["{(", ")}"],
    data: function() {
        return {
            satus: false,
            satus2: false,
            sends: 0,
            sends2: 0,
            sends_amount: 0,
            quantity: 0,
            amount: 0,
            deletes: 0,
            loading2: false
        };
    },

    computed: {
        sums() {
            return (this.datamodel.amount * this.datamodel.quantity).toFixed(2)
        }
    },

    mounted(){
        if (this.datamodel.idx > 0){
            this.idx = this.datamodel.idx
            this.quantity=this.datamodel.quantity
            this.amount=this.datamodel.amount
        }
    },

    methods: {
        addEdition(datamodel){
          this.loading2 = true
          if (this.datamodel.quantity > 0 && this.datamodel.amount > 0){
              datas = {
                  create_edition_invoice:{
                      invoice: this.invoice.id,
                      edition: Number(this.datamodel.id),
                      quantity: Number(this.datamodel.quantity),
                      amount: Number(this.datamodel.amount),
                  }
              };

              axios
                  .post(document.location.href, datas).then(response => {
                        (this.editions_val(response.data.invoice.editions_val)),
                        (this.loading2=false)
                  })
                  .catch(error => {
                        (this.satus = "error"),
                        (this.loading2=false),
                        (this.sends = 2);
                        console.log(error, "rrrr");
              });

          }

        },

        delStatus(idx){
            if (Number(idx) > 0){
                return true
            }else {
                return false
            }
        },


        send() {
            if (this.datamodel.idx > 0 && this.datamodel.quantity > 0){
                data = {
                id: this.datamodel.idx,
                quantity: this.datamodel.quantity
                };
                axios
                    .post(document.location.href, data)
                    .then(response => {
                        (this.satus = "success"), (this.sends = 1);
                    })
                    .catch(error => {
                        (this.satus = "error"), (this.sends = 2);
                        console.log(error, "rrrr");
                    });

            }

        },

        sendAmount() {
            if (this.datamodel.idx > 0 && this.datamodel.amount > 0){
                data = {
                id: this.datamodel.idx,
                amount: this.datamodel.amount
                };
                axios
                    .post(document.location.href, data)
                    .then(response => {
                        (this.satus = "success"), (this.sends_amount = 1);
                    })
                    .catch(error => {
                        (this.satus = "error"), (this.sends_amount = 2);
                        console.log(error, "rrrr");
                    });

            }

        },

        sendplan() {
            if (this.datamodel.quantity > 0){
                data = {
                id: this.datamodel.idx,
                quantity: this.datamodel.quantity
                };
                axios
                    .post(document.location.href, data)
                    .then(response => {
                        (this.satus2 = "success"), (this.sends2 = 1);
                    })
                    .catch(error => {
                        (this.satus2 = "error"), (this.sends2 = 2);
                        console.log(error, "rrrr");
                });

            }

        },

        delEinvoice(){
            this.loading2 = true
            datas ={
                delete_e: Number(this.datamodel.idx)
            }
            axios
                .post(document.location.href, datas).then(response => {
                    (this.editions_val(response.data.editions_val)),
                    this.datamodel.idx = 0,
                    this.datamodel.quantity = 0,
                    this.datamodel.amount = 0,
                    this.loading2 = false
                })
                .catch(function(error) {
                    console.log(error, "error");
                });
        }
    }
});