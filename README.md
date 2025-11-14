# Proligent™ XML Generator for Python

[![GitHub Actions][actions-shield]][actions]

[actions-shield]: https://github.com/averna/proligent-xml-generator-python/actions/workflows/build.yml/badge.svg
[actions]: https://github.com/averna/proligent-xml-generator-python/actions/workflows/build.yml

Python library for creating Proligent™ XML files. These files are used to import
test data in [Proligent™ Cloud][cloud] and [Proligent™ Analytics][analytics]. It
provides a user-friendly, object-oriented wrapper for the [Proligent™
Manufacturing Information Model][model].

[cloud]: https://www.averna.com/en/products/smart-data-management/proligent-cloud
[analytics]: https://www.averna.com/en/products/proligent-analytics
[model]: docs/user/manufacturing-information-model.md

Proligent™ software are designed for Operations Managers, Quality Engineers,
Manufacturing Engineers and Test Engineers. This easy-to-use software solution
monitors test stations and provides valuable insight into your product line.

[launch]: https://www.averna.com/en/products/smart-data-management/launch
[teststand]: https://www.ni.com/teststand

## Installation instructions

<!-- cspell:ignore winget -->

First install a compatible python version. This can be done in the command line
with `winget install Python.Python.3.11`.

To install the package in your (virtual) environment, run the following command:

```cmd
pip install proligent-xml-generator
```

## Getting started

Each layer of the [Proligent™ Manufacturing Information Model][model] is
represented in the package by an equivalent class. Typing hints are used to
indicate what data types are accepted by the objects.

### Example 1

<!-- cspell:ignore LOWERBOUND -->

```python
from proligent.model import DataWareHouse, ExecutionStatusKind, Limit, LimitExpression, Measure, OperationRun, \
    ProcessRun, ProductUnit, SequenceRun, StepRun
import datetime

if __name__ == '__main__':
    limit = Limit(LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND, lower_bound=10, higher_bound=25)
    measure = Measure(value=15, status=ExecutionStatusKind.PASS, limit=limit, time=datetime.datetime.now())
    step = StepRun(name='Step1', status=ExecutionStatusKind.PASS, measure=measure)

    # create sequence run: remember to keep start and end time
    sequence = SequenceRun(
        name='Sequence1',
        station='Station/readme_example',
        status=ExecutionStatusKind.PASS,
        steps=[step],
    )

    # create operation run: remember to keep start and end time
    operation = OperationRun(
        name='Operation1',
        station='Station/readme_example',
        status=ExecutionStatusKind.PASS,
        sequences=[sequence],
    )

    # create process run: remember to keep start and end time
    process = ProcessRun(
        product_unit_identifier='DutSerialNumber',
        product_full_name='Product/readme_example',
        operations=[operation],
        name='Process/readme_example',
        process_mode='PROD',
        status=ExecutionStatusKind.PASS,
    )

    product = ProductUnit(
        product_unit_identifier='DutSerialNumber',
        product_full_name='Product/readme_example',
        manufacturer='Averna'
    )

    warehouse = DataWareHouse(top_process=process, product_unit=product)
    warehouse.save_xml()
```

> [!Note]
> For simplicity this example omits the start and end times, so they default
> to datetime.now. It is highly recommended to set these values with real
> timestamps when used in the real world.

You can also provide the output path for the XML:

```python
from proligent.model import DataWareHouse
warehouse = DataWareHouse()
warehouse.save_xml(destination=r'c:\path_to\Proligent_file_name.xml')
```

### Example 2

This example shows a second way of ordering calls and constructors, from top to
bottom.

```python
from proligent.model import DataWareHouse, ExecutionStatusKind, Limit, LimitExpression, Measure, OperationRun, \
    ProcessRun, ProductUnit, SequenceRun, StepRun
import datetime

if __name__ == '__main__':
    warehouse = DataWareHouse()

    product = warehouse.set_product_unit(ProductUnit(
        product_unit_identifier='DutSerialNumber',
        product_full_name='Product/readme_example',
        manufacturer='Averna'
    ))

    process = warehouse.set_process_run(ProcessRun(
        name='Process/readme_example',
        process_mode='PROD',
        product_unit_identifier='DutSerialNumber',
        product_full_name='Product/readme_example',
    ))

    operation = process.add_operation_run(OperationRun(
        name='Operation1',
        station='Station/readme_example',
    ))

    sequence = operation.add_sequence_run(SequenceRun(
        name='Sequence1',
    ))

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
                        higher_bound=25
                    ),
            )
        )
    )

    sequence.complete(status=ExecutionStatusKind.PASS)

    operation.complete(status=ExecutionStatusKind.PASS)

    process.complete(status=ExecutionStatusKind.PASS)

    warehouse.save_xml()
```

### XML Validation

Generated XML can be validated for safety.

```python
from proligent.xml_validate import validate_xml

# this raises an exception if the XML is invalid
validate_xml(r'c:\path_to\Proligent_file_name.xml')

# this safe call returns the status and meta-data about a failure, if any
is_valid, metadata = validate_xml_safe(r'c:\path_to\Proligent_file_name.xml')
if not is_valid:
    print(metadata.path)
    print(metadata.reason)
```

### Configuration

A few parameters are configurable in the package through the use of the UTIL object.

<!-- cspell:ignore datetimes pytz -->

- `destination_dir`: Specify a different destination directory for the XML
  files, aside from the default `C:\Proligent\IntegrationService\Acquisition`.
- `timezone`: Specify a different timezone for the provided datetimes (default
  is the TZ of the local machine). `pytz` is used for timezone handling. It
  provides `pytz.all_timezones` and `pytz.common_timezones` to list all possible
  timezones. Alternatively, you can look at this list on
  [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

```python
from src.proligent.model import UTIL

if __name__ == '__main__':
    UTIL.destination_dir = r'\\NETWORK_SHARE\Acquisition'
    UTIL.timezone = 'America/New_York'
```

## Trademarks

Proligent is a registered trademark, and Averna is a trademark, of [Averna
Technologies Inc.][web-site]

[web-site]: https://www.averna.com
