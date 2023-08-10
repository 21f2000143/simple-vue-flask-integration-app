// for global messaging for alert or notifications
const Alert = Vue.component('alert', {
  template: `
  <div v-if="alertMessage" :class="theme">
    <strong>Holy guacamole!</strong> {{ alertMessage }}
    <button type="button" class="btn-close" @click="dismissAlert"></button>
  </div>
  `,
  data() {
    return {
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    showMessage(message, color) {
      this.showMessage = message;
      this.theme = color;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
  },
  mounted: function () {
    source = new EventSource("/stream");
    source.addEventListener('notifyadmin', event => {
      let data = JSON.parse(event.data);
      this.alertMessage = data.message;
      this.theme = data.color;
    }, false);
  }
})

// related with venues
const viewReport = Vue.component('viewreport', {
  template: `
  <div class="card p-3 justify-content-center">
    <div class="row">
        <table class="table">
            <thead>
              <tr>
                <th scope="col">Venue Name</th>
                <th scope="col">Show Name</th>
                <th scope="col">Show Rating</th>
                <th scope="col">Number of bookings</th>
              </tr>
            </thead>
            <tbody v-for="(item,index) in row" :key="index">
              <tr>
                <td>{{item["Venue Name"]}}</td>
                <td>{{item["Show Name"]}}</td>
                <td>{{item["Show Rating"]}}</td>
                <td>{{item["Number of bookings"]}}</td>
              </tr>
            </tbody>
        </table>
    </div>
<span class="close" style="cursor: pointer;" @click="closeForm">&times;</span>
</div>
  `,
  data: function () {
    return {
      row: []
    }
  },
  methods: {
    getdata: function () {
      url = `http://127.0.0.1:8000/ts/admin/venue/report`
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.row = data
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    closeForm() {
      router.push('/admin/view/venue/' + this.$route.params.id)
    }
  },
  created: function () {
    this.getdata()
  }
})

const deleteVenue = Vue.component('deletevenue', {
  template: `
  <div class="card p-3 justify-content-center">
        <div v-if="alertMessage" :class="theme">
          {{ alertMessage }}
          <span class="close" style="cursor: pointer;" @click="dismissAlert">&times;</span>
        </div>
        <span @click="closeForm" style="cursor: pointer;">&times;</span>
        <p class="h3">Deletinng Venue</p>
        <form @submit.prevent="onSubmit">
          <div class="row-md-6">
            <div class="input-group">
              <input type="text" v-model="vname" class="form-control" placeholder="Venue Name" readonly>
            </div>
            <br>
            <div class="row-md-6">
              <input type="text" v-model="vplace" class="form-control" placeholder="Place" readonly>
            </div>
            <br>
            <div class="row-md-6">
              <input type="text" v-model="vlocation" class="form-control" placeholder="Location" readonly>
            </div>
            <br>
            <div class="row-md-6">
              <input type="number" v-model="vcapacity" class="form-control" placeholder="Capacity" readonly>
            </div>
            <br>
            <div class="row-12 d-flex justify-content-center">
              <button class="btn btn-outline-secondary" type="submit">Confirm</button>
            </div>
          </div>
        </form>
</div>
  `,
  data() {
    return {
      vname: null,
      vplace: null,
      vlocation: null,
      vcapacity: null,
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    onSubmit() {
        url = "http://127.0.0.1:8000/api/get/venue/" + this.$route.params.id;
        fetch(url, {
          method: 'DELETE',
        })
          .then(response => {
            if (response.status === 200) {
              this.showMessage("Delete Successfully", "alert alert-success");
            } else {
              this.showMessage("Something went wrong!", "alert alert-danger")
              console.log('Request failed with status: ' + response.status);
            }
  
            if (response.status === 404) {
              console.log('Resource not found');
            }
            if (response.status === 400) {
              this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
              console.log('Resource not found');
            }
            response.json()
          })
          .then(data => {
            console.log('Success:', data);
            this.$store.commit('setSuccessMessage', 'Venue successfully deleted');
            this.$router.replace('/');
          })
          .catch((error) => {
            console.error('Error:', error);
            this.showMessage("Something went wrong!", "alert alert-danger")
          });
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
    closeForm() {
      router.push('/admin/view/venue/' + this.$route.params.id)
    }
  },
  created: function () {
    url = "http://127.0.0.1:8000/admin/theatre/" + this.$route.params.id;
    console.log(url)
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        this.venue_id = data['venue_id'];
        this.vname = data['venue_name'];
        this.vplace = data['venue_place'];
        this.vlocation = data['venue_location'];
        this.vcapacity = data['venue_capacity'];
      }).catch((error) => {
        console.error('Error:', error);
        console.log("Error occured");
      });
  }
})

const editVenue = Vue.component('editvenue', {
  template: `
  <div class="card p-3 justify-content-center">
      <div v-if="alertMessage" :class="theme">
        {{ alertMessage }}
        <div style="cursor: pointer" @click="dismissAlert">&times;</div>
      </div>
      <span class="close" style="cursor: pointer;" @click="closeForm">&times;</span>
      <p class="h3">Editing Venue</p>
      <form @submit.prevent="onSubmit">
      <div class="row-md-6">
          <div class="input-group">
          <input type="text" v-model="vname" class="form-control" placeholder="Venue Name" >
          </div>
          <br>
          <div class="row-md-6">
          <input type="text" v-model="vplace" class="form-control" placeholder="Place" >
          </div>
          <br>
          <div class="row-md-6">
          <input type="text" v-model="vlocation" class="form-control" placeholder="Location" >
          </div>
          <br>
          <div class="row-md-6">
          <input type="number" v-model="vcapacity" class="form-control" placeholder="Capacity" >
          </div>
          <br>
          <div class="row-md-6">
          <input type="text" v-model="pricefactor" class="form-control" placeholder="pricefactor">
          </div>
          <br>
          <div class="row-12 d-flex justify-content-center">
          <button class="btn btn-outline-secondary" type="submit">save</button>
          </div>
      </div>
      </form>
  </div>
  `,
  data() {
    return {
      vname: null,
      vplace: null,
      vlocation: null,
      vcapacity: null,
      pricefactor: null,
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    onSubmit() {
      if (this.vname || this.vplace || this.vlocation || this.vcapacity) {
        url = "http://127.0.0.1:8000/api/get/venue/" + this.$route.params.id;
        console.log(url)
        fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "venue_name": this.vname,
            "venue_place": this.vplace,
            "venue_capacity": this.vcapacity,
            "venue_location": this.vlocation,
            "price_factor": this.pricefactor
          }),
        })
          .then(response => {
            if (response.status === 200) {
              this.showMessage("Update Successfully", "alert alert-success");
            } else {
              this.showMessage("Something went wrong!", "alert alert-danger")
              console.log('Request failed with status: ' + response.status);
            }
  
            if (response.status === 404) {
              console.log('Resource not found');
            }
            if (response.status === 400) {
              this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
              console.log('Resource not found');
            }
            response.json()
          })
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
        this.showMessage("No change, nothing entered", "alert alert-warning")
      }
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
    closeForm() {
      router.push('/admin/view/venue/' + this.$route.params.id)
    }
  },
  created: function () {
    url = "http://127.0.0.1:8000/admin/theatre/" + this.$route.params.id;
    console.log(url)
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        this.venue_id = data['venue_id'];
        this.vname = data['venue_name'];
        this.vplace = data['venue_place'];
        this.vlocation = data['venue_location'];
        this.vcapacity = data['venue_capacity'];
        this.pricefactor = data['price_factor'];
      }).catch((error) => {
        console.error('Error:', error);
        console.log("Error occured");
      });
  }
})

