Vue.component("modal", {
    template: "#modal-template"
})

const app = new Vue({
    el: '#app',
    data() {
        return {
            serviceURL: "https://cs3103.cs.unb.ca:8017",

            authenticated: false,
            schoolsData: null,
            loggedIn: null,
            input: {
                username: "",
                password: ""
            },
            currentUser: {
                idUser: null,
                username: ""
            },

            // Comment data part ------
            isEditComment: false,
            commentsData: null,
            // ------------------------

            videoData: null, // current video

            videos: [],

            likedVideos: [],
            likedVideoIds: [],
            likeCounts: {},
            videoToEdit: {
                'id': null,
                'title': null,
                'description': null,

            },

            currentVideo: {
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
                edit: false,
                liked: false
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
            uploadComment: {
                commentBody: ""
            }
        }
    },
    methods: {
        playVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
            // console.log(this.getLikeCountVideo(this.currentVideo['idVideo']))
            this.getLikeCountVideo(this.currentVideo['idVideo'])
            this.$set(this.currentVideo,'likeCount', this.likeCounts[this.currentVideo['idVideo']])
        },
        uploadVideo() {
            let formData = new FormData();
            var form = document.getElementById("myForm");

            // Check if the form is valid
            if (form.checkValidity()) {
                formData.append('title', this.videoToUpload['title']);
                formData.append('description', this.videoToUpload['description']);
                formData.append('file', this.videoToUpload['file']);
                axios
                    .post('/Users/'.concat(this.input['username']).concat('/Videos'), formData)
                    .then(response => {
                        console.log(response.data)
                        this.getProfile(this.input['username'])
                    }).catch(error => {
                        console.log(error);
                    });
            } else {
                // Display an error message or do something else
                alert("Please fill out all required fields.");
            }

        },
        getAllUserVideos(username) {
            axios
                .get('Users/'.concat(username).concat('/Videos'))
                .then(response => {
                    this.user['videos'] = response.data;
                    // alert(this.user['videos'][0]['videoPath']);
                    for (let i = 0; i < this.user['videos'].length; i++) {
                        video = this.user['videos'][i];
                        this.getLikeCountVideo(video['idVideo'])
                    }
                });

        },
        handleFileUpload(event) {
            this.videoToUpload['file'] = event.target.files[0];
        },
        setCurrentVideo() {
            this.currentVideo = this.videos[Math.floor(Math.random() * this.videos.length)];
        },
        getLikedVideos() {
            axios
                .get('/Users/'.concat(this.input['username']).concat('/Videos/Liked'))
                .then(response => {
                    this.likedVideos = response.data
                    this.likedVideoIds = []
                    console.log(this.likedVideos)
                    for (let i = 0; i < this.likedVideos.length; i++) {
                        this.likedVideoIds.push(this.likedVideos[i]['idVideo'])
                    }
                    // console.log(this.likedVideoIds)
                })
        },
        getLikedPage() {
            this.getLikedVideos()
            this.changePage('liked')
        },
        toggleLike(videoId) {
            if (this.likedVideoIds.includes(videoId)) {
                this.unlikeVideo(videoId)
            } else {
                this.likeVideo(videoId)
            }
            this.getLikeCountVideo(videoId)
            console.log(this.likeCounts)
        },
        getLikeCountVideo(videoId) {
            axios
                .get('Videos/'.concat(videoId).concat('/Like/Count'))
                .then(response => {
                    this.$set(this.likeCounts, videoId, response.data[0]['likeCount'])
                    console.log(this.likeCounts[videoId])
                }).catch(error => {
                    console.log(error)
                })
        },
        likeVideo(videoId) {
            axios
                .post('/Users/'.concat(this.input['username']).concat('/Videos/').concat(videoId).concat('/Like'))
            this.getLikedVideos()
        },
        unlikeVideo(videoId) {
            axios
                .delete('/Users/'.concat(this.input['username']).concat('/Videos/').concat(videoId).concat('/Like'))
            this.getLikedVideos()
        },
        getProfile(username) {
            this.getAllUserVideos(username)
            this.changePage('profile')
        },
        // Set the videoEditId to the video id of the video to be edited
        getEdit(videoId) {
            this.videoToEdit['id'] = videoId
            this.videoToEdit['title'] = null
            this.videoToEdit['description'] = null
            this.changePage('edit')
        },
        editVideo() {
            let formData = new FormData();
            var form = document.getElementById("myForm");
            // Check if the form is valid
            if (form.checkValidity()) {
                formData.append('title', this.videoToEdit['title']);
                formData.append('description', this.videoToEdit['description']);

                axios
                    .put('/Users/'.concat(this.input['username']).concat('/Videos/').concat(this.videoToEdit['id']), formData)
                    .then(response => {
                        this.getProfile(this.input['username'])
                    }).catch(error => {
                        console.log(error)
                    })
            } else {
                // Display an error message or do something else
                alert("Please fill out all required fields.");
            }


        },
        deleteVideo(videoId) {
            if (confirm("Do you really want to delete this video?")) {
                axios
                    .delete('/Users/'.concat(this.input['username']).concat('/Videos/').concat(videoId))
                    .then(response => {
                        this.getProfile(this.input.username)
                    }).catch(error => {
                        console.log(error)
                    })

            }
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
            this.getLikedVideos()
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
        fetchComments(videoId) {
            axios
                .get(this.serviceURL + "/Videos/".concat(videoId).concat("/Comments"))
                .then(response => {
                    this.commentsData = response.data;
                });
        },
        fetchVideos() {
            axios
                .get('/Videos')
                .then(response => {
                    this.videos = response.data;
                })
        },
        addComments(videoId) {
            let formData = new FormData();
            formData.append('comment', this.uploadComment['commentBody']);
            axios
                .post('Users/'.concat(this.input['username']).concat("/Comments").concat('?video_id='.concat(videoId)), formData)
                .then(response => {
                    console.log(response.data);
                }).catch(error => {
                    console.log(error);
                });
            this.fetchComments(videoId);
            this.$forceUpdate();
            this.$refs.anyname.reset();
        },
        getUserInfo() {
            axios
                .get(this.serviceURL + "/Users/".concat(this.input['username']))
                .then(response => {
                    this.currentUser = response.data[0]
                });

        },
        letItBegin() {
            this.fetchVideos();
            this.login();
            this.getUserInfo();
        },
        showModal() {
            this.isEditComment = true;
        },
        hideModal() {
            this.isEditComment = false;
            console.log(this.selectedComment['commentText']);
            this.updateComment();
        },
        selectComment(commentId) {
            console.log(this.isEditComment);
            this.showModal();
            for (x in this.commentsData) {
                if (this.commentsData[x].idComment == commentId) {
                    this.selectedComment = this.commentsData[x];
                }
            }
            console.log(this.selectedComment['commentText']);
        },
        updateComment() {
            let formData = new FormData();
            formData.append('comment', this.selectedComment['commentText'])
            axios
                .patch('Users/'.concat(this.input['username']).concat("/Comments/").concat(this.selectedComment['idComment']), formData)
                .then(response => {
                    console.log(response.data);
                }).catch(error => {
                    console.log(error);
                });
            this.fetchComments(this.currentVideo['idVideo']);
            this.$forceUpdate();
        },
        deleteComment(commentId) {
            axios
                .delete('Users/'.concat(this.input['username']).concat("/Comments/").concat(commentId));
            this.fetchComments(this.currentVideo['idVideo']);
            this.$forceUpdate();
        }


    }
});
