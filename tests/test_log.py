"""Test the log on a real life squid sample."""

import re
from ..logrdis.log import find_match

SAMPLES="""time 2017-10-22_18:20:05+0000 time_response 60 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.228:443 user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type -\n'b'time 2017-10-22_18:20:06+0000 time_response 135 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TCP_MISS http_status_code 200 http_reply_size 69919 http_request_method GET http_request_url https://www.google.com/ user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type text/html\n'b'time 2017-10-22_18:20:06+0000 time_response 5 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.227:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -\n'b'time 2017-10-22_18:20:06+0000 time_response 1 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.227:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -\ntime 2017-10-22_18:20:06+0000 time_response 0 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.227:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -\n'b'time 2017-10-22_18:20:06+0000 time_response 42 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TCP_MISS http_status_code 204 http_reply_size 374 http_request_method POST http_request_url https://www.google.com/gen_204? user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type text/html\n'b'time 2017-10-22_18:20:06+0000 time_response 1 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.7.131:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -\n'b'time 2017-10-22_18:20:06+0000 time_response 3 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.7.131:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -\ntime 2017-10-22_18:20:06+0000 time_response 0 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.7.131:443 user_name - squid_hier_code HIER_NONE ip_destination - http_content_type -"""

def test_find_match(test_yaml):
    """Test that find_match returns the expected entries."""
    cfg = test_yaml()

    for sample in SAMPLES.split('\n'):
        tablename, match = find_match(sample, cfg)

        assert tablename == "access_logs", "Invalid table matched"
        assert re.search("[\d\-\:\+]+", match.group("time"))
        assert re.search("\d+", match.group("time_response"))
        assert re.search("[\d\:\-]+", match.group("mac_source"))
        assert re.search("[\d\.\-]+", match.group("ip_source"))
        assert re.search("[\d\.\-]+", match.group("http_request_url"))
        assert re.search("[\d\.\-]+", match.group("ip_destination"))
