const app = new Vue({
    el: '#app',
    data() {
        return {
            serviceURL: "https://cs3103.cs.unb.ca:49005",

            authenticated: false,
            schoolsData: null,
            loggedIn: null,
            input: {
                username: "",
                password: ""
            },
            videos: [
                {
                    title: 'Atoms',
                    src: '/static/resources/videos/atoms.webm',
                },
                {
                    title: 'Funny Dog Video',
                    src: '/static/resources/videos/mountains.mp4',
                },
                {
                    title: 'Awesome Skateboarding Video',
                    src: '/static/resources/videos/windmill.mp4',
                },
            ],

            currentVideo: null,

            showMenu: false,

            imageUrl: '/static/resources/icons/heart.png',
            colorFilter: 'grayscale(100%)',
            isColorful: false,
            isLiked: false,

            // user info part   

            pages: {
                login: true,
                home: false,
                profile: false,
                upload: false,
            },

            user: {
                name: 'John Doe',
                bio: 'What is up?!',
                profilePicture: '/static/resources/pfps/2947278_mihar34_pfp.png',
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
            this.changePage('profile')
        },
        getHome() {
            this.changePage('home')
        },
        getUpload() {
            this.changePage('upload')
        },
        changePage(selected_page) {
            for (page in this.pages) {
                if (selected_page == page) {
                    this.pages[selected_page] = true;
                }
                else {
                    this.pages[page] = false;
                }
            }

        },
        login() {
            if (this.input.username != "" && this.input.password != "") {
                axios
                    .post(this.serviceURL + "/login", {
                        "username": this.input.username,
                        "password": this.input.password
                    })
                    .then(response => {
                        if (response.data.status == "success") {
                            this.authenticated = true;
                            this.loggedIn = response.data.user_id;
                            this.changePage('home')
                        }
                    })
                    .catch(e => {
                        alert("The username or password was incorrect, try again");
                        this.input.password = "";
                        console.log(e);
                    });
            } else {
                alert("A username and password must be present");
            }
        },
        logout() {
            axios
            .delete(this.serviceURL+"/logout")
            .then(response => {
                location.reload();
            })
            .catch(e => {
                console.log(e);
            });
        }
    }
});
