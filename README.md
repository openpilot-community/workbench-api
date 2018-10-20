# Workbench API

This is a small little Python daemon that runs on EON while someone is connected to the EON via Workbench App.  
It used to be included in Workbench but decided it should exist separately as it makes more sense for maintaining the type of code found in it.

A seasoned Python dev could easily assist with this without having to worry about the funky deployments of the Workbench desktop repository.

### Help Support Openpilot Community Efforts

The Openpilot Community or jfrux are funded by Comma.ai, Inc. or any other commercial entity.
Your support is all we have.  Growing expenses with opc.ai, cloud hosting, and costs running great services for the community is not free.
If you have a few bucks, please consider [becoming a patreon](https://patreon.com/openpilotcommunity) for the Openpilot Community and support further uptime and dev time.  Finances will be out in the open on the patreon page for everyone to see.

https://patreon.com/openpilotcommunity

## Contributing

First off, I'm not a Python developer so this is probably somehow a sin amongst Python itself so help me clean it up if you feel so inclined.  Keep in mind that this runs on a Read-only file system... so we need to get it so that we can install dependencies and things in a local environment somehow that isn't in the base system path.

PLEASE: I urge you to take a look at the Todos below and please reach out and fork / submit PRs and help us clean this all up. Its wildly helpful.

## Todos / Issues

- [ ] Find out how to install dependencies with pip locally without using system directories since of "Read-only file system" issues on EON devices.
- [ ] Cleanup `monitor.py` and divide it into a library so that methods aren't all spaghetti'd in one file.
- [ ] Create little mock files that can emulate feeds we're receiving from OP so we can develop on other platforms and deploy to EON safely.
- [ ] Now that its in its own repo, we want Workbench to send command to download an updated self-executing shell script from Git that installs and updates these services regularly.
- [ ] A method to keep Workbench looking at the right version of the API that goes with the client.
  - How should Workbench keep its api codebase in sync with the version installed?
  - Should we just ensure that the API version follows the desktop?
- [ ] It should probably terminate when Workbench is not connected to EON.

## What it does currently

- [x] Workbench downloads install.sh and executes it on EON.
- [x] It then starts a service that runs on EON which hosts a websocket service for the client to interact with.
- [x] It listens to all the ZMQ messages on EON and transmits a lot of them over the websocket in real-time to the client.

## Deprecated

- [x] It is automatically zipped when built with Workbench App.
- [x] The zip file is transferred to EON up connecting.
- [x] The file is unzipped on EON to `/data/workbench`.

## License
MIT of course.