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
            min: 1,
            max: 4,
            oneclik: true,
            notshow: false,
            name_year: {},
            pk: null,
            one: true,
            time: '',
            danger: false,
            sucsess: false,
            token: "",
            list: false,
            datas: [],
            school_tituls: [],
            school_tituls_p: [],
            years: [],
            plan_tituls: [],
            year_school_titul: [],
            number: 0,
            plan_year: "",
            year: "",
            get_plan: [],
            showResults: false,
            plantitul: false,
            dataTable: null,
        };
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
                        delete sh.id;
                        delete sh.deleted;
                        delete sh.date_added;
                        delete sh.exchange;
                        delete sh.comment;
                        sh.planned_quantity = 0;
                        // sh.klass++;
                        return sh;
                    })),
                    (self.years = response.data.years),
                    (self.datas = response.data.datas)
                )
            )
            .catch(function (error) {
                console.log(error);
            });
    },

    methods: {
        exspotB() {
            $("#table2excel").table2excel({
                exclude: ".noExl",
                name: "Worksheet Name",
                fileext: ".xls",
                filename: "Плановый титул " + this.name_year.name + ".xls", //do not include extension

            });
        },

        getPlan(pk) {
            const self = this;
            this.name_year = pk
            this.pk = pk.id
            var all = []
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
            this.notshow = true
            if (this.one == true) {
                this.one = false
            }
        },


        uPdateList() {
            const self = this;
            var datetime = new Date(Date.now()).toLocaleString().split(", ")[0];
            this.time = datetime + "/" + new Date(Date.now()).toLocaleString().split(", ")[1];
            var list = []
            this.get_plan.map(item => {
                list.push({
                    id: item.id,
                    planned_quantity: item.planned_quantity
                })
                return item
            })
            data = {
                token: this.token,
                school_tituls: list,
            }
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

        cReate(number, year) {
            const self = this;
            const newData = [];
            if (this.plan_year !== "") {
                if (this.min <= 1) {

                    this.school_tituls.forEach(function (el) {
                        if (el.year.id == self.plan_year.id) {
                            if ((el.klass + 1) < this.max) {
                                el.klass = el.klass + 1
                                newData.push({
                                    ...el
                                });
                            }
                        }
                    });

                    if (this.min == 0) {
                        newData.unshift({
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 2,
                                name: "Русский язык"
                            },
                            klass: 0,
                            students: 0,
                            planned_quantity: 0
                        }, {
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 1,
                                name: "Казахский язык"
                            },
                            klass: 0,
                            students: 0,
                            planned_quantity: 0
                        }, {
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 2,
                                name: "Русский язык"
                            },
                            klass: 1,
                            students: 0,
                            planned_quantity: 0
                        }, {
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 1,
                                name: "Казахский язык"
                            },
                            klass: 1,
                            students: 0,
                            planned_quantity: 0
                        });
                    }
                    if (this.min == 1) {
                        newData.unshift({
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 2,
                                name: "Русский язык"
                            },
                            klass: 1,
                            students: 0,
                            planned_quantity: 0
                        }, {
                            school: this.school_tituls[0].school,
                            liter: null,
                            language: {
                                id: 1,
                                name: "Казахский язык"
                            },
                            klass: 1,
                            students: 0,
                            planned_quantity: 0
                        })
                    }
                } else {
                    this.school_tituls.forEach(function (el) {
                        if (el.year.id === self.plan_year.id) {
                            if (this.max > el.klass) {
                                if (this.min == el.klass) {
                                    newData.push({
                                        ...el
                                    });
                                    el.klass = el.klass + 1
                                    newData.push({
                                        ...el
                                    });
                                } else {
                                    el.klass = el.klass + 1
                                    newData.push({
                                        ...el
                                    });
                                }
                            }
                        }
                    });

                }
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

                this.notshow = false
                // window.setTimeout(show_popup, 1000);
                this.list = false
                if (this.one) {
                    this.one = false
                }
            }
            if (this.oneclik) {
                this.oneclik = false
            }

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
    }
});

Vue.component("school-tituls", {
    props: ["index", "datamodel"],
    delimiters: ["{(", ")}"],
    data: function () {
        return {};
    },
    template: "#school-tituls"
});

Vue.component("years-list", {
    props: ["index", "year", "getplan", "name_year"],
    delimiters: ["{(", ")}"],
    data: function () {
        return {};
    },
    template: "#years_list"
});