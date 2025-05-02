class ConfigDeltaCounter:
    """
    Класс для поиска изменений в конфигурационном файле.
    """

    def __init__(self, current_config: dict = None, patched_config: dict = None):
        """
        Инициализация ConfigDeltaCounter с конфигурационным файлом.

        :param current_config: Текущая конфигурация в виде словаря.
        :param patched_config: Исправленная конфигурация в виде словаря.
        """
        if current_config is None:
            current_config = {}
        if patched_config is None:
            patched_config = {}
        self.current_config = current_config
        self.patched_config = patched_config

    @property
    def delta(self):
        return {
            "additions": [],
            "deletions": [],
            "updates": []
        }

    def compare_configs(self) -> dict:
        """
        Сравнение предыдущей и текущей конфигураций и подсчет изменений.
        """
        delta = self.delta
        proceseed_keys = set()
        for key in self.patched_config:
            if key in self.current_config:
                if self.current_config[key] != self.patched_config[key]:
                    delta["updates"].append({"key": key,
                                             "from": self.current_config[key],
                                             "to": self.patched_config[key]})
            else:
                delta["additions"].append({"key": key,
                                           "value": self.patched_config[key]})
            proceseed_keys.add(key)

        for key in set(self.current_config.keys()) - proceseed_keys:
            delta["deletions"].append(key)
        delta["deletions"].sort()
        return delta

    def get_applied_delta(self, delta: dict) -> dict:
        """
        Применить дельту к текущей конфигурации.

        :param delta: Словарь дельты, содержащий изменения для применения.
        :return: Обновленная конфигурация в виде словаря.
        """

        return self.patched_config.copy()
