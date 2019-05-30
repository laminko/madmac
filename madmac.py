import random
import re


def format_hexstr(value, delimiter=':'):
    '''
    Format hex string.

    :param value:
    :param delimiter:
    :return:
    '''
    return delimiter.join(
        ['{}{}'.format(a, b) for a, b in zip(value[::2], value[1::2])])


def int_to_hexstr(value, _format='{:06x}'):
    '''
    Convert int to hex string.

    :param value:
    :param _format:
    :return:
    '''
    if not isinstance(value, int):
        raise ValueError('Required int.')
    return _format.format(value)


def hexstr_to_int(value, base=16):
    '''
    Convert hex string to int.

    :param value:
    :param base:
    :return:
    '''
    return int(value, base=base)


def normalize_oui(oui, delimiter=':'):
    '''
    Normalize OUI by using delimiter.

    :param oui:
    :param delimiter:
    :return:
    '''
    pattern = re.compile('[\W_]+')
    cleaned = pattern.sub('', oui)
    return format_hexstr(cleaned, delimiter=delimiter)


class MacGenerator(object):
    '''
    MAC Address generator class.
    '''

    def __init__(self):
        self.case_handler = lambda value, case: getattr(value, case)()

    def generate(self, oui=None, start=None, stop=None, delimiter=':', case='lower'):
        '''
        Generate MAC address.

        :param oui:
        :param start:
        :param stop:
        :param delimiter:
        :param case:
        :return:
        '''
        if not oui:
            oui = int_to_hexstr(random.randint(0, 256))
        oui = normalize_oui(oui, delimiter=delimiter)
        if not start:
            start = 1
        if not stop:
            stop = 100

        for each in range(start, stop):
            dev_id = format_hexstr(int_to_hexstr(each), delimiter=delimiter)
            generated_mac = '{oui}{delimiter}{dev}'.format(
                oui=oui,
                delimiter=delimiter,
                dev=dev_id
            )
            yield self.case_handler(generated_mac, case=case)


def main():
    macg = MacGenerator()
    macs = macg.generate(oui='ab-cd-ef', delimiter='-', case='upper')
    from pprint import pprint
    pprint(list(macs))


if __name__ == '__main__':
    main()