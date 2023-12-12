from invoke.context import Context
from invoke.tasks import task


@task
def build(c: Context) -> None:
    """
    Build neovim
    """
    # First we want to build neovim.
    c.run("make CMAKE_BUILD_TYPE=RelWithDebInfo")


@task(pre=[build])
def update_deps(c: Context) -> None:
    """
    Update the vendored dependencies by re-downloading them and building neovim.
    """
    # Create a vendor directory to contain all of the dependency artifacts.
    c.run("mkdir -p vendor")

    # Copy the dependencies to the new vendor directory.
    c.run("cp -fr .deps/build/downloads/* vendor/")


@task(post=[build])
def vendor_build(c: Context) -> None:
    """
    First unpack the vendored dependencies and then build neovim.
    """
    # Create the dependencies download directory.
    c.run("mkdir -p .deps/build/downloads")

    # Copy the dependencies to the new vendor directory.
    c.run("cp -fr vendor/* .deps/build/downloads/")
