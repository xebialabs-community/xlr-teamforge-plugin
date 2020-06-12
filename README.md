## Build Status

[![Build Status][xlr-teamforge-plugin-travis-image]][xlr-teamforge-plugin-travis-url]
[![Codacy](https://api.codacy.com/project/badge/Grade/71d5adb3b2634edc875bd8c73cc3f24b)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-teamforge-plugin&amp;utm_campaign=Badge_Grade)
[![License: MIT][xlr-teamforge-plugin-license-image]][xlr-teamforge-plugin-license-url]
[![Github All Releases][xlr-teamforge-plugin-downloads-image]]()
[![Code Climate][xlr-teamforge-plugin-code-climate-image]][xlr-teamforge-plugin-code-climate-url]

## Preface

This plugin offers an interface from XL Release to Teamforge. 

## Building the plugin

`./gradlew clean build`

## Testing the plugin

Run the following command to run a local docker container with the plugin installed.  

`./gradlew runDockerCompose`

Per the configuration at `src/test/resources/docker/docker-compose.yml,` the ports are defined so you can browse the local instance at:

`http://localhost:35516` 

## Overview

### Features

#### Server Configuration

Add a sever configuration in the XL Release Shared Configuration page for each server or login you wish to manage.

![SharedConfiguration](images/xlr-teamforge-sharedconfiguration.PNG)

Each entry has the following configuration items in its definition:

![SharedConfiguration](images/teamforge-login.PNG)

##### Basics
*   Title - the name by which you will be referring to this definition in your XLR tasks and dashboard tiles.
*   URL - The URL of the Teamforge
*   Authentication Method - None, Basic, Ntlm, PAT

##### Authentication
*   Username
*   Password
*   Domain
*   Enable SSL Verification

##### Proxy
*   Proxy Host
*   Proxy Port
*   Proxy Username
*   Proxy Password

#### Login
Use this task to logon to a Teamforge.

![Login](images/teamforge-login.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Username - Override the default configuration as needed
*   Password - Specify only if you are overriding the default username

##### Output Properties
*   Save the Authorization cookies to a variable for reuse in other tasks.

#### Logout
Use this task to log out of a Teamforge.

![Logout](images/teamforge-logout.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Username - Override the default configuration as needed
*   Password - Specify only if you are overriding the default username

#### CreateDefect
Use this task to create a new defect in Teamforge

![Create Defect](images/teamforge-create-defect.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Domain Name
*   Project Name
*   Defect Name
*   Defect Description
*   Defect Priority
*   Defect Severity
*   Authorization Cookies

##### Output parameters
*   Output - Task output
*   Defect ID - The ID of the newly created defect

#### UpdateDefect
Update an existing Defect with new information

![Update Defect](images/teamforge-update-defect.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Domain Name
*   Project Name
*   Defect Name
*   Defect Description
*   Comment
*   Status
*   Authorization Cookies

##### Output Properties
*   Defect ID - The ID of the newly created defect
*   Output - Task output

#### GetDefect
Retrieve an already existing Defect

![Get Defect](images/teamforge-get-defect.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Domain Name
*   Project Name
*   Defect ID
*   Authorization Cookies

##### Output Properties
*   Output - Task output

#### DeleteDefect

Delete an existing Defect
![DeleteDefect](images/teamforge-delete-defect.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Domain Name
*   Project Name
*   Defect ID
*   Authorization Cookies

##### Output Properties
*   Output - Task output

#### PollQueryForStatus

Poll the server for a change in the named defect

![PollQueryForStatus](images/teamforge-poll-query-for-status.PNG)

##### Input parameters
*   Server - as configured in XL Release
*   Domain Name
*   Project Name
*   Query for finding Records
*   Polling Interval - in seconds
*   Authorization Cookies

### Dashboard

#### QueryTile

[xlr-teamforge-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-teamforge-plugin.svg?branch=master
[xlr-teamforge-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-teamforge-plugin
[xlr-teamforge-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-teamforge-plugin/badges/gpa.svg
[xlr-teamforge-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-teamforge-plugin
[xlr-teamforge-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-teamforge-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-teamforge-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-teamforge-plugin/total.svg
