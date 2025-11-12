from proligent_processor import ProligentProcessor
from datawarehouse.datawarehouse_model import ExecutionStatusKind
import datetime

# Create the data warehouse
data_warehouse = ProligentProcessor()


# Set the Product data
product_unit_identifier = "00001"  # = Serial Number
product_full_name = "TestBEEN"
start_time = datetime.datetime.now()
end_time = datetime.datetime.now() + datetime.timedelta(seconds=45)

# Create the top process run
top_process_run = data_warehouse.create_process_run()
# Update the top process run properties
data_warehouse.update_process_run_properties(
    top_process_run,
    name="Process1",
    product_unit_identifier=product_unit_identifier,
    product_full_name=product_full_name,
    start_time=start_time,
    end_time=end_time,
)
# Add the top process run to the data warehouse
data_warehouse.append_top_process_run_to_dataset(top_process_run)

# Create a operation run
operation_run = data_warehouse.create_operation_run()
# Update the operation run properties
data_warehouse.update_operation_run_properties(
    operation_run,
    name="Operation1",
    start_time=start_time,
    end_time=end_time,
)
# Append the operation run to the top process run
data_warehouse.append_operation_run_to_process_run(top_process_run, operation_run)

# Create a sequence run
sequence_run = data_warehouse.create_sequence_run()
# Update the sequence run properties
data_warehouse.update_sequence_run_properties(sequence_run, name="Sequence1")
# Append the sequence run to the operation run
data_warehouse.append_sequence_run_to_operation_run(operation_run, sequence_run)

# Create a step run
step_1 = data_warehouse.create_step_run()
# Update the step run properties
data_warehouse.update_step_run_properties(step_1, name="Step1")
# Append the step run to the sequence run
data_warehouse.append_step_run_to_sequence_run(sequence_run, step_1)


# Create a first measurement
measurement_1 = data_warehouse.create_measure()
# Update the measurement properties
data_warehouse.update_measure_properties(measurement_1)
# Append the measurement to the first step run
data_warehouse.append_measure_to_step_run(step_1, measurement_1)
# Create a value for the measurement
value_1 = data_warehouse.create_real_value(value="2.38")
# Append the value to the measurement 1
data_warehouse.update_value_in_measure(measurement_1, value_1)
# Create a limit for the measurement
limit = data_warehouse.create_limit(lower_bound="0", higher_bound="10", limit_expression=data_warehouse.LimitExpression.LOWERBOUND_LEQ_X_LEQ_HIGHER_BOUND)
# update the limit in the measurement
data_warehouse.update_limit_in_measure(measurement_1, limit)

# Create the Product Unit
product_unit = data_warehouse.create_product_unit()
# Update the product unit properties
data_warehouse.update_product_unit_properties(
    product_unit, product_unit_identifier, product_full_name
)
# Append the product unit to the data warehouse
data_warehouse.append_product_unit_to_dataset(product_unit)


# Print the data warehouse
print("Data warehouse: ")
print(data_warehouse.dataset)
print("")
print("Measurement 1: ")
print(
    data_warehouse.dataset.top_process_run[0]
    .operation_run[0]
    .sequence_run[0]
    .step_run[0]
    .step_name
)
print(
    data_warehouse.dataset.top_process_run[0]
    .operation_run[0]
    .sequence_run[0]
    .step_run[0]
    .measure[0]
)


print("")
print("xml string: ")
data_warehouse.save_data_warehouse()