const addVenue = Vue.component('addvenue', {
  template: `
  <div>
  <div v-if="alertMessage" :class="theme">
    <strong>Holy guacamole!</strong> {{ alertMessage }}
    <button me-2 type="button" class="btn-close" style="cursor: pointer" @click="dismissAlert"></button>
  </div>
  <div class=" col d-flex justify-content-center">
  <div class="card p-3" style="width: 18rem;">
    <form class="row g-3" @submit.prevent="onSubmit">
      <div class="row-md-6">
        <div class="input-group">
          <input type="text" v-model="vname" class="form-control" placeholder="Venue Name" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="text" v-model="vplace" class="form-control" placeholder="Place" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="text" v-model="vlocation" class="form-control" placeholder="Location" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="number" v-model="vcapacity" class="form-control" placeholder="Capacity" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="text" v-model="pricefactor" class="form-control" placeholder="Enter Pricefactor in int or float">
        </div>
        <br>
        <div class="row-12 d-flex justify-content-center">
          <button class="btn btn-outline-secondary" type="submit">save</button>
        </div>
      </div>
    </form>
  </div>
  </div>
  </div>
  `,
  data() {
    return {
      vname: null,
      vplace: null,
      vlocation: null,
      vcapacity: null,
      pricefactor: null,
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    onSubmit() {
      if (this.vname && this.vplace && this.vlocation && this.vcapacity) {
        url = `http://127.0.0.1:8000/api/get/venue`
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "venue_name": this.vname,
            "venue_place": this.vplace,
            "venue_capacity": this.vcapacity,
            "venue_location": this.vlocation,
            "price_factor": this.pricefactor
          }),
        })
        .then(response => {
          if (response.status === 200) {
            this.showMessage("Created Successfully", "alert alert-success");
          } else {
            this.showMessage("Something went wrong!", "alert alert-danger")
            console.log('Request failed with status: ' + response.status);
          }

          if (response.status === 404) {
            console.log('Resource not found');
          }
          if (response.status === 400) {
            this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
            console.log('Resource not found');
          }
          response.json()
        })
        .then(data => {
          console.log('Success:', data);
          console.log('Success:', data);

        })
        .catch((error) => {
          console.error('Error:', error);

        });
      } else {
        this.showMessage("Please fill the the fields", "alert alert-warning")
      }
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
  },
})

