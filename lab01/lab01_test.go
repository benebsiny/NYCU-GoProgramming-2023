package main

import (
	"fmt"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

var testCases = []struct {
	a, b, addExpected, subExpected, mulExpected, divExpected int64
}{
	{1, 2, 3, -1, 2, 0},
	{17, 3, 20, 14, 51, 5},
	{2147, 107, 2254, 2040, 229729, 20},
	{39957, 673, 40630, 39284, 26891061, 59},
	{45571256, 1007, 45572263, 45570249, 45890254792, 45254},
}

func TestAdd(t *testing.T) {
	for _, tc := range testCases {
		assert.Equal(t, tc.addExpected, Add(tc.a, tc.b))
	}
}

func TestSub(t *testing.T) {
	for _, tc := range testCases {
		assert.Equal(t, tc.subExpected, Sub(tc.a, tc.b))
	}
}

func TestMul(t *testing.T) {
	for _, tc := range testCases {
		assert.Equal(t, tc.mulExpected, Mul(tc.a, tc.b))
	}
}

func TestDiv(t *testing.T) {
	for _, tc := range testCases {
		assert.Equal(t, tc.divExpected, Div(tc.a, tc.b))
	}
}

func TestE2E(t *testing.T) {
	var err error

	r1, w1, _ := os.Pipe()
	r2, w2, _ := os.Pipe()

	stdin := os.Stdin
	stdout := os.Stdout

	defer func() {
		os.Stdin = stdin
		os.Stdout = stdout
	}()

	os.Stdin = r1
	os.Stdout = w2

	buf := make([]byte, 1024)
	var n int

	for _, tc := range testCases {
		input := fmt.Sprintf("%d\n%d\n", tc.a, tc.b)
		expected := fmt.Sprintf("Add: %d\nSubtract: %d\nMultiply: %d\nDivide: %d\n", tc.addExpected, tc.subExpected, tc.mulExpected, tc.divExpected)

		if _, err = w1.Write([]byte(input)); err != nil {
			t.Fatal(err)
		}
		main()

		if n, err = r2.Read(buf); err != nil {
			t.Fatal(err)
		}
		if n < 70 {
			t.Fatal("Error")
		}
		assert.Equal(t, expected, string(buf[70:n]))
	}
}
