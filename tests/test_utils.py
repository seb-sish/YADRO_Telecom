import unittest
from xml.etree.ElementTree import Element
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.model_manager import XmlMamanger
from utils.config_delta_counter import ConfigDeltaCounter
from data import Node, Node_Attribute, Aggr_Multi


class TestConfigDeltaCounter(unittest.TestCase):
    def setUp(self):
        self.current = {'a': 1, 'b': 2, 'c': 3}
        self.patched = {'a': 1, 'b': 20, 'd': 4}
        self.counter = ConfigDeltaCounter(self.current, self.patched)

    def test_compare_configs(self):
        delta = self.counter.compare_configs()
        self.assertEqual(delta['additions'], [{'key': 'd', 'value': 4}])
        self.assertEqual(delta['deletions'], ['c'])
        self.assertEqual(delta['updates'], [{'key': 'b', 'from': 2, 'to': 20}])

    def test_get_applied_delta(self):
        delta = self.counter.compare_configs()
        result = self.counter.get_applied_delta(delta)
        self.assertEqual(result, {'a': 1, 'b': 20, 'd': 4})

    def test_empty_configs(self):
        cdc = ConfigDeltaCounter()
        delta = cdc.compare_configs()
        self.assertEqual(
            delta, {'additions': [], 'deletions': [], 'updates': []})

    def test_setters(self):
        cdc = ConfigDeltaCounter()
        cdc.set_current_config({'x': 1})
        cdc.set_patched_config({'x': 2, 'y': 3})
        self.assertEqual(cdc.get_current_config(), {'x': 1})
        self.assertEqual(cdc.get_patched_config(), {'x': 2, 'y': 3})


class TestXmlMamanger(unittest.TestCase):
    def setUp(self):
        # Минимальный корректный XML для теста
        self.xml = Element('XMI')
        class_elem = Element(
            'Class', {'name': 'BTS', 'isRoot': 'true', 'documentation': 'doc'})
        attr_elem = Element('Attribute', {'name': 'id', 'type': 'uint32'})
        attr_elem2 = Element('Attribute', {'name': 'name', 'type': 'string'})
        class_elem.append(attr_elem)
        class_elem.append(attr_elem2)

        class_elem2 = Element(
            'Class', {'name': 'MGMT', 'isRoot': 'false', 'documentation': 'Management related'})

        self.xml.append(class_elem)
        self.xml.append(class_elem2)

        aggr_elem = Element('Aggregation', {
                            'source': 'MGMT', 'target': 'BTS', 'sourceMultiplicity': '1', 'targetMultiplicity': '1'})
        self.xml.append(aggr_elem)
        self.manager = XmlMamanger(self.xml)

    def test_validate_success(self):
        result = self.manager.validate()
        self.assertIsInstance(result, Node)
        self.assertEqual(result.name, 'BTS')
        self.assertTrue(result.isRoot)
        self.assertEqual(len(result.attributes), 2)

    def test_validate_fail(self):
        # Создаем некорректный XML для теста
        broken_xml = Element('NotXMI')
        manager = XmlMamanger(broken_xml)
        self.assertFalse(manager.validate())

    def test_get_set_raw_xml(self):
        new_xml = Element('XMI')
        self.manager.set_raw_xml(new_xml)
        self.assertIs(self.manager.get_raw_xml(), new_xml)

    def test_generate_config_xml_and_meta_json(self):
        self.manager.validate()
        config_xml = self.manager.generate_config_xml()
        self.assertEqual(config_xml.getroot().tag, 'BTS')
        meta = self.manager.generate_meta_json()
        self.assertIsInstance(meta, list)
        self.assertEqual(meta[0]['class'], 'BTS')
        self.assertEqual(meta[0]['isRoot'], True)
        self.assertEqual(len(meta[0]['parameters']), 3)
        self.assertEqual(meta[0]['documentation'], 'doc')


if __name__ == '__main__':
    unittest.main()
