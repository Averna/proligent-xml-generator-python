# proligent-xml-generator-python

[![License][license-badge]][eula]

Python library for creating Proligent™ XML files.

[license-badge]: https://img.shields.io/badge/License-BSD%203--Clause-Clause
[eula]: LICENSE

This package implements a XML file generator for import in Proligent Quickview or Analytics in Python.
It provides a user-friendly, object-oriented wrapper for the Proligent data model.

## Installation instructions

First install a compatible python version. This can be done in the command line with `winget install Python.Python.3.11`.

To install the package in your (virtual) environment, run the following command:

```cmd
pip install git+https://github.com/Averna/proligent-xml-generator-python
```

Or, include it in your `requirements.txt` file as follows:

```cmd
proligent @ git+https://github.com/Averna/proligent-xml-generator-python
```

## Getting started

Each layer of the Proligent data model is represented in the package by an equivalent class. Typing hints are used to indicate what data types are accepted by the objects.

More information about the Proligent data model can be found [here](https://resultprocessor.proligent.com/reference/dataware-house-schema.html).

### Example 1

```python
from proligent.datawarehouse.datawarehouse_model import ExecutionStatusKind
from proligent.model import DataWareHouse, Limit, LimitExpression, Measure, OperationRun, \ 
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

Note: for simplicity this example omits the start and end times, so they default to datetime.now. It is highly 
recommended to set these values with real timestamps when used in the real world.

You can also provide the output path for the XML:

```python
from proligent.model import DataWareHouse
warehouse = DataWareHouse()
warehouse.save_xml(destination=r'c:\path_to\Proligent_file_name.xml')
```

### Example 2

This example shows a second way of ordering calls and constructors, from top to bottom.

```python
from proligent.datawarehouse.datawarehouse_model import ExecutionStatusKind
from proligent.model import DataWareHouse, Limit, LimitExpression, Measure, OperationRun, \ 
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
validate_xml(r'c:\path_to\Proligent_file_name.xml')
```

### Configuration

A few parameters are configurable in the package through the use of the UTIL object.

- `destination_dir`: Specify a different destination directory for the XML files, aside from the default `C:\Proligent\IntegrationService\Acquisition`.
- `timezone`: Specify a different timezone for the provided datetimes (default is the TZ of the local machine). `pytz` is used for timezone handling. It provides `pytz.all_timezones` and `pytz.common_timezones` to list all possible timezones. Alternatively, you can look at this list on [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

```python
from src.proligent.model import UTIL

if __name__ == '__main__':
    UTIL.destination_dir = r'\\NETWORK_SHARE\Acquisition'
    UTIL.timezone = 'America/New_York'
```

## Requirements

- Python 3.11

## License

This library is covered by the [BSD 3-Clause License Agreement][eula].

> [!IMPORTANT]
> Don't forget to distribute the `LICENSE.md` file in the root directory of this repo along with
> the library files on the customer machine.

## Developer guide

Clone this repository locally: [Instructions](https://github.com/averna-reuse/.github-private/blob/main/profile/getting-started/repo-cloning.md).

It is recommended to create a virtual environment. If you have the project open in Visual Studio Code, this can be done easily by opening the command palette (CTRL-SHIFT-P) and searching for _Python: Create Environment..._. This action is only available if you have installed the python extension in VSCode.

Finally, the required packages need to be installed in the virtual environment. Open a terminal in Visual Studio Code and execute `pip install -r requirements.txt` (VSCode activates the virtual environment automatically).
