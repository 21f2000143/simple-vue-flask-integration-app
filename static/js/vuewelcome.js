// for global messaging for alert or notifications
const Alert=Vue.component('alert',{
  template:`
  <div v-if="alertMessage" :class="theme">
    ${ this.alertMessage }
    <span class="close" @click="dismissAlert">&times;</span>
  </div>
  `,
  data(){
    return{
      alertMessage:'',
      theme:''
    }
  },
  methods:{
    showMessage(message, color){
      this.showMessage=message;
      this.theme=color;
    },
    dismissAlert() {
      this.alertMessage = '';
  },
},
  mounted: function () {
    source = new EventSource("/stream");
    source.addEventListener('greeting', event => {
      let data = JSON.parse(event.data);
      this.alertMessage = data.message;
      this.theme = data.color;
    }, false);
  }
})
// related with venues

const venueView = Vue.component('venueview',{
  template: `
  <div>
    <div class="col-md-6">
      <!-- Theatre Image -->
      <img src="/static/img/kids-zone-collection.avif" alt="Theatre Image" class="img-fluid">
      <h2>Theatre Name: <span>{{venue_name}}</span></h2>
        <p><strong>Location:</strong> City, Country</p>
        <p>
          <strong>Description:</strong> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tempus dolor
          eget lectus ullamcorper, eu fermentum ligula tincidunt.
        </p>
    </div>
    <div class="col-md-6">
    <router-view></router-view>
    </div>
  </div>
  `,
  data: function() {
      return {
          venue_id: null,
          venue_name: null,
          venue_place: null,
          venue_capacity: null,
          venue_location: null,
          price_factor: null,
          status:''
      }
  },
  methods: {
      fetch_for_one: function () {
          url="http://127.0.0.1:8000/theatre/" + this.$route.params.id;
          console.log(url)
          fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.venue_id=data['venue_id'];
                this.venue_name=data['venue_name'];
                  this.venue_place=data['venue_place'];
                  this.venue_location=data['venue_location'];
                  this.venue_capacity=data['venue_capacity'];
                  this.price_factor==data['price_factor'];
            }).catch((error) => {
                console.error('Error:', error);
                console.log("Error occured");
            });
      }
  },
  // computed: {
  //     count: function() {
  //         return this.messages.length;
  //     }
  // },

  created: function() {
      this.fetch_for_one();
  },
  mounted: function() {
      source = new EventSource("/stream");
      source.addEventListener('report', event => {
        let data = JSON.parse(event.data);
        this.alertMessage=data.message;
      }, false);
  } 
})


// related with shows

const showView = Vue.component('showview',{
  template: `
  <div>
    <div class="col-md-6">
      <!-- Theatre Image -->
      <img :src="'/static/img/' + img_name" alt="Theatre Image" class="img-fluid">
      <h2>Show Name: <span>{{show_name}}</span></h2>
        <p><strong>Location:</strong> City, Country</p>
        <p>
          <strong>Description:</strong> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tempus dolor
          eget lectus ullamcorper, eu fermentum ligula tincidunt.
        </p>
    </div>
    <div class="col-md-6">
    <router-view></router-view>
    </div>
  </div>
  `,
  data: function() {
      return {
        show_id:null,
        show_name:null,
        img_name:null,
        show_likes:null,
        show_tag:null,
        show_price:null,
        show_stime:null,
        show_etime:null,
        venueList:[]
      }
  },
  methods: {
      fetch_for_one: function () {
          url="http://127.0.0.1:8000/api/get/one/show/" + this.$route.params.id;
          console.log(url)
          fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.show_id=data['show_id'];
                this.show_name=data['show_name'];
                this.img_name=data['img_name'];
                this.show_likes=data['show_likes'];
                this.show_tag=data['show_tag'];
                this.show_price=data['show_price'];
                this.show_stime==data['show_stime'];
                this.show_etime==data['show_etime'];
                this.venueList==data['venueList'];
            }).catch((error) => {
                console.error('Error:', error);
                console.log("Error occured");
            });
      }
  },
  created: function() {
      this.fetch_for_one();
  }
})


