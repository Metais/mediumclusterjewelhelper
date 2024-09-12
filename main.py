from session import Session
from query import Query
from report import Report
import json
import time


# URL = 'https://www.pathofexile.com/trade/search/Affliction?q={"query":{"filters":{},"type":"Clear Oil"}}'
DIVINE_PRICE = 110


def fetch_offers(s, cj_type):
    q = Query()

    # Add the cluster jewel type filter
    cj_id = q.config_data["clusterjeweltypefilter"]["id"]
    cj_num = q.config_data["clusterjeweltypefilter"][cj_type]
    q.add_stats_filter(cj_id, {"option": cj_num})

    # Add the cluster jewel # passive skills filter
    cj_passiveskillnum_id = q.config_data["clusterjewelpassivecountfilter"]["id"]
    q.add_stats_filter(cj_passiveskillnum_id, {"value": {"min": 4, "max": 5}})

    notables = q.config_data[cj_type]["notables"]

    # create all unique pairs of notables
    pairs = []
    for i, notable in enumerate(notables):
        for nested_notable in notables[i + 1:]:
            pairs.append((notable, nested_notable))

    # Check for each pair of notables
    reports = []
    for i, pair in enumerate(pairs):
        print(f"Pair {i+1} of {len(pairs)}...")
        time.sleep(5)

        notable_code1 = q.config_data["notables"][pair[0]]
        notable_code2 = q.config_data["notables"][pair[1]]

        q.add_stats_filter(notable_code1)
        q.add_stats_filter(notable_code2)

        response_offers = s.session.post(s.baseURI, json=q.query)

        if not response_offers.ok:
            print("something went wrong: " + response_offers.reason)

        response_offers_json = json.loads(response_offers.content)

        # No orders on the market
        if len(response_offers_json["result"]) == 0:
            report = Report(pair, [], 0, DIVINE_PRICE)
        else:
            # Fetch the first 10 offers
            itemfetchURL = s.itemFetchURI + \
                           ','.join([x for x in response_offers_json['result'][:10]]) + \
                           "?query=" + response_offers_json['id']
            response_detailed = s.session.get(itemfetchURL)
            detailed_json = json.loads(response_detailed.content)

            prices = [result["listing"]["price"] for result in detailed_json["result"]]
            report = Report(pair, prices, response_offers_json["total"], DIVINE_PRICE)

        reports.append(report)

        # Remove the past two notables again
        q.query["query"]["stats"][0]["filters"] = q.query["query"]["stats"][0]["filters"][:2]

    # Sort the reports in descending average price
    sorted_reports = sorted(reports, key=lambda obj: obj.average_price)
    # Place the zero-price reports at the front (either unknown currencies only, or no offers at all!)
    sorted_reports = sorted(sorted_reports, key=lambda obj: obj.average_price == 0)

    for report in sorted_reports:
        delimiter = "\t\t" if report.average_price < 100 else "\t"
        print(f"{report}:\navg. price={report.average_price}{delimiter}|\tcheapest price={report.cheapest_price}\n" +
              f"total items: {report.total_items}\n")


s = Session()

print("Here are all the valid inputs: " +
      ", ".join([x for x in Query().config_data["clusterjeweltypefilter"].keys()][2:]))

toggle = True
while toggle:
    cj = input("Enter cluster jewel type:")

    fetch_offers(s, cj)
