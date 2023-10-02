import re
import time
from typing import List

import pandas
import pandas as pd
import pandera as pa
from pandera import Column, Check

from utilities.SchoolExcelGenerator import SchoolExcelGenerator


class SchoolExcelValidator:
    """
    class_data = ["Class1", "Class2", "Class3"]
    section_data = ["Section1", "Section2", "Section3"]
    session_data = ["Session1","Session2","Session3"]

    student_data = pd.read_excel("Student.xlsx", sheet_name="Student Data",skiprows=1,dtype=str)

    subject_data = pd.read_excel("Subject.xlsx", sheet_name="Subject Data",skiprows=1,dtype=str)

    teacher_data = pd.read_excel("Teacher.xlsx", sheet_name="Teachers Data", skiprows=1, dtype=str)

    result_data = pd.read_excel("Result.xlsx", sheet_name="Result", dtype=str)

    """

    valid_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "E", "F", "AB"]

    def __init__(self):
        self.__invalid_value_or_null = " contains invalid values or null"
        self.__invalid_space_alphanumeric_null = " either contains spaces or non alpha numeric values or null"
        self.__invalid_space_alphanumeric = " either contains spaces or non alpha numeric values"
        self.__duplicate_or_invalid = " contains duplicates or is invalid"
        self.__invalid = "Invalid "
        self.__unexpected_error = "Unexpected Error Occurred"
        self.__contact_owner = "Please contact owner"
        self.__changed_excel = "Excel file is changed"
        self.__incorrect_excel = "Incorrect Excel"
        self.__valid_gender = " Valid gender Male or Female "
        self.__title = "title"
        self.__description = "description"
        self.__html = "html"

    def generate_student_excel_errors(self, student_data: pandas.DataFrame, session_data: list,
                                      class_data: list, section_data: list,
                                      student_registration_set: set):
        """
        only use this method if is_student_excel_valid return false
        otherwise method return None
        :param student_data:
        :param session_data:
        :param class_data:
        :param section_data:
        :param student_registration_set
        :return: error
        """

        try:
            if not set(student_data.columns) == set(SchoolExcelGenerator.pre_filled_student_data):
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}
            student_schema = self.__create_student_schema(session_data, class_data, section_data,
                                                          student_registration_set)
            student_schema.validate(student_data)

        except pa.errors.SchemaError as exc:
            print("hi")
            print(exc.schema.description)
            return {self.__title: exc.schema.title,
                    self.__description: exc.schema.description,
                    self.__html: exc.failure_cases.to_dict()}

        except Exception as e:
            # TODO unexpected error log
            print(e)

            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner+str(e),
                    self.__html: ""}

    def generate_data_response(self, data):
        """
        only use if excel is valid
        :param data:
        :return:
        """
        try:
            return data.to_dict("records")
        except Exception as e:
            # TODO unexpected error log
            return

    def read_excel(self, file_path, sheet_name, skiprows):
        """
        student_data = pd.read_excel("Student.xlsx", sheet_name="Student Data",skiprows=1,dtype=str)

        subject_data = pd.read_excel("Subject.xlsx", sheet_name="Subject Data",skiprows=1,dtype=str)

        teacher_data = pd.read_excel("Teacher.xlsx", sheet_name="Teachers Data", skiprows=1, dtype=str)

        result_data = pd.read_excel("Result.xlsx", sheet_name="Result", dtype=str)

        """
        try:
            data = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows, dtype=str)
            return data.where(pd.notnull(data), None)
        except Exception as e:
            # TODO unexpected error log unable to read excel
            return None

    def generate_subject_excel_errors(self, subject_data: pandas.DataFrame, class_data: list,
                                      section_data: list, teacher_data: list, session_data: list):
        """
        only use this method if is_subject_excel_valid return false
        otherwise method return None
        :param session_data:
        :param subject_data:
        :param class_data:
        :param section_data:
        :param teacher_data:
        :return: error
        """

        try:
            if not set(subject_data.columns) == set(SchoolExcelGenerator.pre_filled_subject_data):
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}
            subject_schema = self.__create_subject_schema(SchoolExcelGenerator.subject_type, class_data, section_data,
                                                          teacher_data, session_data)
            subject_schema.validate(subject_data)

        except pa.errors.SchemaError as exc:
            return {self.__title: exc.schema.title,
                    self.__description: exc.schema.description,
                    self.__html: exc.failure_cases.to_dict()}

        except Exception as e:
            print(e)
            # TODO unexpected error log
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner,
                    self.__html: ""}

    def generate_teacher_excel_errors(self, teacher_data: pandas.DataFrame, class_data: list,
                                      section_data: list):
        """
        only use this method if is_subject_excel_valid return false
        otherwise method return None
        :param teacher_data:
        :param class_data:
        :param section_data:
        :return: error

        response{'title': 'Invalid Full Name',
        'Description': 'Full Name is null',
         'html':
        '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n
          <th></th>\n      <th>index</th>\n      <th>failure_case</th>\n    </tr>\n  </thead>\n  <tbody>\n
           <tr>\n      <th>0</th>\n      <td>18</td>\n      <td>NaN</td>\n    </tr>\n  </tbody>\n
           </table>'}

        """

        try:
            if not set(teacher_data.columns) == set(SchoolExcelGenerator.pre_filled_teacher_data):
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}
            teacher_schema = self.__create_teacher_schema(class_data, section_data)
            teacher_schema.validate(teacher_data)

        except pa.errors.SchemaError as exc:
            return {self.__title: exc.schema.title,
                    self.__description: exc.schema.description,
                    self.__html: exc.failure_cases.to_dict()}

        except Exception as e:
            # TODO unexpected error log
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner,
                    self.__html: ""}

    def generate_detail_excel_errors(self, detail_data: pandas.DataFrame, details: dict):
        """
        Note this method requires Header to be None
        detail = {'Class': 1, 'Class Teacher': 'asasaas', 'Created By': 'Asad', 'Section': 'A', 'Session': '22-23', 'Test': 'Unit 1'}
         detail_data = d.read_excel("Result.xlsx",sheet_name="Details",header=None)
        :param detail_data:
        :param details:
        :return: boolean
        """

        records = detail_data.to_dict(("records"))
        detail_values = dict()
        for record in records:
            detail_values[record[0]] = record[1]
        attendance = detail_values.pop("Max Days of Attendance")
        try:
            if attendance == None:
                return {self.__title: self.__incorrect_excel,
                        self.__description: "Max Days of Attendance" + self.__invalid_value_or_null,
                        self.__html: ""}
            if not detail_values == details:
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}
        except Exception as e:
            # TODO unexpected error log
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner,
                    self.__html: ""}

    def generate_result_excel_errors(self, result_data: pandas.DataFrame,
                                     student_info: list,
                                     academic_subject: list,
                                     co_scholastic_subject: list,
                                     co_curricular_subject: list):
        """
        only use this method if is_result_excel_valid return false
        otherwise method return None
        :return: error

        response{'title': 'Invalid Full Name',
        'Description': 'Full Name is null',
         'html':
        '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n
          <th></th>\n      <th>index</th>\n      <th>failure_case</th>\n    </tr>\n  </thead>\n  <tbody>\n
           <tr>\n      <th>0</th>\n      <td>18</td>\n      <td>NaN</td>\n    </tr>\n  </tbody>\n
           </table>'}
        """
        student_info_from_excel = result_data.iloc[:, 0:2].astype({"student_id": int}).to_dict("records")
        try:
            if not [i for i in student_info if i not in student_info_from_excel] == []:
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}

            result_schema = self.__create_result_schema(academic_subject, co_scholastic_subject, co_curricular_subject)
            # print(result_data)
            result_schema.validate(result_data)
        except pa.errors.SchemaError as exc:
            print("hello 246")
            print(exc)
            # print(exc)
            return {self.__title: exc.schema.title,
                    self.__description: exc.schema.description,
                    self.__html: exc.failure_cases.to_dict()}

        except Exception as e:
            print(e)
            print(e.__dict__)
            # TODO unexpected error log
            # print(e)
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner+(e),
                    self.__html: ""}

    def generate_result_subject_info_excel_errors(self, subject_info_excel: pandas.DataFrame,
                                                  subject_info: list):
        """
        only use this method if is_result_subject_info_valid return false
        otherwise method return None
        :return: error

        response{'title': 'Invalid Full Name',
        'Description': 'Full Name is null',
         'html':
        '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n
          <th></th>\n      <th>index</th>\n      <th>failure_case</th>\n    </tr>\n  </thead>\n  <tbody>\n
           <tr>\n      <th>0</th>\n      <td>18</td>\n      <td>NaN</td>\n    </tr>\n  </tbody>\n
           </table>'}
        """
        subject_info_from_excel = subject_info_excel.iloc[:, 0:3].to_dict("records")
        try:
            if not [i for i in subject_info if i not in subject_info_from_excel] == []:
                return {self.__title: self.__incorrect_excel,
                        self.__description: self.__changed_excel,
                        self.__html: ""}

            result_subject_info_schema = self.__create_result_subject_info_schema()
            result_subject_info_schema.validate(subject_info_excel)

        except pa.errors.SchemaError as exc:
            if not exc.check:
                pass
            else:
                if isinstance(exc.check, Check):
                    return {self.__title: exc.check.title,
                            self.__description: exc.check.description,
                            self.__html: exc.failure_cases.to_dict()}
                else:
                    # print("Null values")
                    return {self.__title: "Null values",
                            self.__description: "Null values found in subject info",
                            self.__html: exc.failure_cases.to_dict()}
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner,
                    self.__html: ""}

        except Exception as e:
            # print(e)
            # TODO unexpected error log
            print()
            print(e)
            return {self.__title: self.__unexpected_error,
                    self.__description: self.__contact_owner,
                    self.__html: ""}

    def is_student_excel_valid(self, student_data: pandas.DataFrame, session_data: list,
                               class_data: list, section_data: list, student_registration_set: set) -> bool:
        """

        :param student_data:
        :param session_data:
        :param class_data:
        :param section_data:
        :return: error

        response{'title': 'Invalid Full Name',
        'Description': 'Full Name is null',
         'html':
        '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n
          <th></th>\n      <th>index</th>\n      <th>failure_case</th>\n    </tr>\n  </thead>\n  <tbody>\n
           <tr>\n      <th>0</th>\n      <td>18</td>\n      <td>NaN</td>\n    </tr>\n  </tbody>\n
           </table>'}
        """
        try:
            if not set(student_data.columns) == set(SchoolExcelGenerator.pre_filled_student_data):
                return False
            student_schema = self.__create_student_schema(session_data, class_data, section_data,
                                                          student_registration_set)
            student_schema.validate(student_data)
            return True
        except Exception as e:
            return False

    def is_subject_excel_valid(self, subject_data: pandas.DataFrame, class_data: list,
                               section_data: list, teacher_data: list, session_data: list) -> bool:
        """
        :param subject_data:
        :param class_data:
        :param section_data:
        :param teacher_data:
        :return: error

        response{'title': 'Invalid Full Name',
        'Description': 'Full Name is null',
         'html':
        '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n
          <th></th>\n      <th>index</th>\n      <th>failure_case</th>\n    </tr>\n  </thead>\n  <tbody>\n
           <tr>\n      <th>0</th>\n      <td>18</td>\n      <td>NaN</td>\n    </tr>\n  </tbody>\n
           </table>'}
        """
        try:
            if not set(subject_data.columns) == set(SchoolExcelGenerator.pre_filled_subject_data):
                return False
            subject_schema = self.__create_subject_schema(SchoolExcelGenerator.subject_type, class_data,
                                                          section_data, teacher_data, session_data)
            subject_schema.validate(subject_data)
            return True
        except Exception as e:
            print("hello 364")
            print(e)
            return False

    def is_teacher_excel_valid(self, teacher_data: pandas.DataFrame, class_data: list,
                               section_data: list) -> bool:
        try:
            if not set(teacher_data.columns) == set(SchoolExcelGenerator.pre_filled_teacher_data):
                return False
            teacher_schema = self.__create_teacher_schema(class_data, section_data)
            teacher_schema.validate(teacher_data)
            return True
        except Exception as e:
            return False

    def is_result_excel_valid(self,
                              result_data: pandas.DataFrame,
                              student_info: list,
                              academic_subject: list,
                              co_scholastic_subject: list,
                              co_curricular_subject: list) -> bool:

        student_info_from_excel = result_data.iloc[:, 0:2].astype({"student_id": int}).to_dict("records")
        try:
            if not [i for i in student_info if i not in student_info_from_excel] == []:
                return False
            result_schema = self.__create_result_schema(academic_subject, co_scholastic_subject, co_curricular_subject)
            result_schema.validate(result_data)
            return True
        except Exception as e:
            print("hum")
            print(e)
            return False

    def is_result_subject_info_valid(self,
                                     subject_info_excel: pandas.DataFrame,
                                     subject_info: list) -> bool:

        subject_info_from_excel = subject_info_excel.iloc[:, 0:3].to_dict("records")
        try:
            if not [i for i in subject_info if i not in subject_info_from_excel] == []:
                return False
            result_subject_info_schema = self.__create_result_subject_info_schema()
            result_subject_info_schema.validate(subject_info_excel)
            return True
        except Exception as e:
            return False

    def is_result_detail_valid(self, detail_data: pandas.DataFrame, details: dict):
        """
        Note this method requires Header to be None
        detail = {'Class': 1, 'Class Teacher': 'asasaas', 'Created By': 'Asad', 'Section': 'A', 'Session': '22-23', 'Test': 'Unit 1'}
         detail_data = d.read_excel("Result.xlsx",sheet_name="Details",header=None)
        :param detail_data:
        :param details:
        :return: boolean
        """
        records = detail_data.to_dict(("records"))
        detail_values = dict()
        for record in records:
            detail_values[record[0]] = record[1]
        attendance = detail_values.pop("Max Days of Attendance")
        try:
            if attendance == None:
                return False
            if not detail_values == details:
                return False
            return True
        except Exception as e:
            # TODO unexpected error log
            return False

    def __email_validator(self, email) -> bool:
        email_regex = "^[\w\.-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,}$"
        if re.match(email_regex, email):
            return True
        return False

    def __create_student_schema(self, session_data: list, class_data: list, section_data: list,
                                student_registration_set: set):
        first_name = SchoolExcelGenerator.pre_filled_student_data[0]
        middle_name = SchoolExcelGenerator.pre_filled_student_data[1]
        last_name = SchoolExcelGenerator.pre_filled_student_data[2]
        date_of_birth = SchoolExcelGenerator.pre_filled_student_data[3]
        email = SchoolExcelGenerator.pre_filled_student_data[4]
        registration_number = SchoolExcelGenerator.pre_filled_student_data[5]
        mother_name = SchoolExcelGenerator.pre_filled_student_data[7]
        phone_number = SchoolExcelGenerator.pre_filled_student_data[8]
        address_line_1 = SchoolExcelGenerator.pre_filled_student_data[9]
        address_line_2 = SchoolExcelGenerator.pre_filled_student_data[10]
        city = SchoolExcelGenerator.pre_filled_student_data[11]
        state = SchoolExcelGenerator.pre_filled_student_data[12]
        country = SchoolExcelGenerator.pre_filled_student_data[13]
        pincode = SchoolExcelGenerator.pre_filled_student_data[14]
        gender = SchoolExcelGenerator.pre_filled_student_data[15]
        session = SchoolExcelGenerator.pre_filled_student_data[16]
        class_value = SchoolExcelGenerator.pre_filled_student_data[17]
        section = SchoolExcelGenerator.pre_filled_student_data[18]

        student_schema = pa.DataFrameSchema(
            {
                first_name: Column(str,
                                   title=self.__invalid + first_name,
                                   description=first_name + self.__invalid_space_alphanumeric_null, nullable=False),
                middle_name: Column(str, None,
                                    title=self.__invalid + middle_name,
                                    description=middle_name + self.__invalid_space_alphanumeric,
                                    nullable=True),
                last_name: Column(str, None,
                                  title=self.__invalid + last_name,
                                  description=last_name + self.__invalid_space_alphanumeric_null,
                                  nullable=True),
                date_of_birth: Column(str, title=self.__invalid + date_of_birth,
                                      description=self.__invalid + self.__invalid_value_or_null, nullable=False),
                email: Column(str, None,
                              title=self.__invalid + email,
                              description=email + self.__invalid, nullable=True),
                registration_number: Column(str, Check(
                    lambda reg: reg.map(lambda r_num: r_num not in student_registration_set)),
                                            title=self.__invalid + registration_number,
                                            description=registration_number + self.__invalid_value_or_null,
                                            nullable=False,
                                            unique=True),
                mother_name: Column(str, title=self.__invalid + mother_name,
                                    description=mother_name + self.__invalid_value_or_null, nullable=False),
                phone_number: Column(str, Check(lambda name: name.str.isnumeric()),
                                     title=self.__invalid + phone_number,
                                     description=phone_number + self.__invalid_value_or_null, nullable=False),
                address_line_1: Column(str,
                                       title=self.__invalid + address_line_1,
                                       description=address_line_1 + self.__invalid_value_or_null, nullable=False),
                address_line_2: Column(str,
                                       title=self.__invalid + address_line_2,
                                       description=address_line_2 + self.__invalid_value_or_null,
                                       nullable=True),
                city: Column(str,
                             title=self.__invalid + city,
                             description=city + self.__invalid_value_or_null, nullable=False),
                state: Column(str,
                              title=self.__invalid + state,
                              description=state + self.__invalid_value_or_null, nullable=False),
                country: Column(str,
                                title=self.__invalid + country,
                                description=country + self.__invalid_value_or_null, nullable=False),
                pincode: Column(str,
                                title=self.__invalid + pincode,
                                description=pincode + self.__invalid_value_or_null, nullable=False),
                gender: Column(str, Check.isin(SchoolExcelGenerator.gender),
                               title=self.__invalid + gender,
                               description=gender + self.__invalid_value_or_null + self.__valid_gender, nullable=False),
                session: Column(str, Check.isin(session_data),
                                title=self.__invalid + session,
                                description=session + self.__invalid_value_or_null, nullable=False),
                class_value: Column(str, Check.isin(class_data),
                                    title=self.__invalid + class_value,
                                    description=class_value + self.__invalid_value_or_null, nullable=False),
                section: Column(str, Check.isin(section_data),
                                title=self.__invalid + section,
                                description=self.__invalid + self.__invalid_value_or_null, nullable=False)
            }
        )
        return student_schema

    def __create_subject_schema(self, subject_type, class_data, section_data, teacher_data, session_data):
        subject_name = SchoolExcelGenerator.pre_filled_subject_data[0]
        subject_type_value = SchoolExcelGenerator.pre_filled_subject_data[1]
        class_value = SchoolExcelGenerator.pre_filled_subject_data[2]
        section = SchoolExcelGenerator.pre_filled_subject_data[3]
        teacher_email = SchoolExcelGenerator.pre_filled_subject_data[4]
        session = SchoolExcelGenerator.pre_filled_subject_data[5]
        subject_schema = pa.DataFrameSchema(
            {
                subject_name: Column(str, title=self.__invalid + subject_name,
                                     description=subject_name + self.__invalid_value_or_null, nullable=False),
                subject_type_value: Column(str, Check.isin(subject_type),
                                           title=self.__invalid + subject_type_value,
                                           description=subject_type_value + self.__invalid_value_or_null,
                                           nullable=False),
                class_value: Column(str, Check.isin(class_data),
                                    title=self.__invalid + class_value,
                                    description=class_value + self.__invalid_value_or_null, nullable=False),
                section: Column(str, Check.isin(section_data),
                                title=self.__invalid + section,
                                description=section + self.__invalid_value_or_null, nullable=False),
                teacher_email: Column(str, Check.isin(teacher_data),
                                      title=self.__invalid + teacher_email,
                                      description=teacher_email + self.__invalid_value_or_null, nullable=False),
                session: Column(str, Check.isin(session_data),
                                title=self.__invalid + session,
                                description=session + self.__invalid_value_or_null, nullable=False)
            }
        )
        return subject_schema

    def __create_teacher_schema(self, class_data: list, section_data: list):
        full_name = SchoolExcelGenerator.pre_filled_teacher_data[0]
        email = SchoolExcelGenerator.pre_filled_teacher_data[1]
        phone_number = SchoolExcelGenerator.pre_filled_teacher_data[2]
        gender = SchoolExcelGenerator.pre_filled_teacher_data[4]
        is_class_teacher = SchoolExcelGenerator.pre_filled_teacher_data[5]
        class_value = SchoolExcelGenerator.pre_filled_teacher_data[6]
        section = SchoolExcelGenerator.pre_filled_teacher_data[7]
        teacher_schema = pa.DataFrameSchema(
            {
                full_name: Column(str,
                                  title=self.__invalid + full_name,
                                  description=full_name + self.__invalid_value_or_null, nullable=False),
                email: Column(str, Check(lambda name: name.map(lambda email: self.__email_validator(email))),
                              title=self.__invalid + email,
                              description=email + self.__invalid_value_or_null, nullable=False),
                phone_number: Column(str, Check(lambda name: name.str.isnumeric()),
                                     title=self.__invalid + phone_number,
                                     description=self.__invalid + self.__invalid_value_or_null, nullable=False),
                gender: Column(str, Check.isin(SchoolExcelGenerator.gender),
                               title=self.__invalid + gender,
                               description=gender + self.__invalid_value_or_null + self.__valid_gender, nullable=False),
                class_value: Column(str, Check.isin(class_data),
                                    title=self.__invalid + class_value,
                                    description=class_value + self.__invalid_value_or_null, nullable=True),
                section: Column(str, Check.isin(section_data),
                                title=self.__invalid + section,
                                description=section + self.__invalid_value_or_null, nullable=True),
                is_class_teacher: Column(str, Check.isin(SchoolExcelGenerator.boolean),
                                         title=self.__invalid + is_class_teacher,
                                         description=is_class_teacher + self.__invalid_value_or_null,
                                         nullable=False)
            }
        )
        return teacher_schema

    def __create_result_schema(self, academic_subject: list, co_scholastic_subject: list, co_curricular_subject: list):
        result_schema_dict = {
            "Attendance": Column(str, Check(lambda name: name.map(lambda marks: self.__is_number_or_absent(marks))),
                                 title=self.__invalid + "Attendance",
                                 description="Attendance" + self.__invalid_value_or_null,
                                 nullable=False),
            "Remark": Column(str, title=self.__invalid + "Remark",
                             description="Remark" + self.__invalid_value_or_null,
                             nullable=True)
        }

        for subject in academic_subject:
            result_schema_dict[subject] = Column(str, Check(
                lambda name: name.map(lambda marks: self.__is_number_or_absent(marks))),
                                                 title=self.__invalid + subject,
                                                 description=subject + self.__invalid_value_or_null,
                                                 nullable=True)

        for subject in co_scholastic_subject:
            result_schema_dict[subject] = Column(str, Check.isin(self.valid_grades),
                                                 title=self.__invalid + subject,
                                                 description=subject + self.__invalid_value_or_null,
                                                 nullable=True)

        for subject in co_curricular_subject:
            result_schema_dict[subject] = Column(str, Check(
                lambda name: name.map(lambda marks: self.__is_number_or_absent(marks))),
                                                 title=self.__invalid + subject,
                                                 description=subject + self.__invalid_value_or_null,
                                                 nullable=False)

        result_schema = pa.DataFrameSchema(result_schema_dict)
        return result_schema

    def __create_result_subject_info_schema(self):
        min_marks = "Min Marks"
        max_marks = "Max Marks"
        result_subject_schema = pa.DataFrameSchema({
            min_marks: Column(str, [
                Check(lambda g: g["Academics"].str.isnumeric(),
                      groupby="Subject Type",
                      title=self.__invalid + min_marks,
                      description=self.__invalid + min_marks + " for Academic Subject"),
                Check(lambda g: g["Co-Curricular"].str.isnumeric(),
                      groupby="Subject Type",
                      title=self.__invalid + min_marks,
                      description=self.__invalid + min_marks + " for Co-Curricular subject"),
                Check(lambda g: g["Co-Scholastic"].isin(SchoolExcelValidator.valid_grades),
                      groupby="Subject Type",
                      title=self.__invalid + min_marks,
                      description=self.__invalid + min_marks + " for Co-Scholastic subject input must be grades")
            ], nullable=False),

            "Max Marks": Column(str, [
                Check(lambda g: g["Academics"].str.isnumeric(),
                      groupby="Subject Type",
                      title=self.__invalid + max_marks,
                      description=self.__invalid + max_marks + " for Academic subject"),
                Check(lambda g: g["Co-Curricular"].str.isnumeric(),
                      groupby="Subject Type",
                      title=self.__invalid + max_marks,
                      description=self.__invalid + max_marks + " for Co-Curricular subject"),
                Check(lambda g: g["Co-Scholastic"].isin(SchoolExcelValidator.valid_grades),
                      groupby="Subject Type",
                      title=self.__invalid + max_marks,
                      description=self.__invalid + max_marks + " for Co-Scholastic subject input must be grades")
            ], nullable=False),
            "Subject Type": pa.Column(str)
        })
        return result_subject_schema

    def __is_number_or_absent(self, value):
        try:
            float(value)
            return True
        except ValueError:
            if value == "AB" or value == "Ab" or value == "ab":
                return True
            return False
        except TypeError:
            if not value:
                return True
            return False
