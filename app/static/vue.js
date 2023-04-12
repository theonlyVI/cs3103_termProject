Vue.component("modal", {
    template: "#modal-template"
  });

const app = new Vue({
    el: '#app',
    data() {
        return {
            serviceURL: "https://cs3103.cs.unb.ca:49005",

            authenticated: false,
            iseditComment: false,
            schoolsData: null,
            commentsData: null,
            videoData: null,
            loggedIn: null,
            input: {
                username: "",
                password: ""
            },
            videos: [],

            currentUser:{
                idUser: 0,
                userName: ""
            },

            likedVideos: [],

            currentVideo:{
                idVideo: 2,
                videoPath: "/static/resources/videos/atoms.webm",
                uploadDate: "2023-03-26 13:44:43",
                idUser: 2,
                videoTitle: "xyz",
                videoDescription: "newdesc"
            },

            videoToUpload: {
                title: '',
                description: '',
                file: null
            },

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
                bio: 'What is up?!',
                profilePicture: '/static/resources/pfps/2947278_mihar34_pfp.png',
                // followers: 5000,
                videos: []
                // {
                //     id: 1,
                //     title: 'My first video',
                //     description: 'Is this video working?,?',
                //     src: 'static/resources/videos/mountains.webm',
                //     likes: 100
                // },
                // {
                //     id: 2,
                //     title: 'My second video',
                //     description: 'Some nature stuff I dont know..',
                //     src: 'static/resources/videos/ambientNature.webm',
                //     likes: 200
                // },
                // {
                //     id: 3,
                //     title: 'My third video',
                //     description: 'spinninggg',
                //     src: 'static/resources/videos/windmill.webm',
                //     likes: 300
                // }

            },
            selectedComment: {
                idComment: "",
                commentText: "",
                idUser: "",
                idVideo: ""
            },
            uploadComment:{
                commentBody: ""
            }
        }
    },
    methods: {
        playVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
        },
        uploadVideo() {
            let formData = new FormData();
            formData.append('title', this.videoToUpload['title']);
            formData.append('description', this.videoToUpload['description']);
            formData.append('file', this.videoToUpload['file']);
            axios
                .post('/Users/'.concat(this.input['username']).concat('/Videos'), formData)
                .then(response => {
                    console.log(response.data);
                }).catch(error => {
                    console.log(error);
                });
        },
        getAllUserVideos(username) {
            axios
                .get('Users/'.concat(username).concat('/Videos'))
                .then(response => {
                    this.user['videos'] = response.data;
                    // alert(this.user['videos'][0]['videoPath']);
                    for (let i = 0; i < this.user['videos'].length; i++) {
                        video = this.user['videos'][i];
                        axios
                            .get('Videos/'.concat(video['idVideo']).concat('/Like/Count'))
                            .then(likeReponse => {
                                this.user['videos'][i]['likeCount'] = likeReponse.data[0]['likeCount']
                                console.log(this.user['videos'][i]['likeCount'])
                            })
                    }
                });
            
        },
        handleFileUpload(event) {
            this.videoToUpload['file'] = event.target.files[0];
        },
        setCurrentVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
        },
        toggleLike() {
            this.isLiked = !this.isLiked;
        },
        likeVideo(videoId) {
            axios
                .post('/Users/'.concat(this.input['username']).concat('/Videos/').concat(videoId).concat('/Like'))
        },
        unlikeVideo(videoId) {
            axios
                .delete('/Users/'.concat(this.input['username']).concat('/Videos/').concat(videoId).concat('/Like'))
        },
        getProfile(username) {
            this.getAllUserVideos(username)
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
            axios
                .get('/Users/'.concat(this.input['username']).concat('/Videos/Liked'))
                .then(response => {
                    this.likedVideos = response.data;
                })

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
                            this.changePage('home');
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
                .delete(this.serviceURL + "/logout")
                .then(response => {
                    location.reload();
                })
                .catch(e => {
                    console.log(e);
                });
        },
        showDropdown() {
            document.getElementById("myDropdown").classList.toggle("show");
        },
        fetchComments(videoId){
            axios
            .get(this.serviceURL+"/Videos/".concat(videoId).concat("/Comments"))
            .then(response => {
                this.commentsData = response.data;
            });
        },
        fetchVideos(){
            axios
            .get(this.serviceURL+"/Videos")
            .then(response=>{
                this.videos=response.data;
            });
        },
        addComments(videoId){
            let formData = new FormData();
            formData.append('comment', this.uploadComment['commentBody']);
            axios
            .post('Users/'.concat(this.input['username']).concat("/Comments").concat('?video_id='.concat(videoId)), formData)
            .then(response=>{
                console.log(response.data);
            }).catch(error=>{
                console.log(error);
            });
            this.fetchComments(videoId);
            this.$forceUpdate();
            this.$refs.anyname.reset();
        },
        getUserInfo(){
            axios
            .get(this.serviceURL+"/Users/".concat(this.input['username']))
            .then(response=>{
                this.currentUser=response.data[0]
            });
    
        },
        letItBegin(){
            this.fetchVideos();
            this.login();
            this.getUserInfo();
        },
        showModal() {
            this.iseditComment = true;
        },
        hideModal() {
            this.iseditComment = false;
            console.log(this.selectedComment['commentText']);
            this.updateComment();
        },
        selectComment(commentId) {
            console.log(this.iseditComment);
            this.showModal();
            for (x in this.commentsData) {
                if (this.commentsData[x].idComment == commentId) {
                this.selectedComment = this.commentsData[x];
                }
            }
            console.log(this.selectedComment['commentText']);
        },
        updateComment(){
            let formData = new FormData();
            formData.append('comment',this.selectedComment['commentText'])
            axios
            .patch('Users/'.concat(this.input['username']).concat("/Comments/").concat(this.selectedComment['idComment']), formData)
            .then(response=>{
                console.log(response.data);
            }).catch(error=>{
                console.log(error);
            });
            this.fetchComments(this.currentVideo['idVideo']);
            this.$forceUpdate();
        },
        deleteComment(commentId){
            axios
            .delete('Users/'.concat(this.input['username']).concat("/Comments/").concat(commentId));
            this.fetchComments(this.currentVideo['idVideo']);
            this.$forceUpdate();
        }

    }
});