const venueView = Vue.component('venueview', {
  template: `
  <div class="row">
    <div class="col-md-6 mb-3">
      <!-- Theatre Image -->
      <img src="/static/img/kids-zone-collection.avif" alt="Theatre Image" class="img-fluid">
      <h2>Theatre Name: <span>{{venue_name}}</span></h2>
        <p><strong>Location:</strong> City, Country</p>
        <p>
          <strong>Description:</strong> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tempus dolor
          eget lectus ullamcorper, eu fermentum ligula tincidunt.
        </p>
        <div v-if="status === 'progress'">
          <button class="btn btn-primary" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Generating...
          </button>
        </div>
        <div v-else-if="status === 'success'">
          <div class="d-grid gap-2 mt-3">
          <button class="btn btn-dark"><router-link :to="'/admin/view/venue/' + $route.params.id + '/report'">View report</router-link></button>
          </div>
        </div>
        <div v-else-if="status === 'error'">
          <button class="btn btn-danger" type="button" disabled>Something went wrong</button>
        </div>
        <div v-else>
          <div class="d-grid gap-2 mt-3">
            <button @click="generate" class="btn btn-primary">Get Report</button>
          </div>
        </div>
        <div class="d-grid gap-2 mt-3">
            <button class="btn btn-dark"><router-link :to="'/admin/view/venue/' + $route.params.id + '/delete'">Delete venue</router-link></button>
            <button class="btn btn-dark"><router-link :to="'/admin/view/venue/' + $route.params.id + '/edit'">Edit venue</router-link></button>
            <input type="hidden">
        </div>
    </div>
    <div class="col-md-6 mt-3">
      <router-view></router-view>
    </div>
  </div>
  `,
  data: function () {
    return {
      venue_id: null,
      venue_name: null,
      venue_place: null,
      venue_capacity: null,
      venue_location: null,
      price_factor: null,
      status: ''
    }
  },
  methods: {
    generate: function () {
      this.status = 'progress';
      const url = "http://127.0.0.1:8000/get/report/" + this.venue_id;
      console.log(url)
      fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          this.status = data.status;
        })
        .catch((error) => {
          console.error('Error:', error);
          this.status = "error";
        });
    },
    fetch_for_one: function () {
      url = "http://127.0.0.1:8000/admin/theatre/" + this.$route.params.id;
      console.log(url)
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.venue_id = data['venue_id'];
          this.venue_name = data['venue_name'];
          this.venue_place = data['venue_place'];
          this.venue_location = data['venue_location'];
          this.venue_capacity = data['venue_capacity'];
          this.price_factor == data['price_factor'];
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    }
  },
  created: function () {
    this.fetch_for_one();
  }
})


