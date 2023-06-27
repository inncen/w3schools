import pytest

from models.customer import Customer
from pages.try_sql import TrySQLPage, CustomersTableColumns


class TestCustomers:

    url = 'https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all'

    @pytest.mark.parametrize(
        'name, address, column_number',
        [('Giovanni Rovelli',
          'Via Ludovico il Moro 22',
          CustomersTableColumns.ADDRESS)],
        ids=['Select customer']
    )
    def test_select_all_customers(self, sb, name, address, column_number):
        sb.open(self.url)
        TrySQLPage().enter_query(sb, 'select * from Customers;')
        TrySQLPage().run_sql(sb)
        TrySQLPage().check_value_in_column(
            sb,
            expected_value=address,
            search_text=name,
            column_number=column_number
        )

    def test_filter_customers(self, sb):
        sb.open(self.url)
        TrySQLPage().enter_query(
            sb, 'select * from Customers where City="London";'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().check_number_of_records(sb, 6)

    @pytest.mark.parametrize(
        'customer', [Customer.random()], ids=['Create random customer']
    )
    def test_create_customer(self, sb, customer):
        sb.open(self.url)
        TrySQLPage().enter_query(
            sb,
            f'insert into Customers {customer.columns()} '
            f'values {customer.values()};'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().enter_query(
            sb,
            f'select * from Customers '
            f'where CustomerName="{customer.customer_name}";'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().check_number_of_records(sb, 1)
        TrySQLPage().check_values_in_table_row(
            sb,
            expected_values=customer.values(),
            search_text=customer.customer_name,
            columns=CustomersTableColumns.to_list(
                exclude=[CustomersTableColumns.CUSTOMER_ID]
            )
        )

    @pytest.mark.parametrize(
        'customer_id, customer',
        [(1, Customer.random())],
        ids=['Update customer with id=1']
    )
    def test_update_customer(self, sb, customer_id, customer):
        sb.open(self.url)
        TrySQLPage().enter_query(
            sb,
            f'update Customers set {customer.columns_with_values()} '
            f'where CustomerID={customer_id};'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().enter_query(
            sb,
            f'select * from Customers where CustomerID="{customer_id}";'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().check_values_in_table_row(
            sb,
            expected_values=customer.values(),
            search_text=customer.customer_name,
            columns=CustomersTableColumns.to_list(
                exclude=[CustomersTableColumns.CUSTOMER_ID]
            )
        )

    @pytest.mark.parametrize(
        'customer_id', [1], ids=['Delete customer with id=1']
    )
    def test_delete_customer(self, sb, customer_id):
        sb.open(self.url)
        TrySQLPage().enter_query(
            sb,
            f'delete from Customers where CustomerID="{customer_id}";'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().enter_query(
            sb,
            f'select * from Customers where CustomerID="{customer_id}";'
        )
        TrySQLPage().run_sql(sb)
        TrySQLPage().check_number_of_records(sb, 0)
