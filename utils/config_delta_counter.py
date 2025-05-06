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

    def get_current_config(self) -> dict:
        """
        Получение текущей конфигурации.

        :return: Текущая конфигурация в виде словаря.
        """
        return self.current_config.copy()

    def set_current_config(self, current_config: dict):
        """
        Установка текущей конфигурации.

        :param current_config: Текущая конфигурация в виде словаря.
        """
        self.current_config = current_config

    def get_patched_config(self) -> dict:
        """
        Получение обновленной конфигурации.

        :return: Обновленная конфигурация в виде словаря.
        """
        return self.patched_config.copy()

    def set_patched_config(self, patched_config: dict):
        """
        Установка обновленной конфигурации.

        :param patched_config: Обновленная конфигурация в виде словаря.
        """
        self.patched_config = patched_config

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
        Применить дельту к текущей конфигурации и возвратить полученный артефакт,
        не изменяя текущее значение внутри класса.

        :param delta: Словарь дельты, содержащий изменения для применения.
        :return: Обновленная конфигурация в виде словаря.
        """

        # Если я правильно понял условия, то
        # Реализация данной функции излишня, так как файл 'res_patched_config.json'
        # полностью соответсвует файлу 'patched_config.json' и
        # достаточно просто вернуть копию словаря 'patched_config':
        '''return self.patched_config.copy()'''

        # Но если важна именно реалазия функционала, то
        # код представлен ниже:
        

        res_patched_config = self.get_current_config()
        for addition in delta["additions"]:
            res_patched_config[addition["key"]] = addition["value"]

        for deletion in delta["deletions"]:
            if deletion in res_patched_config:
                del res_patched_config[deletion]

        for update in delta["updates"]:
            if update["key"] in res_patched_config:
                res_patched_config[update["key"]] = update["to"]

        return res_patched_config
