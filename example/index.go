package main

import "fmt"
import "test-build/dogs"
import "test-build/people"
// import "test-build/dogs"


func main() {
	fmt.Println( dogs.Snickers() )
	fmt.Println( dogs.Brooklyn() )
	fmt.Println( people.Smith() )
	fmt.Println( people.James() )
}