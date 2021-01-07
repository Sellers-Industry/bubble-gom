#
#   Copyright (C) 2021 Sellers Industry - All Rights Reserved
#   Unauthorized copying of this file, via any medium is strictly
#   prohibited. Proprietary and confidential.
#
#   author: Evan Sellers <sellersew@gmail.com>
#   date: Wed Jan 06 2021
#   file: index.py
#   project: Bubble Gom (Go Manager)
#   purpose: Go manager allows you to build go modules from anywhere
#
#


import argparse
import os
import json
from datetime import datetime
import shutil
import glob


# Config
VERSION = "0.0.1"
GO_PATH = "/Go/src"
LOCKFILE_NAME = "gom-lock"
CONFIG_NAME   = "gom.config"


"""
    Build Lock File Data
    Will create the lockfile data. The lock file will have the gom version
    number, the source directory it is built from, the date it will built on,
    and the first creation time.

    sourceDirectory - the source it's being built from
    firstBuild - string from the past lockfile or False
"""
def buildLockFile( sourceDirectory, firstBuild ):
    lockFileData = {}
    lockFileData[ "source" ]  = sourceDirectory
    lockFileData[ "gomV" ]    = VERSION
    lockFileData[ "build" ]   = str( datetime.now() )
    if firstBuild:                                                              # if has first build
        lockFileData[ "created" ] = firstBuild
    else:
        lockFileData[ "created" ] = lockFileData[ "build" ]
    return lockFileData                                                         # return json dict data


"""
    Add Lock File
    Will add lock file to the vendor directory.

    vendorDirectory - directory to build lockfile in
    lockFileData - data created from buildLockFile()
"""
def addLockFile( vendorDirectory, lockFileData ):
    if os.path.isdir( vendorDirectory ):                                        # valid vendor directory
        filename = os.path.join( vendorDirectory, LOCKFILE_NAME )               # filename for dump
        with open( filename, 'w') as outfile:                                   # open file
            json.dump( lockFileData, outfile )                                  # dump data


"""
    Get Lock File
    Will get the lock file from the vendor directory or return false if there
    is no vendor directory. The data will be parsed into a python dict.

    vendorDirectory - directory to get lockfile from
"""
def getLockFile( vendorDirectory ):
    filename = os.path.join( vendorDirectory, LOCKFILE_NAME )                   # file name if exists
    if os.path.isfile( filename ):                                              # does file exists
        with open( filename ) as lockFile:                                      # open file
            return json.load( lockFile )                                        # return json parsed data
    return False                                                                # if file does not exist


"""
    Add Config Data
    Adds config data to the vendor file. This is just so their is a backup of
    the gom config.

    vendorDirectory - build directory to prepare
    config          - data from the gom.config as dict
"""
def addConfig( vendorDirectory, config ):
    if os.path.isdir( vendorDirectory ):                                        # valid vendor directory
        filename = os.path.join( vendorDirectory, CONFIG_NAME )                 # filename for dump
        with open( filename, 'w') as outfile:                                   # open file
            json.dump( config, outfile )                                        # dump data


"""
    Prepare Vendor Directory
    Will prepare the vendor directory. If the directory does not exist will
    create it. If the directory does will empty it if it contains a lock from
    the same build source. If there is content in the direcotry but no lock file
    then it will fail.

    vendorDirectory - build directory to prepare
    sourceDirectory - where is it being build from
    config          - data from the gom.config as dict
"""
def prepareVenderDirectory( vendorDirectory, sourceDirectory, config ):
    lockFileData = None
    if os.path.isdir( vendorDirectory ):

        # Valid Path
        lockFile = getLockFile( vendorDirectory )
        if not os.listdir( vendorDirectory ):
            lockFileData = buildLockFile( sourceDirectory, False )
            addLockFile( vendorDirectory, buildLockFile( sourceDirectory, False ) )
        elif lockFile and lockFile[ "source" ] == sourceDirectory:
            lockFileData = buildLockFile( sourceDirectory, lockFile[ "created" ] )
        else:
            print( """Error: Unable to get gom-lock for vendor.\nThe
                    directory you are trying to build in does not appear
                    to be the same gom project.\n{}"""
                    .format( vendorDirectory ) )
            exit

        shutil.rmtree( vendorDirectory )
    else:
        lockFileData = buildLockFile( sourceDirectory, False )

    os.mkdir( vendorDirectory )
    addLockFile( vendorDirectory, lockFileData )
    addConfig( vendorDirectory, config )


"""
    Build Package
    Will Build Each Package in the directory required by the config file.
    Will Ensure the path is unuinqe and then build the file and copy all the 
    go files from the build source over.
"""
def buildPackages( vendorDirectory, sourceDirectory, config ):
    if "packages" in config:
        for package in config[ "packages" ]:
            buildPath = os.path.join( vendorDirectory, package[ "name" ] )
            sourcePath = os.path.join( sourceDirectory, package[ "path" ] )
            
            if os.path.isdir( buildPath ):
                print( """Error: Unable to build package {}, as the build 
                        name is not unique."""
                        .format( package[ "name" ] ) )
                continue

            os.mkdir( buildPath )

            if not os.path.isdir( sourcePath ):
                print( """Error: Unable to build package {}, as the source
                        directory, \"{}\" does not exist."""
                        .format( package[ "name" ], sourcePath ) )
                continue

            files = glob.iglob( os.path.join( sourcePath, "*.go" ) )
            for file in files:
                if os.path.isfile( file ):
                    shutil.copy2( file, buildPath )


# Build Config
def build():
    configFile      = os.path.join( os.getcwd(), CONFIG_NAME )
    sourceDirectory = os.path.dirname( configFile )

    with open( configFile ) as data: config = json.load( data )
    vendorDirectory = os.path.join( GO_PATH, config[ "vendor" ] )

    prepareVenderDirectory( vendorDirectory, sourceDirectory, config )
    buildPackages( vendorDirectory, sourceDirectory, config )
    

# Setup
def main(args=None):
    description = "Bubble Gom (v{}) by Sellers Industry".format( VERSION )
    parser = argparse.ArgumentParser( description=description, add_help=False )

    # Version Number
    subparsers = parser.add_subparsers( help="Commands", dest='command' )

    # Commands
    parser_help    = subparsers.add_parser( "help", help="help documents" )
    parser_version = subparsers.add_parser( "version", help="version of Bubble Gom" )
    parser_build   = subparsers.add_parser( "build", help="Build from config file" )
        
    args = parser.parse_args()

    # Run Commands
    if args.command == "help":
        parser.print_help()
    elif args.command == "version":
        print( description )
    elif args.command == "build":
        build()
    else:
        print( "Command unknown try \"gom help\"" )



if __name__ == "__main__":
    sys.exit( main() )