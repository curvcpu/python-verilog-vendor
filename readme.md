# `python-verilog-vendor`

Collection of simple python functions and classes related to build/test/codegen for Verilog and SystemVerilog projects that are vendored into other python packages.

## Usage

This repo was set up for code in `src/utils` to be vendored other repos like this:

```sh
# in this repo, when changes on main are ready for other repos to vendor
git checkout main
git pull --ff-only   # if changes aren't on your local main yet
git subtree split --prefix=src/utils -b dist-utils # (re)creates/advances the split branch
git push -f origin dist-utils # force is fine; this branch is derived
```

However, it is not necessary to do this manually. A [GitHub Actions workflow](.github/workflows/update-dist-utils.yml) is set up to do the above automatically on every push to `main`.

In the other repo that will vendor this updated code, in order to copy the contents of `src/utils` into `src/PACKAGE_NAME/_vendor/utils` do this:

```sh
# once, in outer repo:
git remote add utils git@github.com:mikegoelzer/python-verilog-vendor.git
git subtree add --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils --squash
```

For the next round of changes:

```sh
# in outer repo, on main
git fetch utils
git subtree pull --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils --squash
```

To push changes from the outer repo back into this repo:

```sh
# in outer repo:
git subtree push --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils
# then, in this repo, open a PR from dist-utils → main
```

## Tests

Run tests with:

```sh
make test
```
