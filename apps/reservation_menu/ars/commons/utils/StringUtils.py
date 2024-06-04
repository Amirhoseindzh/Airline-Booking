class StringUtils(object):

    @classmethod
    def is_blank(cls, str_):

        return str_ is None or len(str_.strip()) == 0
