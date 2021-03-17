import requests


class TRMHelper:

    @staticmethod
    def convert_usd_to_cop(usd_money: float) -> float:

        current_trm = 'https://trm-colombia.vercel.app/?date=2021-03-17'
        response = requests.get(current_trm)
        data = response.json().get('data')
        return data['value'] * usd_money
