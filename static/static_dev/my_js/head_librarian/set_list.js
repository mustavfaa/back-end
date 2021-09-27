axios.defaults.xsrfHeaderName = "X-CSRFToken";
Vue.component("vue-multiselect", window.VueMultiselect.default);

new Vue({
  el: "#Appset",
  delimiters: ["{(", ")}"],
  data: {
    ru: true,
    kk: false,
    not: true,
    token: "",
    sets: []
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
    axios
      .get(urlLanguage + "cabinet/head_librarian/create_sets/api/list/?token=" + token)
      .then(
        response => (
          (self.sets = response.data),
          (self.not = false)
        )
      )
      .catch(function (error) {
        console.log(error);
      });
  }
});

Vue.component("ClassList", {
  props: ["item", "index"],
  template: "#class-list",
  delimiters: ["{(", ")}"]
});

Vue.component("EditionsList", {
  props: ["item", "index"],
  delimiters: ["{(", ")}"],
  template: "#editions-list"
});