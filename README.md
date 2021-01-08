# Bubble Gom (Go Build Manager)
Bubble Gom by Sellers Industry is a Go Build Manager that allows you to build Go Projects outside your go folder. It then allows you to import other Go files inside your local project directory. This command line script allows you to create a gom build config and it will be built on request.

Quick Note: This project was created to help with the development of Go Projects. It is an early prototype and if people like it, we will continue to develop Bubble Gom further. If you are using Bubble Gom and like it, give a star on GitHub, so we know we should keep developing this project.

<br>

**What is Bubble Gom?**<br>
Bubble Gom is a simple package manager for Go your projects.

**Why use Bubble Gom?**<br>
Bubble Gom allows you to have Go Projects outside the Go Path directory.

**What does Bubble Gom actually do?**<br>
Gom config files store project path directories and copies all Go files over to a package directory in your Go Path Directory. Bubble Gom is super simple, but is designed to stream line your Go Project.

**Will my code break if I stop using Bubble Gom?**<br>
No, your code will not break. Bubble Gom does not alter any of your code. all you would have to do is move your project into your go directory, and in the worst case changes the import path for local files. 

**How do I get Started?**<br>
All you need to do is install Bubble Gom using a python script, build your config file and tell gom to run a build.

**Why is it called Bubble Gom?**<br>
It is called bubble because your packages float up into your Go Path, and Gom as in Go Manager.

<br>
<br>

## Installing

<br>
<br>

## Config File
The Bubble Gom config file `gom.config` should be located in the root of your project you will then have package folders with Go file packages in them.

<br>

### Project Name `{ String } name` *optional*
The name of the project. This has not technical purpose but helps you identify the project.

<br>

### Vendor Name `{ String } vendor` *required*
The vendor name is the technical name for the project and is used for organization by Bubble Gom. The vendor name is also the path your project will be built in. Bubble Gom will tell you if this path is not available. When this path is created a `gom-lock` is placed their to ensure only this specific project is built in that directory.

<br>

### Package List `{ object[] } packages` *required*
The package list is an array of packages that will be built by Bubble Gom. There are two properties, `name` and `path`. The name should be the same name of the package on the Go Files you are importing. The path is the local directory to be copied. For example, all the Go giles from the local path are copied into the Go Directory in the vendor directory and sub-directory of the name.


<br>
<br>

## Commands
The Bubble Gom commands will help you build a Bubble Gom project.

<br>

### Help Documents `gom help`
Returns help documentation about commands in Bubble Gom

<br>

### Version `gom version`
Prints the current version of Bubble Gom you are using

<br>

### Build Config `gom build`
Will build all your packages based on your `gom.config` file. You much run in the directory your config file is located. This command must be ran every time you update any code in packages.

<br>
<br>

## Example Builds
In this example the vendor is `example` so that means this will be build in `/Go/src/example/`. The Go files in `packages/packOne` will be places in `/Go/src/example/packOne` and the Go files in `packages/packTwo` will be places in `/Go/src/example/packTwo`. The directories architecture is below. Everytime a new build is made a `gom-lock` file is created in the vendor directory, Bubble Gom will not remove any files and generate a new build if this lock file is not present.
```json
.
├── packages
│   ├── packOne
│   │   ├── file1.go
│   │   └── file2.go
│   └── packTwo
│       ├── file1.go
│       └── file2.go
├── gom.cofig
└── main.go
```

**gom.config**
```JSON
{
    "name": "Example",
    "vendor": "example",
    "packages": [
        {
            "name": "packOne",
            "path": "packages/packOne"
        },
        {
            "name": "packTwo",
            "path": "packages/packTwo"
        }
    ]
}
```

**main.go**
```go
package main

import "example/packOne"

func main() {
    packOne.test()
}
```

<br>
<br>

## Notes & Hints
- Must run `gom build` everytime you change any code in packages that Bubble Gom Generates
- Any funtion your would like to be export properly from your package must start with an uppercase letter.

<br>
<br>


## Fixme
- Add way to make package with having a sub package directory
- add override flag for build to force build

<br>

## Building New Version
When building a new version make sure to update the version number in `__main__.py` and in `setup.py`.