from abc import ABC, abstractmethod
import datetime
import json


class Builder(ABC):

    @abstractmethod
    def build_title_section(self, ctx):
        pass

    @abstractmethod
    def build_filter_section(self, ctx):
        pass

    @abstractmethod
    def get_result(self):
        pass


class SectionBuilder(Builder):

    def __init__(self):
        self._report = Report()

    def reset(self):
        self._report = ''

    def __header(self):
        return '*' * 70

    def build_title_section(self, ctx):
        section = self.__header()
        section += f'\nTitle: {ctx["query"]["name"]} Report'
        section += f'\nDate: {datetime.datetime.now()}\n'
        self._report.add(section)

    def build_filter_section(self, ctx):
        section = self.__header()
        section += f'\nFilter: {ctx["section"]}'
        formatted_results = json.dumps(ctx['results'], indent=4)
        section += f'\nResults: \n{formatted_results}\n'
        self._report.add(section)

    def get_result(self):
        report = self._report
        self.reset()
        return report


class Report:
    def __init__(self):
        self.sections = []

    def add(self, section):
        self.sections.append(section)

    def print(self):
        for x in self.sections:
            print(x)


class Reporter:
    def __init__(self):
        self.builder = SectionBuilder()

    def __set_builder(self, builder: Builder):
        self.builder = builder

    def __set_context(self, ctx):
        self.ctx = ctx

    def construct(self, ctx):
        self.builder.build_title_section(ctx)
        for section in ctx['results']:
            self.builder.build_filter_section(section)
        return self.builder.get_result()
