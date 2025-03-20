package main

import (
    "fmt"
    // "io"
    "net/http"
    "os"
    "resty.dev/v3"
)

func main() {

    // resp, err :=
    http.Get(os.Args[1])
    
    client := resty.New()
    defer client.Close()

    res, err := client.R().
        EnableTrace().
        Get(os.Args[1])
    fmt.Println(err, res)
    fmt.Println(res.Request.TraceInfo())
}
