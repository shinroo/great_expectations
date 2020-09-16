import logging
import pytest


from great_expectations.execution_environment.data_connector.partitioner.regex_partitioner import RegexPartitioner
from great_expectations.execution_environment.data_connector.partitioner.partition import Partition
from great_expectations.execution_environment.data_connector.partitioner.lexicographic_sorter import LexicographicSorter
from great_expectations.execution_environment.data_connector.partitioner.date_time_sorter import DateTimeSorter
from great_expectations.execution_environment.data_connector.partitioner.numeric_sorter import NumericSorter

try:
    from unittest import mock
except ImportError:
    import mock

logger = logging.getLogger(__name__)

"""
asset_param = {
    "test_asset": {
        "partition_regex": r"file_(.*)_(.*).csv",
        "partition_param": ["year", "file_num"],
        "partition_delimiter": "-",
        "reader_method": "read_csv",
    }
}

"""
# TODO: <Alex>We might wish to invent more cool paths to test and different column types and sort orders...</Alex>
batch_paths = [
  "my_dir/alex_20200809_1000.csv",
  "my_dir/eugene_20200809_1500.csv",
  "my_dir/james_20200811_1009.csv",
  "my_dir/abe_20200809_1040.csv",
  "my_dir/will_20200809_1002.csv",
  "my_dir/james_20200713_1567.csv",
  "my_dir/eugene_20201129_1900.csv",
  "my_dir/will_20200810_1001.csv",
  "my_dir/james_20200810_1003.csv",
  "my_dir/alex_20200819_1300.csv",
]


def test_regex_partitioner():
    # TODO: <Alex>We might wish to invent more cool paths to test and different column types and sort orders...</Alex>
    my_partitioner = RegexPartitioner(
        name="mine_all_mine",
        sorters=[
            LexicographicSorter(name='name', orderby='asc'),
            DateTimeSorter(name='timestamp', orderby='desc', datetime_format='%Y%m%d'),
            NumericSorter(name='price', orderby='desc')
        ]
    )
    # TODO: <Alex>Do not delete this yet, because we do need to have the test where no sorters are configured!</Alex>
    # TODO: <Alex>Delete only after this ("group_") test has been placed in its own test method.</Alex>
    # my_partitioner = RegexPartitioner(name="mine_all_mine", sorters=None)
    regex = r".*/(.*)_(.*)_(.*).csv"

    # test 1: no regex configured. we  raise error
    with pytest.raises(ValueError) as exc:
        partitions = my_partitioner.get_available_partitions(batch_paths)

    # set the regex
    my_partitioner.regex = regex
    returned_partitions = my_partitioner.get_available_partitions(batch_paths)
    # TODO: <Alex>Do not delete this yet, because we do need to have the test where no sorters are configured!</Alex>
    # TODO: <Alex>Delete only after this ("group_") test has been placed in its own test method.</Alex>
    # assert returned_partitions == [
    #     Partition(name='alex-20200809-1000', definition={'group_0': 'alex', 'group_1': '20200809', 'group_2': '1000'}),
    #     Partition(name='eugene-20200809-1500', definition={'group_0': 'eugene', 'group_1': '20200809', 'group_2': '1500'}),
    #     Partition(name='james-20200811-1009', definition={'group_0': 'james', 'group_1': '20200811', 'group_2': '1009'}),
    #     Partition(name='abe-20200809-1040', definition={'group_0': 'abe', 'group_1': '20200809', 'group_2': '1040'}),
    #     Partition(name='will-20200809-1002', definition={'group_0': 'will', 'group_1': '20200809', 'group_2': '1002'}),
    #     Partition(name='james-20200713-1567', definition={'group_0': 'james', 'group_1': '20200713', 'group_2': '1567'}),
    #     Partition(name='eugene-20201129-1900', definition={'group_0': 'eugene', 'group_1': '20201129', 'group_2': '1900'}),
    #     Partition(name='will-20200810-1001', definition={'group_0': 'will', 'group_1': '20200810', 'group_2': '1001'}),
    #     Partition(name='james-20200810-1003', definition={'group_0': 'james', 'group_1': '20200810', 'group_2': '1003'}),
    #     Partition(name='alex-20200819-1300', definition={'group_0': 'alex', 'group_1': '20200819', 'group_2': '1300'}),
    # ]
    assert returned_partitions == [
        Partition(name='abe-20200809-1040', definition={'name': 'abe', 'timestamp': '20200809', 'price': '1040'}),
        Partition(name='alex-20200819-1300', definition={'name': 'alex', 'timestamp': '20200819', 'price': '1300'}),
        Partition(name='alex-20200809-1000', definition={'name': 'alex', 'timestamp': '20200809', 'price': '1000'}),
        Partition(name='eugene-20201129-1900', definition={'name': 'eugene', 'timestamp': '20201129', 'price': '1900'}),
        Partition(name='eugene-20200809-1500', definition={'name': 'eugene', 'timestamp': '20200809', 'price': '1500'}),
        Partition(name='james-20200811-1009', definition={'name': 'james', 'timestamp': '20200811', 'price': '1009'}),
        Partition(name='james-20200810-1003', definition={'name': 'james', 'timestamp': '20200810', 'price': '1003'}),
        Partition(name='james-20200713-1567', definition={'name': 'james', 'timestamp': '20200713', 'price': '1567'}),
        Partition(name='will-20200810-1001', definition={'name': 'will', 'timestamp': '20200810', 'price': '1001'}),
        Partition(name='will-20200809-1002', definition={'name': 'will', 'timestamp': '20200809', 'price': '1002'}),
    ]

    # partition names
    returned_partition_names = my_partitioner.get_available_partition_names(batch_paths)
    assert returned_partition_names == [
        'abe-20200809-1040',
        'alex-20200819-1300',
        'alex-20200809-1000',
        'eugene-20201129-1900',
        'eugene-20200809-1500',
        'james-20200811-1009',
        'james-20200810-1003',
        'james-20200713-1567',
        'will-20200810-1001',
        'will-20200809-1002',
    ]
