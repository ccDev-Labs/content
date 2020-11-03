import pytest
import os
import json
import shutil
from tempfile import mkdtemp

from Tests.Marketplace.marketplace_services import GCPConfig
from Tests.Marketplace.copy_and_upload_packs import FAILED_PACKS_PATH_SUFFIX


# disable-secrets-detection-start
class TestGetPackNames:
    @pytest.mark.parametrize("packs_names_input, expected_result", [
        ("pack1,pack2,pack1", {"pack1", "pack2"}),
        ("pack1, pack2,  pack3", {"pack1", "pack2", "pack3"})
    ])
    def test_get_packs_names_specific(self, packs_names_input, expected_result):
        from Tests.Marketplace.copy_and_upload_packs import get_pack_names
        modified_packs = get_pack_names(packs_names_input)

        assert modified_packs == expected_result
# disable-secrets-detection-end


class TestHelperFunctions:
    def test_load_failed_packs_file(self):
        from Tests.Marketplace.copy_and_upload_packs import load_failed_packs_file
        tempdir = mkdtemp()
        failed_packs_file = os.path.join(tempdir, FAILED_PACKS_PATH_SUFFIX)

        # assert path not exist
        assert load_failed_packs_file(failed_packs_file) == {}

        # assert empty file
        with open(failed_packs_file, "w") as f:
            f.write('')
        assert load_failed_packs_file(failed_packs_file) == {}

        # assert valid file
        with open(failed_packs_file, "w") as f:
            f.write(json.dumps({"a": 1}))
        assert load_failed_packs_file(failed_packs_file) == {"a": 1}

        try:
            shutil.rmtree(tempdir)
        except shutil.Error:
            pass


class TestRegex:
    BUILD_BASE_PATH = f"{GCPConfig.GCS_PUBLIC_URL}/{GCPConfig.CI_BUILD_BUCKET}/content/builds"
    BUILD_PATTERN = "upload-packs-build-flow/169013/content/packs"

    @pytest.mark.parametrize("gcs_path, latest_zip_suffix", [
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonWidgets/1.0.5/CommonWidgets.zip",
         "CommonWidgets/1.0.5/CommonWidgets.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/Malware/1.2.4/Malware.zip",
         "Malware/1.2.4/Malware.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/HelloWorld/1.1.11/HelloWorld.zip",
         "HelloWorld/1.1.11/HelloWorld.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonDashboards/1.0.0/CommonDashboards.zip",
         "CommonDashboards/1.0.0/CommonDashboards.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/AutoFocus/1.1.9/AutoFocus.zip",
         "AutoFocus/1.1.9/AutoFocus.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/UrlScan/1.0.5/UrlScan.zip",
         "UrlScan/1.0.5/UrlScan.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/AccessInvestigation/1.2.2/AccessInvestigation.zip",
         "AccessInvestigation/1.2.2/AccessInvestigation.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/Phishing/1.10.7/Phishing.zip",
         "Phishing/1.10.7/Phishing.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/FeedTAXII/1.0.5/FeedTAXII.zip",
         "FeedTAXII/1.0.5/FeedTAXII.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/WhereIsTheEgg/1.0.0/WhereIsTheEgg.zip",
         "WhereIsTheEgg/1.0.0/WhereIsTheEgg.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/TIM_Processing/1.1.6/TIM_Processing.zip",
         "TIM_Processing/1.1.6/TIM_Processing.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/DemistoRESTAPI/1.1.2/DemistoRESTAPI.zip",
         "DemistoRESTAPI/1.1.2/DemistoRESTAPI.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonPlaybooks/1.8.5/CommonPlaybooks.zip",
         "CommonPlaybooks/1.8.5/CommonPlaybooks.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/Base/1.3.24/Base.zip",
         "Base/1.3.24/Base.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/rasterize/1.0.4/rasterize.zip",
         "rasterize/1.0.4/rasterize.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/VirusTotal/1.0.1/VirusTotal.zip",
         "VirusTotal/1.0.1/VirusTotal.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/DemistoLocking/1.0.0/DemistoLocking.zip",
         "DemistoLocking/1.0.0/DemistoLocking.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/TIM_SIEM/1.0.3/TIM_SIEM.zip",
         "TIM_SIEM/1.0.3/TIM_SIEM.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/ExportIndicators/1.0.0/ExportIndicators.zip",
         "ExportIndicators/1.0.0/ExportIndicators.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/DefaultPlaybook/1.0.2/DefaultPlaybook.zip",
         "DefaultPlaybook/1.0.2/DefaultPlaybook.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonTypes/2.2.1/CommonTypes.zip",
         "CommonTypes/2.2.1/CommonTypes.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/ImageOCR/1.0.1/ImageOCR.zip",
         "ImageOCR/1.0.1/ImageOCR.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonScripts/1.2.69/CommonScripts.zip",
         "CommonScripts/1.2.69/CommonScripts.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/Active_Directory_Query/1.0.7/Active_Directory_Query.zip",
         "Active_Directory_Query/1.0.7/Active_Directory_Query.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/CommonReports/1.0.1/CommonReports.zip",
         "CommonReports/1.0.1/CommonReports.zip"),
        (f"{BUILD_BASE_PATH}/{BUILD_PATTERN}/Whois/1.1.6/Whois.zip",
         "Whois/1.1.6/Whois.zip"),
        (f"{GCPConfig.GCS_PUBLIC_URL}/oproxy-dev.appspot.com/wow/content/packs/TIM-wow_a/99.98.99/TIM-wow_a.zip",
         "TIM-wow_a/99.98.99/TIM-wow_a.zip")
    ])
    def test_latest_zip_regex(self, gcs_path, latest_zip_suffix):
        from Tests.Marketplace.copy_and_upload_packs import LATEST_ZIP_REGEX
        assert LATEST_ZIP_REGEX.findall(gcs_path)[0] == latest_zip_suffix