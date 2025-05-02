from json import load, dump
from xml.etree.ElementTree import parse, Element, ElementTree, indent


class FileManager:

    @staticmethod
    def read_xml(path: str) -> Element:
        """
        Прочитать XML файл и вернуть его содержимое в виде элемента.

        :param path: Путь к XML файлу.
        :return: Элемент, содержащий данные XML.
        """
        tree = parse(path)
        XMI = tree.getroot()
        return XMI

    @staticmethod
    def read_json(path: str) -> dict:
        """
        Прочитать JSON файл и вернуть его содержимое в виде словаря.

        :param path: Путь к JSON файлу.
        :return: Словарь, содержащий данные JSON.
        """
        with open(path, 'r') as file:
            data = load(file)
        return data

    @staticmethod
    def write_xml(output_path: str, xml: ElementTree):
        """
        Записать словарь в XML файл.

        :param output_path: Путь к XML файлу для записи.
        :param xml_dict: Словарь, который будет записан в XML файл.
        """

        with open(output_path, 'wb') as file:
            indent(xml, space="\t", level=0)
            xml.write(file, encoding='utf-8', method='xml', xml_declaration=False,
                      short_empty_elements=False)

    @staticmethod
    def write_json(output_path: str, json_dict: dict):
        """
        Записать словарь в JSON файл.

        :param output_path: Путь к JSON файлу для записи.
        :param json_dict: Словарь, который будет записан в JSON файл.
        """
        with open(output_path, 'w', encoding='utf-8') as file:
            dump(json_dict, file, indent=4, sort_keys=True, ensure_ascii=True)
