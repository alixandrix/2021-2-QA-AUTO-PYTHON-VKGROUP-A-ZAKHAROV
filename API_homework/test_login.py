from base import ApiBase
from ui.fixtures import *


class TestSegment(ApiBase):

    @pytest.mark.API
    def test_segment_creator(self, create_name):
        self.api_client.post_segment_create(create_name)
        segm_id = self.api_client.get_segment_id(create_name)
        assert segm_id
        self.api_client.delete_segment_id(segm_id)

    @pytest.mark.API
    def test_segment_deleter(self, create_name):
        segm_id = self.api_client.post_segment_create(create_name)
        self.api_client.delete_segment_id(segm_id)
        assert self.api_client.get_segment_id(create_name) is None


class TestCampaign(ApiBase):

    @pytest.mark.API
    def test_campaign_create(self, create_name, temp_dir):
        c_id = self.api_client.post_create_campaign(create_name, temp_dir)
        assert self.api_client.get_campaign_id(c_id) == c_id
        self.api_client.post_delete_campaign(c_id)