// related with admin dashboard
const welcomeHome = Vue.component('adminhome', {
  props:['location', 'search_words'],
  template: `
  <div class="col">
    <div v-if="successMessage && receivedMessages" class="alert">
      {{ successMessage }}
      <span class="close" @click="clearReceivedMessage">&times;</span>
    </div>
    <alert></alert>
    <div v-if="empty">
        <div class="alert alert-info" role="alert" style="margin-top: 4.5%;">
            No shows and venues Available.
        </div>
    </div>
    <div v-else>
        <top-three-shows></top-three-shows>
        <toptrendinggenres></toptrendinggenres>
        <div v-if="search_words">
            <div v-for="data in matches" :key="data.seq_no" :data-list-item="data" class="text-center">
                <a style="font-family: 'Kanit', sans-serif; cursor: pointer;" @click="goVenue(data.venue_id)">{{ data.venue_name }}</a>
                <div class="scroll-container">
                  <div v-for="item in data.shows" :key="item.seq_no" class="card scroll-item">
                      <a href="#"><img :src="'/static/img/' + item.img_name" @click="actions(item.show_id)" class="d-block w-100 h-10 curve-corner" alt="..."></a>
                      <div class="card-body">
                          <h5 class="card-title">{{ item.show_stime }} - {{ item.show_etime }}</h5>
                          <a v-if="item.no_seats>0" class="btn btn-primary" href="/login">Book Ticket</a>
                          <a v-else class="btn btn-danger" disabled>Show full</a>
                      </div>
                  </div>
                </div>
            </div>
        </div>
        <div v-else>
            <div v-for="data in datalist" :key="data.seq_no" class="text-center">
            <a style="font-family: 'Kanit', sans-serif; cursor: pointer;" @click="goVenue(data.venue_id)">{{ data.venue_name }}</a>
                <div class="scroll-container">
                <div v-for="item in data.shows" :key="item.seq_no" class="card scroll-item">
                    <a href="#"><img :src="'/static/img/' + item.img_name" @click="actions(item.show_id)" class="d-block w-100 h-10 curve-corner" alt="..."></a>
                    <div class="card-body">
                        <h5 class="card-title">{{ item.show_stime }} - {{ item.show_etime }}</h5>
                        <a v-if="item.no_seats>0" class="btn btn-primary" href="/login">Book Ticket</a>
                        <a v-else class="btn btn-danger" disabled>Show full</a>
                    </div>
                </div>
                </div>
            </div>
        </div>
    </div>
</div>
  `,
  data() {
    return{
    empty: false,
    datalist: [],
    matches: [],
    alertMessage:'',
    receivedMessages: true
  }
  },
  methods: {
     fetch_for_one: function () {
      url = `http://127.0.0.1:8000/api/location/${localStorage.location}`
       fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data, "inside home fetchone");
          this.datalist = data;
          console.log(this.location);
          if (this.datalist.length == 0) {
            this.empty = true;
          }
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    fetch_all: function () {
       fetch("http://127.0.0.1:8000/api/get/venue")
        .then(response => response.json())
        .then(data => {
          console.log(data, "inside home object, fetch all");
          this.datalist = data;
          if (this.datalist.length == 0) {
            this.empty = true;
          }
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
          this.loading=false
        });
    },
    marked_location() {
      localStorage.setItem("location", this.location);
      url = `http://127.0.0.1:8000/api/location/${localStorage.location}`
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data, "inside home object");
          this.datalist = data;
          console.log(this.location);
          if (this.datalist.length == 0) {
            this.empty = true;
          }
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    search_engine() {
      console.log(this.search_words)
      console.log("inside search engine");
      url = `http://127.0.0.1:8000/api/search/${this.search_words}`
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.matches = data;
          console.log(this.location);
          if (this.matches.length == 0) {
            this.empty = true;
          }
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    dismissAlert() {
      this.alertMessage = '';
    },
    clearReceivedMessage(){
      this.receivedMessages=false;
    },
    actions(id){
      this.$router.push('/admin/view/show/' + id);
    },
    goVenue(id){
      this.$router.push('/admin/view/venue/' + id);
    },
    book(showid, venueid){
      this.$router.push('/user/view/show/'+showid+'/'+venueid +'/'+'book')
    }
  },
  created: function () {
    if (localStorage.location) {
      this.fetch_for_one()
      console.log("location from parent", this.location)
      console.log("search word from parent", this.search_words)
    }
    else {
      this.fetch_all()
      console.log("location from parent", this.location)
      console.log("search word from parent", this.search_words)
    }
    
  },
  watch: {
    location: function (newLocation, oldLocation) {
      this.marked_location();
    },
    search_words: function (newSearchWords, oldSearchWords) {
      this.search_engine();
    },
  },
  computed: {
    successMessage() {
      const message = this.$store.state.successMessage;
      if (message) {
        this.$store.commit('clearSuccessMessage');
        return message;
      }
      return '';
    },
  },
})

const TopThreeShows = Vue.component('top-three-shows', {
  template: `<div><label for="" style="font-family: 'Courgette', cursive;">Top 3 Movies</label>
  <div class="row" style="margin-bottom: 20px;">
    <div class="col">
      <div id="carouselExampleInterval" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active" data-bs-interval="10000">
            <img :src="movie1" class="d-block w-100 h-10" alt="...">
          </div>
          <div class="carousel-item" data-bs-interval="2000">
            <img :src="movie2" class="d-block w-100 h-10" alt="...">
          </div>
          <div class="carousel-item">
            <img :src="movie3" class="d-block w-100 h-10" alt="...">
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleInterval" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  </div></div>`,
  data: function () {
      return {
          movie1: '/static/img/',
          movie2: '/static/img/',
          movie3: '/static/img/',
      }
  },
  methods:{
    actions(id){
      this.$router.replace('/admin/view/show/' + id);
    }
  },
  mounted() {
      fetch("http://127.0.0.1:8000/api/get/top3/movies")
          .then(response => response.json())
          .then(data => {
              console.log(data);
              this.movie1 = this.movie1 + data.image1;
              this.movie2 = this.movie2 + data.image2;
              this.movie3 = this.movie3 + data.image3;
          }).catch((error) => {
              console.error('Error:', error);
              console.log("Error occured");
          });
  }
})

const TopTrendingGenres = Vue.component('toptrendinggenres', {
  template: `<div><label for="" style="font-family: 'Courgette', cursive;">Most watched movies</label>
  <div class="row" style="margin-bottom: 20px;">
    <div class="col d-flex justify-content-center">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col">
          <div class="card ">
            <img :src="genre1" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div class="col">
          <div class="card ">
            <img :src="genre2" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div class="col">
          <div class="card ">
            <img :src="genre3" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div class="col">
          <div class="card ">
            <img :src="genre4" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
      </div>
    </div>
  </div></div>`,
  data: function () {
      return {
          genre1: '/static/img/',
          genre2: '/static/img/',
          genre3: '/static/img/',
          genre4: '/static/img/',
      }
  },
  methods:{
    actions(id){
      this.$router.replace('/admin/view/show/' + id);
    }
  },
  mounted() {
      fetch("http://127.0.0.1:8000/api/get/top/genres")
          .then(response => response.json())
          .then(data => {
              console.log(data);
              this.genre1 = this.genre1 + data.image1;
              this.genre2 = this.genre2 + data.image2;
              this.genre3 = this.genre3 + data.image3;
              this.genre4 = this.genre4 + data.image3;
          }).catch((error) => {
              console.error('Error:', error);
              console.log("Error occured");
          });
  }
})


// const NotFound = { template: '<p>Page not found</p>' }


// Vue router
const routes = [
    { path: '/', component: welcomeHome },
    { path: '/admin/view/venue/:id', component: venueView },
    { path: '/admin/view/show/:id', component: showView},
];
const router = new VueRouter({
    routes // short for `routes: routes`
})


// creating vue store using vuex
const store = new Vuex.Store({
  state: {
    successMessage: '',
  },
  mutations: {
    setSuccessMessage(state, message) {
      state.successMessage = message;
    },
    clearSuccessMessage(state) {
      state.successMessage = '';
    },
  },
})

//Vue instance: the main app
var app = new Vue({
  el: "#app",
  delimiters: ['${', '}'],
  router: router,
  store: store,
  data: {
    location: "",
    locations: [],
    alertMessage: '',
    search_words: '',
  },
  methods: {
    changed_location() {
      localStorage.setItem("location", this.location);
      url = `http://127.0.0.1:8000/api/location/${localStorage.location}`
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.datalist = data;
          console.log(this.location);
          if (this.datalist.length == 0) {
            this.empty = true;
          }
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    activated_search() {
      this.search_words = document.getElementById('search_words').value;
    },
    
    },
  created: function () {
    fetch("http://127.0.0.1:8000/api/get/venue")
      .then(response => response.json())
      .then(data => {
        for (const value of data) {
          if (this.locations.includes(value['venue_location'])) {
            console.log(value['venue_location'], "inside main")
          }
          else {
            this.locations.push(value['venue_location'])
            console.log(value['venue_location'], "inside main")
          }
        }
      }).catch((error) => {
        console.error('Error:', error);
        console.log("Error occured");
    })
  }
})