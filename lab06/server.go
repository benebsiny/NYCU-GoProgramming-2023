package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Go server is running on http://localhost:8086")
	log.Fatal(http.ListenAndServe(":8086", http.FileServer(http.Dir("."))))
}
