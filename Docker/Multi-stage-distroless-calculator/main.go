package main

import (
    "flag"
    "fmt"
    "os"
    "strconv"
)

func main() {
    if len(os.Args) < 4 {
        fmt.Println("Usage: calc <add|sub|mul|div> <num1> <num2>")
        os.Exit(1)
    }

    op := os.Args[1]
    a, err := strconv.ParseFloat(os.Args[2], 64)
    if err != nil {
        fmt.Println("invalid first number")
        os.Exit(2)
    }
    b, err := strconv.ParseFloat(os.Args[3], 64)
    if err != nil {
        fmt.Println("invalid second number")
        os.Exit(3)
    }

    switch op {
    case "add":
        fmt.Println(a + b)
    case "sub":
        fmt.Println(a - b)
    case "mul":
        fmt.Println(a * b)
    case "div":
        if b == 0 {
            fmt.Println("division by zero")
            os.Exit(4)
        }
        fmt.Println(a / b)
    default:
        fmt.Println("unknown operation: use add, sub, mul or div")
        os.Exit(5)
    }
}