// related with shows
const addShow = Vue.component('addshow', {
  template: `
  <div>
  <div v-if="alertMessage" :class="theme">
    <strong>Holy guacamole!</strong> {{ alertMessage }}
    <button me-2 type="button" class="btn-close" style="cursor: pointer" @click="dismissAlert"></button>
  </div>
  <div class=" col d-flex justify-content-center">
  <div class="card p-3" style="width: 18rem;">
    <form class="row g-3" @submit.prevent="onSubmit">
      <div class="row-md-6">
        <div class="input-group">
          <input type="text" v-model="sname" class="form-control" placeholder="Show Name" required>
        </div>
        <br>
        <div class="input-group mb-3">
          <label class="input-group-text" for="inputGroupSelect02">Select Image</label>
          <select v-model="selectedImage" class="form-select" id="inputGroupSelect02">
            <option selected>Choose image...</option>
            <option v-for="(item, index) in imagesList" :key="index" :value="item">{{item}}</option>
          </select>
        </div>
        <br>
        <div class="row-md-6">
          <input type="text" v-model="stag" class="form-control" placeholder="Show Tag" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="text" v-model="sprice" class="form-control" placeholder="Show Price" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="time" v-model="sstime" class="form-control" placeholder="Start Time" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="time" v-model="setime" class="form-control" placeholder="End Time" required>
        </div>
        <br>
        <div class="row-md-6">
          <input type="date" v-model="show_date" class="form-control" placeholder="Set Date" required>
        </div>
        <br>
        <div class="input-group mb-3">
          <label class="input-group-text" for="inputGroupSelect02">Select Venue</label>
          <select v-model="selectedVenue" class="form-select" id="inputGroupSelect02">
            <option selected>Choose...</option>
            <option v-for="(data, index) in venueList" :key="index" :value="data.venue_id">{{data.venue_name}}</option>
          </select>
        </div>
        <br>
        <div class="row-12 d-flex justify-content-center">
          <button class="btn btn-outline-secondary" type="submit">save</button>
        </div>
      </div>
    </form>
  </div>
  </div>
</div> 
  `,
  data() {
    return {
      sname: null,
      stag: null,
      sprice: null,
      sstime: null,
      setime: null,
      show_date: null,
      selectedVenue: null,
      selectedImage: null,
      alertMessage: '',
      theme: '',
      imagesList: [],
      venueList: []
    }
  },
  methods: {
    onSubmit() {
      if (this.sname && this.stag && this.sprice && this.sstime && this.setime && this.selectedVenue && this.selectedImage) {
        url = "http://127.0.0.1:8000/api/get/show"
        console.log(this.selectedImage)
        console.log(this.selectedVenue)
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "show_name": this.sname,
            "img_name": this.selectedImage,
            "show_price": this.sprice,
            "show_stime": this.sstime,
            "show_etime": this.setime,
            "selecte_venue": this.selectedVenue,
            "show_tag": this.stag,
            "show_date": this.show_date,
          }),
        })
          .then(response => {
            if (response.status === 200) {
              this.showMessage("Created Successfully", "alert alert-success");
            } else {
              this.showMessage("Something went wrong!", "alert alert-danger")
              console.log('Request failed with status: ' + response.status);
            }
  
            if (response.status === 404) {
              console.log('Resource not found');
            }
            if (response.status === 400) {
              this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
              console.log('Resource not found');
            }
            response.json()
          })
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
        this.showMessage("Please fill the the fields", "alert alert-warning")
      }
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
  },
  created: function () {
    fetch("http://127.0.0.1:8000/admin/create/show")
      .then(response => response.json())
      .then(data => {
        this.imagesList = data.images;
        console.log(this.imagesList)
        this.venueList = data.venue;
        console.log(this.venueList)
        console.log(this.venueList[0])
      }).catch((error) => {
        console.error('Error:', error);
        console.log("Error occured");
      })
  },

})

