from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Locators:
    editor = '//textarea[@id="textareaCodeSQL"]/../div'
    run_button = '//button[@class="ws-btn"]'
    column_value = '//tr/td[text()="{search_text}"]/../td[{column_number}]'
    records_count = '//div[@id="divResultSQL"]//div//div'
    query_result_text = '//div[@id="divResultSQL"]//div'
    result_table_row = '//div[@id="divResultSQL"]//tbody//tr'


class CustomersTableColumns(IntEnum):
    CUSTOMER_ID = 1
    CUSTOMER_NAME = 2
    CONTACT_NAME = 3
    ADDRESS = 4
    CITY = 5
    POSTAL_CODE = 6
    COUNTRY = 7

    @classmethod
    def to_list(cls, exclude=None):
        exclude = exclude if exclude is not None else []
        return [column for column in cls if (column not in exclude)]


class TrySQLPage:

    locators: Locators = Locators()

    def enter_query(self, sb, query):
        sb.wait_for_element_visible(selector=self.locators.editor)
        sb.execute_script(
            f"window.editor.setValue(arguments[0]);", query
        )

    def run_sql(self, sb):
        sb.click(self.locators.run_button)

    def check_value_in_column(
            self, sb, expected_value, search_text, column_number
    ):
        selector = self.locators.column_value.format(
            search_text=search_text, column_number=column_number
        )
        sb.assert_text(expected_value, selector)

    def check_number_of_records(self, sb, records_count):
        if records_count == 0:
            sb.assert_text('No result.', self.locators.query_result_text)
        else:
            sb.assert_text(
                f'Number of Records: {records_count}',
                selector=self.locators.records_count
            )
            records_count_with_title = records_count + 1
            sb.assert_equal(
                first=len(sb.find_elements(self.locators.result_table_row)),
                second=records_count_with_title
            )

    def check_values_in_table_row(self, sb, expected_values, search_text, columns):
        for expected_text, column in zip(expected_values, columns):
            self.check_value_in_column(
                sb=sb,
                expected_value=expected_text,
                search_text=search_text,
                column_number=column
            )
