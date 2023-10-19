package main

import (
	"github.com/stretchr/testify/assert"
	"net/http/httptest"
	"testing"
)

func TestCalculator(t *testing.T) {
	testData := []struct {
		path     string
		expected string
	}{
		{"/add/1/2", "1 + 2 = 3"},
		{"/add", "Error!"},
		{"/sub/7/2", "7 - 2 = 5"},
		{"/sub/7/2/3", "Error!"},
		{"/mul/3/4", "3 * 4 = 12"},
		{"/mul/3", "Error!"},
		{"/div/10/3", "10 / 3 = 3, reminder = 1"},
		{"/div/10/0", "Error!"},
		{"/div/10/3/4", "Error!"},
		{"/div/10/a", "Error!"},
		{"/div/a/3", "Error!"},
		{"/gcd/10/3", "Error!"},
		{"/gcd/10/3/4", "Error!"},
		{"/favicon.ico", "Error!"},
		{"/", "Error!"},
	}

	for _, tc := range testData {
		w := httptest.NewRecorder()
		r := httptest.NewRequest("GET", tc.path, nil)

		Calculator(w, r)

		assert.Equal(t, tc.expected, w.Body.String())
	}
}