const showView = Vue.component('showview', {
  template: `
  <div class="row">
    <div class="col-md-6 mb-3">
      <!-- Theatre Image -->
      <img :src="'/static/img/' + img_name" alt="Theatre Image" class="img-fluid">
      <h2>Show Name: <span>{{show_name}}</span></h2>
        <p><strong>Location:</strong> City, Country</p>
        <p>
          <strong>Description:</strong> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed tempus dolor
          eget lectus ullamcorper, eu fermentum ligula tincidunt.
        </p>
        <div>
          <div class="d-grid gap-2 mt-3">
            <button class="btn btn-dark"><router-link :to="'/admin/view/show/' + $route.params.id + '/delete'">Delete show</router-link></button>
            <button class="btn btn-dark"><router-link :to="'/admin/view/show/' + $route.params.id + '/edit'">Edit show</router-link></button>
            <input type="hidden">
          </div>
        </div>
    </div>
    <div class="col-md-6 mt-3">
    <router-view></router-view>
    </div>
  </div>
  `,
  data: function () {
    return {
      show_id: null,
      show_name: null,
      img_name: null,
      show_likes: null,
      show_tag: null,
      show_price: null,
      show_stime: null,
      show_etime: null,
      venueList: []
    }
  },
  methods: {
    fetch_for_one: function () {
      url = "http://127.0.0.1:8000/api/get/one/show/" + this.$route.params.id;
      console.log(url)
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.show_id = data['show_id'];
          this.show_name = data['show_name'];
          this.img_name = data['img_name'];
          this.show_likes = data['show_likes'];
          this.show_tag = data['show_tag'];
          this.show_price = data['show_price'];
          this.show_stime == data['show_stime'];
          this.show_etime == data['show_etime'];
          this.venueList == data['venueList'];
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    }
  },
  created: function () {
    this.fetch_for_one();
  }
})

