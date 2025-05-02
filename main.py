from utils import FileManager as FM
from utils import ConfigDeltaCounter
from utils import XmlMamanger


def main():
    model_configure()
    config_delta()


def model_configure():
    xml_model = FM.read_xml("./input/model_input.xml")
    xmlm = XmlMamanger(xml_model)
    r = xmlm.validate()
    if not r:return

    xml_config = xmlm.generate_config_xml()
    FM.write_xml("./out/config.xml", xml_config)
    print("XML model file created successfully.")

    json_config = xmlm.generate_meta_json()
    FM.write_json("./out/meta.json", json_config)
    print("Meta JSON file created successfully.")


def config_delta():
    json_config = FM.read_json("./input/config.json")
    patched_json_config = FM.read_json("./input/patched_config.json")

    CDC = ConfigDeltaCounter(json_config, patched_json_config)
    delta = CDC.compare_configs()
    FM.write_json("./out/delta.json", delta)
    print("Delta JSON file created successfully.")

    applied_delta = CDC.get_applied_delta(delta)
    FM.write_json("./out/res_patched_config.json", applied_delta)
    print("Patched JSON file created successfully.")


if __name__ == "__main__":
    main()
