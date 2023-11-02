package main

import (
	"log"
	"net/http"
)

// TODO: Please create a struct to include the information of a video

func YouTubePage(w http.ResponseWriter, r *http.Request) {
	// TODO: Get API token from .env file
	// TODO: Get video ID from URL query `v`
	// TODO: Get video information from YouTube API
	// TODO: Parse the JSON response and store the information into a struct
	// TODO: Display the information in an HTML page through `template`
}

func main() {
	http.HandleFunc("/", YouTubePage)
	log.Fatal(http.ListenAndServe(":8085", nil))
}
