package main

import (
	"github.com/stretchr/testify/assert"
	"os"
	"strings"
	"testing"
)

func TestLab08(t *testing.T) {
	var err error
	r2, w2, _ := os.Pipe()
	stdout := os.Stdout

	defer func() {
		os.Stdout = stdout
	}()
	os.Stdout = w2

	buf := make([]byte, 10240)
	var n int

	main()
	n, err = r2.Read(buf)
	if err != nil {
		t.Fatal(err)
	}

	expected := strings.Repeat("沒夾到喔！\n", 50)
	assert.Equal(t, expected, string(buf[:n]))
}
