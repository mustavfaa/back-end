axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
    el: "#Invoice",
    delimiters: ["{(", ")}"],
    data: {
        ru: vdp_translation_ru.js,
        disabledDates: {
            to: new Date(2019, 1, 23),
            from: new Date(2030, 1, 26)
        },
        EditNnumber: 0,
        sendsShipper: 0,
        sendsconfidant: 0,
        datepickerClosed: 0,
        datepickerClosed2: 0,
        EditNumberProvider2: 0,
        sendsfreight_carrier: 0,
        loading: true,
        loading2: false,
        id: null,
        number: null,
        shipper: null,
        customer: null,
        provider: null,
        confidant: null,
        date_extracts: null,
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
        formStyle: "form-control",
        briefcase: "",
        menu_edition: "",
        datas: [],
        years: [],
        liters: [],
        klasses: [],
        subjects: [],
        invoices: [],
        editions: [],
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

            var all = this.editions_val;
            if (this.klass || this.language || this.subject || this.edition) {
                filter = {
                    edition: {}
                };
                if (this.klass) {
                  filter.edition.klass = this.klass.name;
                }
                if (this.language) {
                  filter.edition.language = this.language.name;
                }
                if (this.subject) {
                    filter.edition = this.subject.name
                }
                if (this.edition) {
                  filter.edition = this.edition;
                }

                all = _.filter(all, filter);
                return all;
              } else {
                return all;
              }

        },

        Summs(){
            var sums = 0
            this.invoices.map(item =>{
                sums = sums + item.sum
                return item
            })
            return sums
        },

        SummEditions(){
            var sum = {
                pq_amount: 0,
                q_amount: 0,
                amount: 0
            };
            this.filterEditions2.forEach(item =>{

                sum.amount = sum.amount + (item.amount * item.planned_quantity);
                sum.pq_amount = Number(sum.pq_amount) + Number(item.planned_quantity);
                sum.q_amount = Number(sum.q_amount) + Number(item.quantity);

                return item
            });
            return sum
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
                (this.invoices = response.data.invoices.map((item) => {
                    item.checked = 0
                    item.len = 0
                    item.sum = 0
                    item.editions_val.map((ed) =>{
                        if (ed.planned_quantity == ed.quantity){
                            item.checked = item.checked + 1
                        }
                        item.len = item.len + 1;
                        item.sum = item.sum + (ed.amount * ed.planned_quantity);
                        return ed
                    })
                    return item
                })),
                (this.klasses = response.data.klasses),
                (this.providers = response.data.providers),
                (this.languages = response.data.languages),
                (this.loading=false)
            })
            .catch(function(error) {
                console.log(error);
            });
    },

    methods: {
        Ready(){
            this.loading2 = true;
            data = {
             ready: this.invoice.id,
             status_r: this.invoice.status
            };
            axios
                .post(document.location.href, data)
                .then(response => {
                    this.invoice=response.data
                    this.loading2=false
                })
                .catch(function(error) {
                    console.log(error)
            });
        },

        datepickerClosedFunction(){
            var time = moment(this.date_extracts).format('YYYY-MM-DD');
            data = {
             id: this.invoice.id,
             date_extracts: time
            };
             axios
                .post(document.location.href, data)
                .then(response => {
                    this.datepickerClosed = 1
                })
                .catch(function(error) {
                    this.datepickerClosed = 2
                });
        },

        datepickerClosedFunction2(){
            var time = moment(this.date_power_of_attorney).format('YYYY-MM-DD');
            data = {
             id: this.invoice.id,
             date_power_of_attorney: time
            };
             axios
                .post(document.location.href, data)
                .then(response => {
                    this.datepickerClosed2 = 1
                })
                .catch(function(error) {
                    this.datepickerClosed2 = 2
                });
        },

        customFormatter(date) {
          return moment(date).format('DD.MM.YYYY');
        },

        SendfFeightCarrier(){
            var id = null
            if (this.freight_carrier){
                id = this.freight_carrier.id
            }
            data = {
             invoice: this.invoice.id,
             freight_carrier: id
            };

             axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsfreight_carrier = 1
                })
                .catch(function(error) {
                    this.sendsfreight_carrier = 2
                    console.log(error, 'shipper');
                });
        },

        SendConfidant(){
            var id = null
            if (this.confidant){
                id = this.confidant.id
            }
            data = {
             id: this.invoice.id,
             confidant: id
            };
             axios
                .post(document.location.href, data)
                .then(response => {
                    this.sendsconfidant = 1
                })
                .catch(function(error) {
                    this.sendsconfidant = 2
                });
        },

        nameWithLang ({ last_name, first_name }) {
          return `${first_name} ${last_name}`
        },

        EditNnumberFn(){
            data = {
             id: this.invoice.id,
             number: this.number
            };
             axios
                .post(document.location.href, data)
                .then(response => {
                    this.EditNnumber = 1
                })
                .catch(function(error) {
                    this.EditNnumber = 2
                });
        },

        EditNumberProviderFn(){
            data = {
             id: this.invoice.id,
             power_of_attorney: this.power_of_attorney
            };
             axios
                .post(document.location.href, data)
                .then(response => {
                    this.EditNumberProvider2 = 1
                })
                .catch(function(error) {
                    this.EditNumberProvider2 = 2
                });
        },

        Sendshipper(){
         data = {
             invoice: this.invoice.id,
             shipper: this.shipper.id
         };
         axios
            .post(document.location.href, data)
            .then(response => {
                this.sendsShipper = 1
            })
            .catch(function(error) {
                this.sendsShipper = 2
            });
        },

        sendEdition() {
            axios
                .post(document.location.href, Data)
                .then(response => {

                })
                .catch(function(error) {
                    console.log(error);
                });
        },

        // Получение инвойса
        GetInvoice(id){
            this.id = id;
            axios
                .get(document.location.href, {
                    params: {
                        e_invoices: id
                    }
                })
                .then(response => {
                    this.editions_val = Array(...response.data.invoice.editions_val);
                    (this.editions = response.data.editions),
                    (this.invoice = response.data.invoice),
                    (this.shipper=response.data.invoice.shipper),
                    (this.provider=response.data.invoice.provider),
                    (this.confidant=response.data.invoice.confidant),
                    (this.number_provider=response.data.invoice.number_provider),
                    (this.number=response.data.invoice.number),
                    (this.power_of_attorney=response.data.invoice.power_of_attorney),
                    (this.portfolios=response.data.portfolios),
                    (this.subjects=response.data.subjects),
                    (this.customer=response.data.customer),
                    (this.date_power_of_attorney=response.data.invoice.date_power_of_attorney),
                    (this.date_extracts=response.data.invoice.date_extracts),
                    (this.statusInvoice = true)
                })
                .catch(function(error) {
                    console.log(error);
                });

        },


        downloadPDF(id) {

            const params = {
                pdf_invoice: id,
            };

            axios.get(document.location.href, {responseType: 'blob', params: params})
                .then(response => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'file.pdf');
                    document.body.appendChild(link);
                    link.click();
                })
                .catch(error => {

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
            loading: false,
        };
    }

});

Vue.component("EditionsList", {
    props: ["datamodel", "index", "datas", "addfn", "invoice"],
    template: "#editions-list",
    delimiters: ["{(", ")}"],
    data: function() {
        return {
            satus: null,
            sends: 0
        };
    },
    computed:{
        Sums(){
            var a = this.datamodel.amount * this.datamodel.planned_quantity
            var b = a.toFixed(2)
            return b
        }
    },

    methods:{

        send(){
            if (Number(this.datamodel.quantity) >= 0 && Number(this.datamodel.quantity) <= Number(this.datamodel.planned_quantity)){
                data = {
                    id: this.datamodel.id,
                    quantity: this.datamodel.quantity
                };
                var data = this.datamodel;
                axios.post(document.location.href, data).then(response => {
                    this.satus = 'success',
                    this.sends = 1
                }).catch(error => {
                    this.satus = 'error',
                    this.sends = 2
                    console.log(error, 'rrrr');
                });
            }
            else {
                console.log('notval')
                this.satus = 'error'
                this.sends = 2
            }


        },



    }
});