# repo2docker-pangeo

repo2docker plugin to use [PANGEO Stacks](https://github.com/pangeo-data/pangeo-stacks)
as base images.

## Features

`repo2docker-pangeo` supports the following files to configure it.

1. `pangeo-stack`

   This buildpack is triggered if a file with this name exists, and contains
   a docker image name that meets the following criteria:

   a. Is in the `pangeo/` docker organization
   b. Has a tag that is not `latest`

   This ensures that we only support a specific list of base images, and
   can guarantee a good experience for users.

2. `environment.yml`

   A conda environment.yml file that specifies extra packages to be installed.

3. `postBuild`

   A script that can be used to run arbitrary commands after all the other
   build steps are complete.

4. `start`

   A script that is used as the ENTRYPOINT. Can be used to set environment
   variables, modify the arguments passed to the command, etc.

These are the *only* config files that are looked at by the repo2docker-pangeo
build pack. So some other features of repo2docker buildpacks - such as
composition with R or Julia, are unavailable. However, if required, they can
be added later on if PANGEO stack adds a base image with R or Julia present.

All these files can be present in base of the repository, or in `binder/`
directory.

## Usage

1. Install `repo2docker-pangeo`

   ```bash
   pip install repo2docker-pangeo
   ```

2. Create a file called `repo2docker_config.py`, and add the following lines
   to it:

   ```python
   from repo2docker_pangeo import PangeoStackBuildPack

   c.Repo2Docker.buildpacks.insert(0, PangeoStackBuildPack
   ```

3. Run `repo2docker` on your repository of choice, with the following command:

   ```bash
   repo2docker --config repo2docker_config.py <repository-url-or-path>
   ```

This should build the repository with the appropriate pangeo-stack,
and start a notebook.

## Testing

This repository has a `binder/` directory that is set up to trigger the
PangeoStackBuildPack. You can test it with:

```
repo2docker --config repo2docker_config.py https://github.com/yuvipanda/repo2docker-pangeo
```
