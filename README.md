# Proligent™ XML Generator for Python™

[![Build][actions-shield]][actions]
[![Python Package Index][pypi-version]][pypi-page]
[![Python Versions][python-versions]][pypi-page]

[actions-shield]: https://github.com/averna/proligent-xml-generator-python/actions/workflows/build.yml/badge.svg
[actions]: https://github.com/averna/proligent-xml-generator-python/actions/workflows/build.yml
[pypi-version]: https://img.shields.io/pypi/v/proligent-xml-generator.svg
[pypi-page]: https://pypi.org/project/proligent-xml-generator
[python-versions]: https://img.shields.io/pypi/pyversions/proligent-xml-generator.svg

Python™ library for generating Proligent™ XML files. It provides a simple,
structured API for building valid import files, reducing manual XML writing and
ensuring consistent data formatting. These files are used to import data into
[Proligent™ Cloud][cloud] and [Proligent™ Analytics][analytics].

[cloud]: https://www.averna.com/en/products/smart-data-management/proligent-cloud
[analytics]: https://www.averna.com/en/products/proligent-analytics

> **Tip:** Refer to the [Proligent™ Manufacturing Information Model][model] to
> learn how to structure and map your data in Proligent™.

[model]: https://github.com/Averna/proligent-xml-generator-python/blob/main/docs/user/manufacturing-information-model.md

Proligent™ software are designed for Operations Managers, Quality Engineers,
Manufacturing Engineers and Test Engineers. This easy-to-use software solution
monitors test stations and provides valuable insight into your product line.

## Installation instructions

First, install a compatible python version from [Python.org][python].

[python]: https://www.python.org/downloads

Then, to install the package in your (virtual) environment, run the following
command:

```cmd
pip install proligent-xml-generator
```

## Getting started

Each layer of the [Proligent™ Manufacturing Information Model][model] is
represented in the package by an equivalent class. Typing hints are used to
indicate what data types are accepted by the objects.

### Example 1

```python
from proligent.model import (
    DataWareHouse,
    ExecutionStatusKind,
    Limit,
    LimitExpression,
    Measure,
    OperationRun,
    ProcessRun,
    ProductUnit,
    SequenceRun,
    StepRun,
)
import datetime

if __name__ == "__main__":
    limit = Limit(
        LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
        lower_bound=10,
        higher_bound=25,
    )
    measure = Measure(
        value=15,
        status=ExecutionStatusKind.PASS,
        limit=limit,
        time=datetime.datetime.now(),
    )
    step = StepRun(
        name="Step1",
        status=ExecutionStatusKind.PASS,
        measure=measure
    )

    # Create sequence run: remember to keep track of start and end time

    sequence = SequenceRun(
        name="Sequence1",
        status=ExecutionStatusKind.PASS,
        steps=[step],
    )

    # Create operation run: remember to keep track of start and end time

    operation = OperationRun(
        name="Operation1",
        station="Station/readme_example",
        status=ExecutionStatusKind.PASS,
        sequences=[sequence],
    )

    # Create process run: remember to keep track of start and end time

    process = ProcessRun(
        product_unit_identifier="DutSerialNumber",
        product_full_name="Product/readme_example",
        operations=[operation],
        name="Process/readme_example",
        process_mode="PROD",
        status=ExecutionStatusKind.PASS,
    )

    product = ProductUnit(
        product_unit_identifier="DutSerialNumber",
        product_full_name="Product/readme_example",
        manufacturer="Averna",
    )

    warehouse = DataWareHouse(top_process=process, product_unit=product)
    warehouse.save_xml()
```

> **Note:** For simplicity this example omits the start and end times, so they
> default to datetime.now. It is highly recommended to set these values with
> real timestamps when used in the real world.

You can also provide the output path for the XML:

```python
from proligent.model import DataWareHouse
warehouse = DataWareHouse()
warehouse.save_xml(destination=r'C:\path_to\Proligent_file_name.xml')
```

### Example 2

This example shows a second way of ordering calls and constructors, from top to
bottom.

```python
from proligent.model import (
    DataWareHouse,
    ExecutionStatusKind,
    Limit,
    LimitExpression,
    Measure,
    OperationRun,
    ProcessRun,
    ProductUnit,
    SequenceRun,
    StepRun,
)
import datetime

if __name__ == "__main__":
    warehouse = DataWareHouse()

    product = warehouse.set_product_unit(
        ProductUnit(
            product_unit_identifier="UutSerialNumber",
            product_full_name="Product/readme_example",
            manufacturer="Averna",
        )
    )

    process = warehouse.set_process_run(
        ProcessRun(
            name="Process/readme_example",
            process_mode="PROD",
            product_unit_identifier="DutSerialNumber",
            product_full_name="Product/readme_example",
        )
    )

    operation = process.add_operation_run(
        OperationRun(
            name="Operation1",
            station="Station/readme_example",
        )
    )

    sequence = operation.add_sequence_run(
        SequenceRun(
            name="Sequence1",
        )
    )

    sequence.add_step_run(
        StepRun(
            name="Step1",
            status=ExecutionStatusKind.PASS,
            measure=Measure(
                value=15,
                time=datetime.datetime.now(),
                status=ExecutionStatusKind.PASS,
                limit=Limit(
                    LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                    lower_bound=10,
                    higher_bound=25,
                ),
            ),
        )
    )

    sequence.complete(status=ExecutionStatusKind.PASS)
    operation.complete(status=ExecutionStatusKind.PASS)
    process.complete(status=ExecutionStatusKind.PASS)
    warehouse.save_xml()
```

