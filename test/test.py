from proligent.model import UTIL, Limit, Measure, StepRun, SequenceRun, OperationRun, ProductUnit, DataWareHouse, ProcessRun, LimitExpression
from proligent.datawarehouse.datawarehouse_model import ExecutionStatusKind
import datetime

if __name__ == '__main__':
    limit = Limit(LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND, lower_bound=10, higher_bound=25)  # 10 <= X <= 25
    start_time = datetime.datetime.now()
    end_time = start_time = start_time + datetime.timedelta(seconds=5)
    measure = Measure(0, status=ExecutionStatusKind.PASS, limit=limit, time=end_time)
    step = StepRun(
        measure=measure,
        name='Step1',
        start_time=start_time,
        end_time=end_time)
    sequence = SequenceRun(
        steps=[step],
        name='Sequence1',
        station='Station1',
        start_time=start_time,
        end_time=end_time)
    operation = OperationRun(
        sequences=[sequence],
        name='Operation1',
        start_time=start_time,
        end_time=end_time)
    process = ProcessRun(
        product_unit_identifier='ABCDEFG',
        product_full_name='DUT',
        operations=[operation],
        name='Process1',
        start_time=start_time,
        end_time=end_time)
    product = ProductUnit(
        product_unit_identifier='ABCDEFG',
        product_full_name='DUT',
        manufacturer='Averna')
    warehouse = DataWareHouse(
        top_process=process,
        product_unit=product)
    warehouse.save_xml('c:\\Temp\\Proligent_PythonToQuickView_Example.xml')
