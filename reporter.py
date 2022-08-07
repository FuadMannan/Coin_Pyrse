from abc import ABC, abstractmethod
import datetime


class Builder(ABC):

    @abstractmethod
    def build_title_section(self, ctx):
        pass

    @abstractmethod
    def build_filter_section(self, ctx):
        pass

    @abstractmethod
    def get_result(self, ctx):
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
        section += f'\nTitle: {ctx.name} Report'
        section += f'\nDate: {datetime.datetime.now()}\n'
        self._report.add(section)

    def build_filter_section(self, ctx):
        section = self.__header()
        name = ctx.__class__.__name__.split('Filter')[0]
        section += f'\nFilter: {name}'
        section += f'\nOptions: {ctx.options}\n'
        section += f'Results: {ctx.results}\n'
        self._report.add(section)

    def get_result(self, ctx):
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
        self.builder = None
        self.ctx = None

    def __set_builder(self, builder: Builder):
        self.builder = builder

    def __set_context(self, ctx):
        self.ctx = ctx

    def construct(self):
        self.builder.build_title_section(self.ctx)
        for x in self.ctx:
            self.builder.build_filter_section(self.ctx)
