from django.shortcuts import render
from ta_app.commands_interface import CommandsInterface


class Commands(CommandsInterface):

    def login(self, user, password):
        pass

    def logout(self):
        pass

    def create_course(self, name, section, days, times, labs):
        pass

    def create_account(self, user, password, role):
        pass

    def delete_account(self, user, password, role):
        pass

    def edit_account(self, user):
        pass

    def assign_instructor(self, user, course):
        pass

    def assign_ta_to_course(self, user, course):
        pass

    def assign_ta_to_lab(self, user, course, lab):
        pass

    def read_contact_info(self):
        pass

    def edit_contact_info(self):
        pass

    def view_course_assignments(self):
        pass

    def view_ta_assignments(self):
        pass

    def help(self):
        pass

    def get_current_user(self):
        pass

    def call_command(self, command):
        pass

# Create your views here.
