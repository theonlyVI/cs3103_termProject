const app = new Vue({
    el: '#app',
    data() {
        return {
            videos: [
                {
                    title: 'Atoms',
                    src: '../resources/videos/atoms.mp4',
                },
                {
                    title: 'Funny Dog Video',
                    src: '../resources/videos/mountains.mp4',
                },
                {
                    title: 'Awesome Skateboarding Video',
                    src: '../resources/videos/windmill.mp4',
                },
            ],

            currentVideo: null,

            showMenu: false,

            imageUrl: '../resources/icons/heart.png',
            colorFilter: 'grayscale(100%)',
            isColorful: false,
            isLiked: false,

            // user info part
            
            isHome: false,
            isProfile: false,
            isLogin: true,

            user: {
                name: 'John Doe',
                bio: 'What is up?!',
                profilePicture: '../resources/pfps/2947278_mihar34_pfp.png',
                // followers: 5000,
                videos: [
                    {
                        id: 1,
                        title: 'My first video',
                        description: 'Is this video working?,?',
                        src: '../resources/videos/mountains.mp4',
                        likes: 100
                    },
                    {
                        id: 2,
                        title: 'My second video',
                        description: 'Some nature stuff I dont know..',
                        src: '../resources/videos/ambientNature.mp4',
                        likes: 200
                    },
                    {
                        id: 3,
                        title: 'My third video',
                        description: 'spinninggg',
                        src: '../resources/videos/windmill.mp4',
                        likes: 300
                    }
                ]
            }
        }
    },
    created() {
        this.setCurrentVideo();
    },
    methods: {
        playVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
        },
        toggleColor() {
            this.isColorful = !this.isColorful;
            this.colorFilter = this.isColorful ? 'saturate(0%) hue-rotate(0deg)' : 'grayscale(100%)';
        },
        setCurrentVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
        },
        toggleLike() {
            this.isLiked = !this.isLiked;
        },
        getProfile() {
            this.isProfile = true;
            this.isHome = false;
            this.isLogin = false;
        },
        getHome() {
            this.isHome = true;
            this.isProfile = false;
            this.isLogin = false;
        },
        login() {
            this.isLogin = false;
            this.isHome = true;
            this.isProfile = false;
            // if (this.input.username != "" && this.input.password != "") {
            //   axios
            //   .post(this.serviceURL+"/login", {
            //       "username": this.input.username,
            //       "password": this.input.password
            //   })
            //   .then(response => {
            //       if (response.data.status == "success") {
            //         this.authenticated = true;
            //         this.loggedIn = response.data.user_id;
            //       }
            //   })
            //   .catch(e => {
            //       alert("The username or password was incorrect, try again");
            //       this.input.password = "";
            //       console.log(e);
            //   });
            // } else {
            //   alert("A username and password must be present");
            // }
          },
      
        //   fetchVideos() {
        //     alert("do i do this one?");
        //   }
        
    }
});
