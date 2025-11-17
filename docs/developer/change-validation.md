# Change Validation Guide

This short guide explains how to validate your changes before publishing a new
version of `proligent-xml-generator`, and how to consume both local and released
packages from another project.

## Prerequisites

- Use Python 3.11 thru 3.13.
- Create and activate a virtual environment.
- Install the project dependencies:

  ```powershell
  pip install -r requirements.txt
  ```

## Run Unit Tests

All tests live under `test/` and use `pytest`.

```powershell
python -m pytest
```

The command exits with status code `0` when every test passes. Resolve failures
before moving to packaging.

## Build a Local Package

We use `setuptools` with a `pyproject.toml`, so `python -m build` produces both
a source distribution (`.tar.gz`) and a wheel (`.whl`).

```powershell
python -m pip install --upgrade build
python -m build --outdir dist
```

The artifacts are written to `dist/`.

## Use the Local Package in Another Project

Suggestion: use `proligent-xml-generator-python-demo` from averna-reuse.

`https://github.com/averna-reuse/proligent-xml-generator-python-demo`

From the other project, install the freshly built wheel:

```powershell
$version = '1.0.0' # change this
$pathToPackage = "..\proligent-xml-generator-python\dist\proligent_xml_generator-$version-py3-none-any.whl"
pip install --force-reinstall $pathToPackage
```

This allows you to validate integration scenarios before publishing an official
release.

## Increment Library Version

> [!IMPORTANT]
> Remember to update the library version in `pyproject.toml`.

## Publish And Consume From TestPypi (OPTIONAL)

If you feel the need to publish to the TestPypi before publishing to the real
Pypi...

From *your PR branch* use the github `Publish` workflow to deploy to the TestPypi
package manager.

> [!IMPORTANT]
> If you install the pre-release from TestPyPI, add the main PyPI index as a
> fallback so dependencies such as `pytz` resolve correctly:
>
> ```cmd
> pip install \
>     --index-url https://test.pypi.org/simple/ \
>     --extra-index-url https://pypi.org/simple \
>     proligent-xml-generator
> ```

## Publish And Consume The Released Package From Pypi

Use the github `Publish` workflow to deploy to Pypi package manager.

> [!IMPORTANT]
> Merge first into main, and then publish to Pypi. \
> Publishing should NEVER be done from a dev or PR branch.

Once the release is live, downstream projects can simply rely on the official
package:

```cmd
pip install --upgrade proligent-xml-generator
```

Pin a version if you need a specific release:

```cmd
pip install proligent-xml-generator
```

## Validate XMLs Can be Integrated In Proligent

You can ask the Proligent team to validate that your generated XMLs can be
integrated in Proligent Analytics or Proligent Cloud.

> [!NOTE]
> Even valid XMLs can be rejected. There are some validation that can't be done
> in a XSD. Please make sure the DIT (Data Integration Toolkit) can process
> your generated XMLs.