### About Names

Most of the "names" (product, station, etc.) in the model can be simple strings,
or can be built in hierarchies.

The goal is to allow grouping of items in meaningful categories, which can be
useful when selecting items for display or
reporting.

Note that the last item in the full name (the "leaf" of the tree) must be
meaningful: some reports display only the leaf, for simplicity and brevity. In
most cases the full names is also available, but may be less visible (tooltips).

#### Example: Stations

`Country/ManufacturerName/ProductionLine/StationName`

Other items in the full station names could be: city, station type, etc.

For stations that can test multiple units in parallel: see `test_position_name`.

#### Example: Products

`ProductFamily/ProductName/PartNumber`

We don't recommend having a version or revision as the leaf of the full product
name. This is best recorded as a characteristic, either on the product unit or
the operation.

### Sequence "Tree"

All sequences are added to the operation. However, typically sequences are
organized in "trees".

```text
MainSequence1
    SubSequence1
        SubSubSeq1
        SubSubSeq2
    SubSequence2
MainSequence2
    etc.
```

To keep the sequences organized in trees like the example above, the sequences
names need to include all nodes of the tree, separated by "/".

```python
    sequence = operation.add_sequence_run(SequenceRun(name="MainSequence1/SubSequence1/SubSubSeq1"))
    sequence = operation.add_sequence_run(SequenceRun(name="MainSequence1/SubSequence1/SubSubSeq2"))
    sequence = operation.add_sequence_run(SequenceRun(name="MainSequence1/SubSequence2"))
    sequence = operation.add_sequence_run(SequenceRun(name="MainSequence2"))
    # etc.
```

It is not necessary to create all nodes (e.g. `MainSequence1` and
`MainSequence1/SubSequence1`). However, they can also be created if they need to
old steps, characteristics or documents.

Also note that the full sequence name is limited to 2000 characters, and each
part to 64 characters.

### Process Run ID

By default, the ProcessRunID is automatically generated as a deterministic ID
based on the `product_full_name`, `product_unit_identifier`, `process_mode`, and
a configurable fixed process start time (default: "2000-01-01").

This ensures that multiple operation runs within the same process refer to the
same process run, which is critical for accurate reporting in Proligent.

If you need a fixed ID regardless of field values, you can optionally set the
`id` parameter directly when constructing the `ProcessRun`.

### File Names

The XML files must have the prefix "Proligent_".

The documents attached must have the prefix "Document_".

In case of compressed documents, "CompressedDocument_".

### XML Validation

Generated XML can be validated for safety.

```python
from proligent.xml_validate import validate_xml

# This raises an exception if the XML is invalid

validate_xml(r"C:\path_to\Proligent_file_name.xml")

# This safe call returns the status and meta-data about a failure, if any

is_valid, metadata = validate_xml_safe(r"C:\path_to\Proligent_file_name.xml")

if not is_valid:
    print(metadata.path)
    print(metadata.reason)
```

### Configuration

A few parameters are configurable in the package through the use of the UTIL
object.

`UTIL` and `Util` now live in `proligent.util`.
Backward compatibility is kept, so importing these symbols from `proligent.model`
still works.

<!-- cspell:ignore datetimes pytz -->

- `destination_dir`: Specify a different destination directory for the XML
  files, aside from the default `C:\Proligent\IntegrationService\Acquisition`.
- `timezone`: Specify a different timezone for the provided datetimes (default
  is the TZ of the local machine). `pytz` is used for timezone handling. It
  provides `pytz.all_timezones` and `pytz.common_timezones` to list all possible
  timezones. Alternatively, you can look at this list on
  [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

```python
from proligent.util import UTIL

if __name__ == '__main__':
    UTIL.destination_dir = r'\\NETWORK_SHARE\Acquisition'
    UTIL.timezone = 'America/New_York'
```

## Trademarks

Proligent is a registered trademark, and Averna is a trademark, of [Averna
Technologies Inc.][web-site]

[web-site]: https://www.averna.com

Python is a trademark of the [Python Software Foundation][python-foundation].

[python-foundation]: https://www.python.org/psf

Other product and company names mentioned herein are trademarks or trade names
of their respective companies.
