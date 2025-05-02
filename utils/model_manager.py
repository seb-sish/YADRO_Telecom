from xml.etree.ElementTree import ElementTree, Element, ParseError
from data import Node, Node_Attribute, Aggr_Multi


class XmlMamanger:
    """
    Класс для работы с UML-моделью в формате XMI (UML 1.3).
    
    :param xml: Элемент XML, представляющий корневой элемент XMI.
    """
    validated_tree = None

    def __init__(self, xml: Element):
        self.raw_xml = xml

    def validate(self) -> set[Node] | bool:
        """
        Проверить структуру XML.

        :return: Проверенная 'Node' структура или False в случае ошибки.
        """

        try:
            if self.raw_xml.tag != "XMI":
                raise ParseError("Root element must be 'XMI'")

            classes = self.raw_xml.findall("Class")
            if not classes:
                raise ParseError("No 'Class' elements found")
            try:
                classes = {c.attrib["name"]: Node(**c.attrib,
                                                attributes=[Node_Attribute(**attr.attrib) for attr in c.findall("Attribute")])
                        for c in classes}
            except (TypeError, KeyError) as e:
                raise ParseError(f"Missing attribute in class: {e}")

            aggregations = self.raw_xml.findall("Aggregation")
            if not aggregations:
                raise ParseError("No 'Aggregation' elements found")

            def get_root(classes: dict[str, Node]) -> Node:
                for cl in classes.values():
                    if cl.isRoot:
                        return cl
                return None

            root = get_root(classes)
            if not root:
                raise ParseError("No root class found")

            for a in aggregations:
                try:
                    source = classes.get(a.attrib["source"])
                    target = classes.get(a.attrib["target"])
                    if not source or not target:
                        raise ParseError(
                            f"Invalid aggregation: {a.attrib['source']} -> {a.attrib['target']}")
                    target.add_child(source)
                    source.set_parent(target, Aggr_Multi(
                        a.attrib["sourceMultiplicity"]))

                except KeyError as e:
                    raise ParseError(
                        f"Missing attribute in aggregation '{a.attrib['source']} -> {a.attrib['target']}': {e}")
            self.validated_tree = root
            return self.validated_tree

        except ParseError as e:
            print(f"XML validation error: {e}")
            return False

    def generate_config_xml(self) -> ElementTree:
        """
        Сгенерировать ElementTree из проверенной структуры XML.

        :return: Представление XML в виде ElementTree.
        """
        root = Element(self.validated_tree.name)
        for attr in self.validated_tree.attributes:
            attr_elem = Element(attr.name)
            attr_elem.text = attr.type
            root.append(attr_elem)

        def add_children(parent: Element, children: list[Node]):
            if not children:
                return
            for child in children:
                child_elem = Element(child.name)
                for attr in child.attributes:
                    attr_elem = Element(attr.name)
                    attr_elem.text = attr.type
                    child_elem.append(attr_elem)
                parent.append(child_elem)
                add_children(child_elem, child.children)

        add_children(root, self.validated_tree.children)
        return ElementTree(root)

    def generate_meta_json(self) -> dict:
        """
        Сгенерировать JSON представление структуры XML.

        :return: JSON представление XML.
        """
        meta = []

        def parse_node(parent: Node, meta: list[dict]):
            info = {
                "class": parent.name,
                "documentation": parent.documentation,
                "isRoot": parent.isRoot,
                "parameters": [{"name": attr.name, "type": attr.type} for attr in parent.attributes] +
                [{"name": child.name, "type": "class"}
                    for child in parent.children]
            }
            if parent.multiplicity:
                info["max"] = str(parent.multiplicity.max)
                info["min"] = str(parent.multiplicity.min)
            meta.append(info)
            for child in parent.children:
                parse_node(child, meta)

        parse_node(self.validated_tree, meta)
        return meta
