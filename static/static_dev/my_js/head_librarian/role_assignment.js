axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
  el: "#app",
  delimiters: ["{(", ")}"],
  data: {
    token: "",
    users: [],
    groups: [],
    role_list: [],
    history_roles: [],
    groups_list_b: [],
    user: {
      last_name: "Имя",
      first_name: "Фамилия"
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

    axios
      .get(urlLanguage + "cabinet/head_librarian/roles/api/", {
        headers: {
          token: self.token
        }
      })
      .then(
        response => (
          (this.users = response.data.users.map(user => {
            return Object.assign({}, user.user, {
              avatar: "https://eportfolio.kz/static/images" + user.avatar.substr(6)
            });
          })),
          (self.history_roles = response.data.role_history.map(function (sh) {
            if (sh.user.portfolio_set) {
              sh.user.portfolio_set =
                "https://eportfolio.kz/static/images" +
                sh.user.portfolio_set[0].avatar;
            } else {
              sh.user.portfolio_set = "";
            }
            return sh;
          })),
          (self.role_list = response.data.role_list.map(function (sh) {
            if (sh.user.portfolio_set) {
              sh.user.portfolio_set =
                "https://eportfolio.kz/static/images" +
                sh.user.portfolio_set[0].avatar;
            } else {
              sh.user.portfolio_set = "";
            }
            return sh;
          })),
          (self.groups_list_b = response.data.groups)
        )
      )
      .catch(function (error) {
        console.log(error);
      });
  },

  methods: {
    nameWithLang({
      last_name,
      first_name,
      username
    }) {
      return `${last_name} ${first_name} / ${username}`;
    },
    aAdd() {
      data = {
        token: this.token,
        user: this.user,
        groups: this.groups.map(group => {
          return {
            role: group.id
          };
        })
      };
      axios
        .post(urlLanguage + "cabinet/head_librarian/roles/api/", data)
        .then(function (response) {
          location.reload();
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    cheCkid(user) {
      this.groups = user.groups;
      return console.log(user);
    }
  }
});

Vue.component("roles-list", {
  props: ["roles", "tokens"],
  delimiters: ["{(", ")}"],
  template: "#roles-list"
});

Vue.component("end-role", {
  props: ["role", "token"],
  delimiters: ["{(", ")}"],
  template: "#end-role",

  methods: {
    theEndP() {
      data = {
        token: this.token,
        role: this.role
      };
      axios
        .post(urlLanguage + "cabinet/head_librarian/roles/api/end/", data)
        .then(function (response) {
          location.reload();
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});