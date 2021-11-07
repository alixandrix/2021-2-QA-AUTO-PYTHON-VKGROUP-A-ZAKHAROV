def post_segment_create_json(name):
    return {"name": name,
            "pass_condition": 1,
            "relations": [{"object_type": "remarketing_player",
                           "params": {"type": "positive",
                                      "left": 365,
                                      "right": 0}}],
            "logicType": "or"}


def post_create_campaign_json(name_campaign, url_id, image_id, false=False, null=None, true=True):
    return {
        "name": name_campaign,
        "read_only": false,
        "conversion_funnel_id": null,
        "objective": "traffic",
        "enable_offline_goals": false,
        "targetings": {
            "split_audience": [
                1,
                2,
            ],
            "sex": [
                "male",
                "female"
            ],
            "age": {
                "age_list": [
                    0,
                    12,
                    13,
                    14,
                    15

                ],
                "expand": true
            },
            "geo": {
                "regions": [
                    188
                ]
            },
            "interests_soc_dem": [],
            "segments": [],
            "interests": [],
            "fulltime": {
                "flags": [
                    "use_holidays_moving",
                    "cross_timezone"
                ],
                "mon": [
                    0,
                    1,
                    2,
                    3
                ],
                "tue": [
                    0,
                    1,
                    2,
                    3,
                    4
                ],
                "wed": [
                    0,
                    1,
                    2,
                    3
                ],
                "thu": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                ],
                "fri": [
                    0,
                    1,
                    2,
                    3,
                    4
                ],
                "sat": [
                    0,
                    1,
                    2,
                    3,
                    4
                ],
                "sun": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6
                ]
            },
            "pads": [
                102643
            ],
            "mobile_types": [
                "tablets",
                "smartphones"
            ],
            "mobile_vendors": [],
            "mobile_operators": []
        },
        "age_restrictions": null,
        "date_start": null,
        "date_end": null,
        "autobidding_mode": "second_price_mean",
        "budget_limit_day": null,
        "budget_limit": null,
        "mixing": "fastest",
        "utm": null,
        "enable_utm": true,
        "price": "3.53",
        "max_price": "0",
        "package_id": 961,
        "banners": [
            {
                "urls": {
                    "primary": {
                        "id": url_id
                    }
                },
                "textblocks": {},
                "content": {
                    "image_240x400": {
                        "id": image_id
                    }
                },
                "name": ""
            }
        ]
    }
