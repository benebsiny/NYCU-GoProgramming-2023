package main

import (
	"github.com/gin-gonic/gin"
)

type Book struct {
	// TODO: Finish struct
}

var bookshelf = []Book{
	// TODO: Init bookshelf
}

func getBooks(c *gin.Context) {
}
func getBook(c *gin.Context) {
}
func addBook(c *gin.Context) {
}
func deleteBook(c *gin.Context) {
}
func updateBook(c *gin.Context) {
}

func main() {
	r := gin.Default()
	r.RedirectFixedPath = true

	// TODO: Add routes

	err := r.Run(":8087")
	if err != nil {
		return
	}
}
