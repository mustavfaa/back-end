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
            idx: null,
            date: null,
            provider: null,
            bin: null,
            number: null,
            date_invoice: null,
        },
        EditNnumber: 0,
        datepickerClosed: 0,
        datepickerClosed2: 0,
        sendsfreight_carrier: 0,
        addE: false,
        mylist: false,
        ready_s: false,
        loading: true,
        loading2: false,
        loading3: false,
        id: null,
        bin: null,
        number: null,
        date: null,
        invoice: null,
        provider: null,
        date_invoice: null,
        statusInvoice: false,
        year: "",
        time: "",
        token: "",
        klass: "",
        edition: "",
        subject: "",
        language: "",
        briefcase: "",
        menu_edition: "",
        errors: [],
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

            let all = this.editionss.map(item => {
                    item.quantity = 0
                    item.amount = 0
                    item.style = false
                    item.idx = ''
                    const sameElem = this.editions_val.find(el => item.id === el.edition.id);

                    if (sameElem){
                        item.idx = sameElem.id
                        item.quantity = sameElem.quantity
                        item.amount = sameElem.amount
                        item.style=true
                    }
                    return item;
            })

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
        axios
            .get(document.location.href, {
                params: {
                    all_invoices: true
                }
            })
            .then(response => {
                (this.invoices = response.data.invoices.map(item => {
                    item.sum = 0;
                    item.editions_val.map(ed => {
                        item.sum += ed.amount;
                        return ed;
                    });
                    return item;
                })),
                (this.klasses=response.data.klasss),
                (this.languages=response.data.languages),
                (this.subjects=response.data.subjects),
                (this.editionss=response.data.editions.map(item =>{
                    item.style = false;
                    item.quantity = 0;
                    item.amount = 0;
                    return item
                })),
                (this.years=response.data.years),
                (this.loading=false);
            })
            .catch(function(error) {
                console.log(error);
            });
    },

    methods: {
        getLength(val) {
            if (val){
                return val.length
            }
            else {
                return 0
            }
        },

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
                .post(document.location.href, datas).then(response => this.editions_val = this.editions_val.filter(item => item.id != response.data.id))
                .catch(function(error) {
                    console.log(error, "error");
                });
        },


        GetEditionsVal(data){
            this.editions_val = data
        },

        DelEditionsVal(id){
            return this.editions_val = this.editions_val.filter(item => item.id != id)
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
                status_r: this.invoice.status,
                invoice: this.invoice,
            }
            data.invoice.bin = Number(data.invoice.bin)
            data.invoice.date =  moment(data.invoice.date).format('YYYY-MM-DD')
            data.invoice.date_invoice =  moment(data.invoice.date_invoice).format('YYYY-MM-DD')
            delete data.invoice.status
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.defGETValid(response)
                })
                .catch(function(error) {
            });
        },

        defGETValid(response){
            if (response.data.errors){
                this.errors = response.data.errors
                this.ready_s = false
            }else {
                this.invoice=response.data;
                this.ready_s=response.data.status;
            }
            this.loading2=false;
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
                    (this.ready_s=response.data.invoice.status),
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
            date_invoice: null,
            bin: null,
            number: null,
            }
        },

        createInvoice(){
          this.loading = true
          data = {
            create_i: {
                date: moment(this.formCreate.date).format('YYYY-MM-DD'),
                idx: this.formCreate.idx,
                provider: this.formCreate.provider,
                bin: Number(this.formCreate.bin),
                number: this.formCreate.number,
                date_invoice: moment(this.formCreate.date_invoice).format('YYYY-MM-DD'),
            }
          };
          axios
                .post(document.location.href, data)
                .then(response => {
                    this.Validates(response)
                    this.loading = false
                })
                .catch(error => {
                    this.loading = false
                    console.log(error);
                });


        },

        Validates(response){
            if (response.data.errors){
                this.errors = response.data.errors
            }
            if (response.data.id){
                this.invoices.push(response.data);
                this.formCreate = {
                    date: null,
                    idx: null,
                    provider: null,
                    bin: null,
                    number: null,
                    date_invoice: null,
                };
                this.GetInvoice(response.data.id);
            }
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
    props: ["datamodel", "index", "datas", "invoice", "addfn", "editions_val", "getpush", "del_edition_val", "loading3", "ready_s", "get_edition_val"],
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
                        (this.get_edition_val(response.data.invoice.editions_val)),
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
            console.log(this.datamodel.idx)
            this.del_edition_val(this.datamodel.idx)

            axios
                .post(document.location.href, datas).then(response => {
                    (this.del_edition_val(response.data.id)),
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