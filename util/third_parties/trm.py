import requests

from settings import third_party_settings


class TRMHelper:

    @staticmethod
    def convert_usd_to_cop(usd_money: float) -> float:

        current_trm = third_party_settings.trm_api
        response = requests.get(current_trm)
        data = response.json().get('USDCOL')
        return data['ratetrm'] * usd_money