const deleteShow = Vue.component('deleteshow', {
  template: `
  <div class="card p-3 justify-content-center">
    <div v-if="alertMessage" :class="theme">
        {{ alertMessage }}
        <span class="close" style="cursor: pointer;" @click="dismissAlert">&times;</span>
    </div>
    <span class="close" style="cursor: pointer;" @click="closeForm">&times;</span>
    <p class="h3">Deleting Show from every venues</p>
    <form  @submit.prevent="onSubmit">
        <div class="row-md-6">
        <div class="input-group">
            <input type="text" v-model="show_name" class="form-control" readonly>
        </div>
        <br>
        <div class="row-md-6">
            <input type="text" v-model="show_tag" class="form-control" readonly>
        </div>
        <br>
        <div class="row-md-6">
            <input type="number" v-model="show_price" class="form-control" readonly>
        </div>
        <br>
        <div class="row-md-6">
            <input type="text" v-model="show_stime" class="form-control" readonly>
        </div>
        <br>
        <div class="row-md-6">
            <input type="text" v-model="show_etime" class="form-control" readonly>
        </div>
        <br>
        <div class="row-md-6">
            <input type="text" v-model="show_date" class="form-control" readonly>
        </div>
        <br>
        <div class="row-12 d-flex justify-content-center">
            <button class="btn btn-outline-secondary" type="submit">Confirm Delete</button>
        </div>
        </div>
    </form>
</div>
  `,
  data: function () {
    return {
      show_id: null,
      show_name: null,
      show_likes: null,
      show_tag: null,
      show_price: null,
      show_stime: null,
      show_etime: null,
      show_date: null,
      venueList: [],
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    onSubmit() {
      url = "http://127.0.0.1:8000/api/get/show/" + this.$route.params.id;
      console.log(url)
      fetch(url, {
        method: 'DELETE',
      })
        .then(response =>{
          if (response.status === 200) {
            this.showMessage("Delete Successfully", "alert alert-success");
          } else {
            this.showMessage("Something went wrong!", "alert alert-danger")
            console.log('Request failed with status: ' + response.status);
          }

          if (response.status === 404) {
            console.log('Resource not found');
          }
          if (response.status === 400) {
            this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
            console.log('Resource not found');
          }
          response.json()
        } )
        .then(data => {
          console.log('Success:', data);
          this.$store.commit('setSuccessMessage', 'Show successfully deleted');
          this.$router.replace('/');
        })
        .catch((error) => {
          console.error('Error:', error);
          this.showMessage("Please fill the the fields", "alert alert-danger")
        });
    },
    fetch_for_one: function () {
      url = "http://127.0.0.1:8000/api/get/one/show/" + this.$route.params.id;
      console.log(url)
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.show_id = data['show_id'];
          this.show_name = data['show_name'];
          this.show_likes = data['show_likes'];
          this.show_tag = data['show_tag'];
          this.show_price = data['show_price'];
          this.show_stime = data['show_stime'];
          this.show_etime = data['show_etime'];
          this.show_date = data['show_date'];
          this.venueList = data['venueList'];
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
    closeForm() {
      router.push('/admin/view/show/' + this.$route.params.id)
    }
  },
  created: function () {
    this.fetch_for_one()
  }
})

const editShow = Vue.component('editshow', {
  template: `
  <div class="card p-3 justify-content-center">
        <div v-if="alertMessage" :class="theme">
          {{ alertMessage }}
          <span class="close" style="cursor: pointer;" @click="dismissAlert">&times;</span>
        </div>
        <span class="close" style="cursor: pointer;" @click="closeForm">&times;</span>
        <p class="h3">Editing Show</p>
        <form class="row g-3" @submit.prevent="onSubmit">
          <div class="row-md-6">
            <div class="input-group">
              <input type="text" v-model="show_name" class="form-control"  >
            </div>
            <br>
            <div class="row-md-6">
              <input type="text" v-model="show_tag" class="form-control" >
            </div>
            <br>
            <div class="row-md-6">
              <input type="number" v-model="show_price" class="form-control" >
            </div>
            <br>
            <div class="row-md-6">
              <input type="time" v-model="show_stime" class="form-control" >
            </div>
            <br>
            <div class="row-md-6">
              <input type="time" v-model="show_etime" class="form-control" >
            </div>
            <br>
            <div class="row-md-6">
              <input type="date" v-model="show_date" class="form-control" >
            </div>
            <br>
            <div class="row-12 d-flex justify-content-center">
              <button class="btn btn-outline-secondary" type="submit">Edit</button>
            </div>
          </div>
        </form>
</div>
  `,
  data: function () {
    return {
      show_id: null,
      show_name: null,
      show_tag: null,
      show_price: null,
      show_stime: null,
      show_etime: null,
      show_date: null,
      venueList: [],
      alertMessage: '',
      theme: ''
    }
  },
  methods: {
    onSubmit() {
      if (this.show_name || this.show_likes || this.show_tag || this.show_price || this.show_stime || this.show_etime || this.show_date) {
        url = "http://127.0.0.1:8000/api/get/show/" + this.$route.params.id;
        console.log(url)
        fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "show_name": this.show_name,
            "show_likes": this.show_likes,
            "show_tag": this.show_tag,
            "show_price": this.show_price,
            "show_stime": this.show_stime,
            "show_etime": this.show_etime,
            "show_date": this.show_date
          }),
        })
          .then(response => {
            if (response.status === 200) {
              this.showMessage("Update Successfully", "alert alert-success");
            } else {
              this.showMessage("Something went wrong!", "alert alert-danger")
              console.log('Request failed with status: ' + response.status);
            }
  
            if (response.status === 404) {
              console.log('Resource not found');
            }
            if (response.status === 400) {
              this.showMessage('Status message: ' + response.statusText, "alert alert-danger")
              console.log('Resource not found');
            }
            response.json()
          })
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      } else {
        this.showMessage("No change, nothing entered", "alert alert-warning")
      }
    },
    fetch_for_one: function () {
      url = "http://127.0.0.1:8000/api/get/one/show/" + this.$route.params.id;
      console.log(url)
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.show_id = data['show_id'];
          this.show_name = data['show_name'];
          this.show_likes = data['show_likes'];
          this.show_tag = data['show_tag'];
          this.show_price = data['show_price'];
          this.show_stime = data['show_stime'];
          this.show_etime = data['show_etime'];
          this.venueList = data['venueList'];
          this.show_date = data['show_date'];
        }).catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
        });
    },
    showMessage(message, theme) {
      this.alertMessage = message;
      this.theme = theme;
    },
    dismissAlert() {
      this.alertMessage = '';
    },
    closeForm() {
      router.push('/admin/view/show/' + this.$route.params.id)
    }
  },
  created: function () {
    this.fetch_for_one();
  }
})


