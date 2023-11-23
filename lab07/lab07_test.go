package main

import (
	"bytes"
	"github.com/stretchr/testify/assert"
	"io"
	"net/http"
	"testing"
	"time"
)

func TestRest(t *testing.T) {
	testData := []struct {
		path     string
		method   string
		body     string
		status   int
		expected string
	}{
		{"/bookshelf", http.MethodGet, "", 200, `[{"id":1,"name":"Blue Bird","pages":500}]`},
		{"/bookshelf/1", http.MethodGet, "", 200, `{"id":1,"name":"Blue Bird","pages":500}`},
		{"/bookshelf/2", http.MethodGet, "", 404, `{"message":"book not found"}`},
		{"/bookshelf", http.MethodPost, `{"name":"Blue Bird","pages":500}`, 409, `{"message":"duplicate book name"}`},
		{"/bookshelf", http.MethodPost, `{"name":"Red Bird","pages":500}`, 201, `{"id":2,"name":"Red Bird","pages":500}`},
		{"/bookshelf", http.MethodGet, "", 200, `[{"id":1,"name":"Blue Bird","pages":500},{"id":2,"name":"Red Bird","pages":500}]`},
		{"/bookshelf/2", http.MethodGet, "", 200, `{"id":2,"name":"Red Bird","pages":500}`},
		{"/bookshelf/2", http.MethodPut, `{"name":"Yellow Bird","pages":500}`, 200, `{"id":2,"name":"Yellow Bird","pages":500}`},
		{"/bookshelf/2", http.MethodGet, "", 200, `{"id":2,"name":"Yellow Bird","pages":500}`},
		{"/bookshelf/2", http.MethodPut, `{"name":"Blue Bird","pages":500}`, 409, `{"message":"duplicate book name"}`},
		{"/bookshelf/300", http.MethodPut, `{"name":"Real life","pages":500}`, 404, `{"message":"book not found"}`},
		{"/bookshelf/2", http.MethodDelete, "", 204, ``},
		{"/bookshelf/800", http.MethodDelete, "", 204, ``},
		{"/bookshelf/2", http.MethodGet, "", 404, `{"message":"book not found"}`},
		{"/bookshelf", http.MethodGet, "", 200, `[{"id":1,"name":"Blue Bird","pages":500}]`},
		{"/bookshelf", http.MethodPost, `{"name":"Les Misérables","pages":500}`, 201, `{"id":3,"name":"Les Misérables","pages":500}`},
		{"/bookshelf", http.MethodGet, "", 200, `[{"id":1,"name":"Blue Bird","pages":500},{"id":3,"name":"Les Misérables","pages":500}]`},
		{"/bookshelf/3", http.MethodGet, "", 200, `{"id":3,"name":"Les Misérables","pages":500}`},
		{"/bookshelf/3", http.MethodPut, `{"name":"Red Bird","pages":1000}`, 200, `{"id":3,"name":"Red Bird","pages":1000}`},
		{"/bookshelf/3", http.MethodGet, "", 200, `{"id":3,"name":"Red Bird","pages":1000}`},
		{"/bookshelf/3", http.MethodDelete, "", 204, ``},
		{"/bookshelf/2", http.MethodDelete, "", 204, ``},
		{"/bookshelf/1", http.MethodDelete, "", 204, ``},
		{"/bookshelf", http.MethodGet, "", 200, `[]`},
	}

	go func() {
		main()
	}()

	isUp := false
	for i := 0; i < 30; i++ {
		_, err := http.Get("http://localhost:8087")
		if err == nil {
			isUp = true
			break
		}
		t.Logf("Server not up yet... try again")
		time.Sleep(2 * time.Second)
	}
	if !isUp {
		t.Fatal("Unable to connect to server")
		return
	}

	for _, tc := range testData {
		bodyVal := tc.body
		if bodyVal == "" {
			bodyVal = "nil"
		}
		t.Logf("Sending request... Path: \"%s\"\tMethod: %s\tBody: %s", tc.path, tc.method, bodyVal)

		req, err := http.NewRequest(tc.method, "http://localhost:8087"+tc.path, bytes.NewReader([]byte(tc.body)))
		if err != nil {
			t.Fatal(err)
			return
		}
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			t.Fatal(err)
			return
		}

		if !assert.Equal(t, tc.status, resp.StatusCode) {
			return
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			t.Fatal(err)
			return
		}
		if !assert.Equal(t, tc.expected, string(body)) {
			return
		}

		err = resp.Body.Close()
		if err != nil {
			t.Fatal(err)
			return
		}
	}
}
