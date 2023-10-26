package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"
)

// TODO: Create a struct to hold the data sent to the template

func Calculator(w http.ResponseWriter, r *http.Request) {
	// TODO: Finish this function
}

func main() {
	http.HandleFunc("/", Calculator)
	log.Fatal(http.ListenAndServe(":8084", nil))
}
