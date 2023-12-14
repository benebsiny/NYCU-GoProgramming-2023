package main

import (
	"flag"
	"github.com/gocolly/colly"
)

func main() {

	flag.Parse()

	c := colly.NewCollector()

	c.OnHTML("???", func(e *colly.HTMLElement) {
	})
}
