import threading
import requests
from typing import List
from requests.exceptions import RequestException


class OpenProxy:
    """
    Collect free proxies from https://proxyscrape.com API and filter
    valid proxies with the help of http://ipinfo.io/json.
        Attributes:
            - country_list(List[str]) : Contain ISO 3166 country codes.
            - protocol_list(List[str]) : Contain supported protocols.
            - anonymity_list(List[str]) : Contain supported anonymity levels.
    """
    def __init__(self):
        self.country_list = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT',
                             'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI',
                             'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY',
                             'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
                             'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM',
                             'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK',
                             'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL',
                             'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM',
                             'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR',
                             'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN',
                             'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
                             'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK',
                             'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW',
                             'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP',
                             'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM',
                             'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW',
                             'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM',
                             'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF',
                             'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW',
                             'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI',
                             'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW']
        self.protocol_list = ['http', 'socks4', 'socks5']
        self.anonymity_list = ['elite', 'anonymous', 'transparent']

    def __check_country(self, country: str) -> bool:
        """
        Check whether the given `country` exist in the `country_list`.
        :param country: The ISO 3166 country code. Eg : 'IN', 'US'..
        :return: True if the `country` exist in the `country_list`.
        Otherwise, raise ValueError.
        """
        if country not in self.country_list:
            raise ValueError('The given country code is invalid.')
        else:
            return True

    def __check_protocol(self, protocol: str) -> bool:
        """
        Check if the `protocol` exist in the `protocol_list`.
        :param protocol: The supported protocol [http, socks4, socks5].
        :return: True if the `protocol` exist in the `protocol_list`.
        Otherwise, raise ValueError.
        """
        if protocol not in self.protocol_list:
            raise ValueError('The given protocol is invalid.')
        else:
            return True

    def __check_anonymity_level(self, anonymity_level: str) -> bool:
        """
        Check if the `anonymity_level` exist in the `anonymity_list`.
        :param anonymity_level: The different level of anonymity [elite, transparent, anonymous].
        :return: True if the `anonymity_level` exist in the `anonymity_list`.
        Otherwise, raise ValueError.
        """
        if anonymity_level not in self.anonymity_list:
            raise ValueError('The given anonymity is invalid.')
        else:
            return True

    @staticmethod
    def __get_addresses(url: str) -> None:
        """
        Make a get request to the given `url` and call the `__filter_proxy_addresses`
        to filter the working proxy from the available proxies in the url.
        :param url: https://proxyscrape.com API url.
        """
        output: List[str] = []
        try:
            response = requests.get(url)
            output = response.text.split('\n')
        except RequestException:
            pass
        return OpenProxy.__filter_proxy_addresses(output)

    @staticmethod
    def __filter_proxy_addresses(proxies: List[str]) -> None:
        """
        This method uses http://ipinfo.io/json to filter the working proxies
        using multithreading to reduce the waiting time for the user.
        :param proxies: Contain both dead and working proxies from all around the world.
        """
        for address in proxies:
            address = address[:-1]

            # Function to make the request.
            def make_request(proxy: str):
                # Make a request to ensure that the proxy is working.
                try:
                    response = requests.get('http://ipinfo.io/json',
                                            proxies={
                                                'http': proxy,
                                                'https': proxy
                                            })
                    if response.status_code == 200:
                        print(proxy)
                except RequestException:
                    pass

            # Start a new thread
            thread = threading.Thread(target=make_request, args=[address])
            thread.start()

    def proxies_random(self) -> None:
        """
        Print random working proxies around the world.
        - Country: All
        - protocol: All
        - anonymity level: All
        """
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10000&country=all&ssl=all" \
              "&anonymity=all"
        return self.__get_addresses(url)

    def proxies_country(self, country: str) -> None:
        """
        Print the working proxies form the specified `country`.
        :param country: The ISO 3166 country code. Eg. 'IN', 'US'..
        - Country: `country`
        - protocol: All
        - anonymity level: All
        """
        # Check if the `country` is valid.
        if self.__check_country(country):
            url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=" \
                  f"{country}&ssl=all&anonymity=all"
            return self.__get_addresses(url)

    def proxies_protocol(self, protocol: str) -> None:
        """
        Print all working proxies filter by the specified `protocol`.
        :param protocol: The supported protocols [http, socks4, socks5].
        - Country: All
        - protocol: `protocol`
        - anonymity level: All
        """
        # Check if the `protocol` is valid. Otherwise, raise value error.
        if self.__check_protocol(protocol):
            url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country" \
                  f"=all&ssl=all&anonymity=all"
            return self.__get_addresses(url)

    def proxies_anonymity(self, anonymity_level: str) -> None:
        """
        Print all the working proxies filtered by `anonymity_level`.
        :param anonymity_level: The supported anonymity levels [elite, anonymous, transparent].
        - Country: All
        - protocol: All
        - anonymity level: `anonymity_level`.
        """
        if self.__check_anonymity_level(anonymity_level):
            url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all" \
                  f"&ssl=all&anonymity={anonymity_level}"
            return self.__get_addresses(url)

    def proxies_custom(self, country: str, protocol: str, anonymity_level: str) -> None:
        """
        Print all working proxies filtered by the specified country, protocol, anonymity_level.
        :param country: The ISO 3166 country code.
        :param protocol: The supported protocols [http, socks4, socks5].
        :param anonymity_level: The supported anonymity level.
        - Country: `country`.
        - protocol: `protocol`.
        - anonymity level: `anonymity_level`.
        """
        if self.__check_country(country) and self.__check_protocol(protocol) and \
                self.__check_anonymity_level(anonymity_level):
            url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country" \
                  f"={country}&ssl=all&anonymity={anonymity_level}"

            return self.__get_addresses(url)


if __name__ == '__main__':
    op = OpenProxy()
    op.proxies_random()
