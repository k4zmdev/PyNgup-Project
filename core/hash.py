# ngup/hash.py

import requests

MALWARE_BAZAAR_API_URL = "https://bazaar.abuse.ch/api/v1/file/"

def get_info_from_hash(hash_value):
    url = MALWARE_BAZAAR_API_URL + f"lookup/hash/{hash_value}/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"status": "error", "data": "Erreur lors de la connexion à Malware Bazaar."}
        data = response.json()
        if data.get("data"):
            result = data["data"][0]
            if result.get("malware"):
                return {"status": "malware", "data": result}
            else:
                return {"status": "clean", "data": "Ce hash n'est pas associé à un malware."}
        else:
            return {"status": "not_found", "data": "Aucune information trouvée pour ce hash."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "data": str(e)}
