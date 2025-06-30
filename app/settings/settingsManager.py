import os
import shutil
import yaml
from types import SimpleNamespace

class SettingsManager:
    def __init__(self, settings_file='settings.yml'):
        self.settings_file = os.path.abspath(settings_file)
        self.backup_file = self.settings_file + '.bak'
        self._ensure_backup()
        self._load_settings()

    def _ensure_backup(self):
        if not os.path.exists(self.backup_file):
            shutil.copy2(self.settings_file, self.backup_file)

    def _load_settings(self):
        with open(self.settings_file, 'r') as f:
            data = yaml.safe_load(f)
        self.settings = self._dict_to_namespace(data)

    def _dict_to_namespace(self, d):
        if isinstance(d, dict):
            return SimpleNamespace(**{k: self._dict_to_namespace(v) for k, v in d.items()})
        if isinstance(d, list):
            return [self._dict_to_namespace(i) for i in d]
        return d

    def _namespace_to_dict(self, ns):
        if isinstance(ns, SimpleNamespace):
            return {k: self._namespace_to_dict(v) for k, v in vars(ns).items()}
        if isinstance(ns, list):
            return [self._namespace_to_dict(i) for i in ns]
        return ns

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            yaml.safe_dump(self._namespace_to_dict(self.settings), f)

    def reload(self):
        self._load_settings()

    def restore_defaults(self):
        shutil.copy2(self.backup_file, self.settings_file)
        self.reload()

    def __getattr__(self, item):
        return getattr(self.settings, item)
    

settings = SettingsManager('app/settings/settings.yml')
