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
                    src: 'https://www.w3schools.com/html/mov_bbb.mp4',
                },
            ],

            currentVideo: null,

            showMenu: false,

            imageUrl: '../resources/icons/heart.png',
            colorFilter: 'grayscale(100%)',
            isColorful: false,
            isLiked: false,
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
        }
    }
});
