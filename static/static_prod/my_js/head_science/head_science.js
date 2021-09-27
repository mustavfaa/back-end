axios.defaults.xsrfHeaderName = 'X-CSRFToken';
new Vue({
    el: "#app",
    delimiters: ["{(", ")}"],
    data: {
      token: "",
      schoolTitul: [],
      amaunt: '',
      schoolTitulForm: {
        klass: 0,
        liter: 0,
        students: 0,
        year: 0,
        language: 0,
        study_direction: 0
      }
    },

    methods:{
        remove: function(index, item){
            self = this
            axios({
              method: 'DELETE',
              url: '/cabinet/head_science/api/delete/' + item.id,
              data: {token: self.token},
              headers: {'Content-Type': 'application/json'}
            }).then(function (response) {
              self.schoolTitul.splice(index, 1);
            })
            .catch(function (error) {
              console.log(error);
            });

        },

        computeMyBind() {
            var sum = this.schoolTitul.reduce(function(acc, equity) {
              return acc + parseInt(equity.students);
            }, 0);
            return sum;
        },

        aAdd() {
            const self = this;
            data1 = {
                token: this.token,
                klass: Number(this.schoolTitulForm.klass),
                liter: this.schoolTitulForm.liter,
                students: Number(this.schoolTitulForm.students),
                year: Number(this.schoolTitulForm.year),
                language: Number(this.schoolTitulForm.language),
                study_direction: Number(this.schoolTitulForm.study_direction),
            }
            axios.post('/cabinet/head_science/api/school_titul/add/', data1).then(function (response) {
                 self.schoolTitul = response.data;
            })
            .catch(function (error) {
              console.log(error);
            })
        }
    },

    mounted() {
      const el = document.getElementById('token');
      var token = el.dataset.token;
      this.token = token
      const self = this;
      axios
        .get(
          "/cabinet/head_science/school_titul_list/?token=" + token
        )
        .then(response => (this.schoolTitul = response.data)).catch(function (error) {
        console.log(error);
      });
    }

});