// related with admin dashboard
const AdminHome = Vue.component('adminhome', {
  props: ['location', 'search_words'],
  template: `
  <div class="col">
    <div v-if="successMessage && receivedMessages" class="alert alert-success">
      <strong>Holy guacamole!</strong> {{ successMessage }}
      <button type="button" class="btn-close" @click="clearReceivedMessage"></button>
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
                          <button class="btn btn-primary" @click="actions(item.show_id)">View</button>
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
                      <button class="btn btn-primary" @click="actions(item.show_id)">View</button>
                  </div>
              </div>
              </div>
          </div>
        </div>
    </div>
</div>
  `,
  data() {
    return {
      empty: false,
      datalist: [],
      matches: [],
      alertMessage: '',
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
        .then(response => {
          if (response.status === 200) {
           
              console.log('Request resource successful');
          }
           else {
            console.log('Request failed with status: ' + response.status);
          }

          if (response.status === 404) {
            console.log('Resource not found');
          }
          if (response.status === 400) {
            console.log('Resource not found');
          }
          return response.json()
        }).then(data=>{
          this.datalist = data;
          if (this.datalist.length == 0) {
            this.empty = true;
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          console.log("Error occured");
          this.loading = false
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
    clearReceivedMessage() {
      this.receivedMessages = false;
    },
    actions(id) {
      this.$router.push('/admin/view/show/' + id);
    },
    goVenue(id) {
      this.$router.push('/admin/view/venue/' + id);
    },
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
          <div v-if="movie1" class="carousel-item active" data-bs-interval="10000">
            <img :src="movie1" class="d-block w-100 h-10" alt="...">
          </div>
          <div v-if="movie2" class="carousel-item" data-bs-interval="2000">
            <img :src="movie2" class="d-block w-100 h-10" alt="...">
          </div>
          <div v-if="movie3" class="carousel-item">
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
        <div  class="col">
          <div class="card ">
            <img :src="genre1" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div  class="col">
          <div class="card ">
            <img :src="genre2" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div  class="col">
          <div class="card ">
            <img :src="genre3" class="card-img-top curve-corner" alt="...">
          </div>
          <div class="card-footer">
            <small class="text-muted">Last updated 3 mins ago</small>
          </div>
        </div>
        <div  class="col">
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
  mounted() {
    fetch("http://127.0.0.1:8000/api/get/top/genres")
      .then(response => {
        if (response.status === 200) {
          console.log('requst resource successful');
        } else {
          console.log('Request failed with status: ' + response.status);
        }

        if (response.status === 404) {
          console.log('Resource not found');
        }
        if (response.status === 400) {
          console.log('Resource not found');
        }
        return response.json()
      }).then(data => {
          this.genre1 = this.genre1 + data.image1;
          this.genre2 = this.genre2 + data.image2;
          this.genre3 = this.genre3 + data.image3;
          this.genre4 = this.genre4 + data.image4;
      })
      .catch((error) => {
        console.error('Error:', error);
        console.log("Error occured");
      });
  }
})


// const NotFound = { template: '<p>Page not found</p>' }


// Vue router
const routes = [
  { path: '/', component: AdminHome },
  { path: '/admin/create/venue', component: addVenue },
  { path: '/admin/view/venue/:id', component: venueView, children: [{ path: 'edit', component: editVenue }, { path: 'delete', component: deleteVenue }, { path: 'report', component: viewReport }] },
  { path: '/admin/view/show/:id', component: showView, children: [{ path: 'edit', component: editShow }, { path: 'delete', component: deleteShow }] },
  { path: '/admin/create/show', component: addShow }
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
  delimiters: ["${", "}"],
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
      .then(response => {
        if (response.status === 200) {
          console.log('successful');
        } else {
          console.log('Request failed with status: ' + response.status);
        }

        if (response.status === 404) {
          console.log('Resource not found');
        }
        if (response.status === 400) {
          console.log('Resource not found');
        }
        return response.json()
      }).then(data => {
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