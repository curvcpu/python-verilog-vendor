# `python-verilog-vendor`

Collection of simple python functions and classes related to build/test/codegen for Verilog and SystemVerilog projects that are vendored into other python packages.

## Usage

Everything is automated and scripted.  No manual steps are required.  

  - Each push to `main` from this repo triggers a GitHub Actions workflow that updates the `dist-utils` branch of this repo.
  - The consumer repo has a Makefile rule in `tools/curvcfg/Makefile` that fetches the latest `dist-utils`:

    ```sh
    # in the other repo that will vendor in this repo
    make vendor
    ```

  - Changes made in the other repo can be merged into this repo's main via a PR:

    - Step 1: In the other repo, push the changes to this repo's `dist-utils` branch:

      ```sh
      # in the consumer repo
      git subtree push --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils
      ```

    - Step 2: In this repo, open a PR from `dist-utils` → `main`

## Manual Methods

This repo was set up for code in `src/utils` to be vendored other repos in the following manner:

  - Commit your changes to `main`, or stash them.

  - In your local checkout of this repo, we will make the latest commits available for others to vendor.  First, make sure your local is up to date:
    ```sh
    # in this repo
    # (just to make sure you're up to date...)
    git checkout main    
    git pull --ff-only
    ```

  - Now, recreate the split branch and force pursh it to `dist-utils` branch on the outer repo:

    ```sh
    # in this repo's directory
    git subtree split --prefix=src/utils -b dist-utils # (re)creates/advances the split branch
    git push -f origin dist-utils # force is fine; this branch is derived
    ```

However, it is not necessary to do this manually. A [GitHub Actions workflow](.github/workflows/update-dist-utils.yml) is set up to do the above automatically on every push to `main`.  

Here are the steps to manually update the `dist-utils` branch in the other repo (the one that will vendor in this repo):

In the repo that will vendor this updated code, in order to copy the contents of `src/utils` into `src/PACKAGE_NAME/_vendor/utils` do this **only once** (first time you vendor this repo):

```sh
# once, in the other repo that will vendor in this repo
git remote add utils git@github.com:mikegoelzer/python-verilog-vendor.git
git subtree add --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils --squash
```

For the next round of changes:

```sh
# in the other repo that will vendor in this repo, on branch main
git fetch utils
git subtree pull --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils --squash
```

To push changes from the other repo (e.g., `curvcfg`) back into this repo:

```sh
# in other curvcfg repo:
git subtree push --prefix=src/PACKAGE_NAME/_vendor/utils utils dist-utils
# then, in this repo, open a PR from dist-utils → main
```

## Tests

Run tests with:

```sh
make test
```
