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
    
    def as_flat_dict(self):
        """Return settings as a flat dict for form rendering."""
        def flatten(ns, prefix=''):
            items = {}
            for k, v in vars(ns).items():
                if isinstance(v, SimpleNamespace):
                    items.update(flatten(v, f"{prefix}{k}_"))
                else:
                    items[f"{prefix}{k}"] = v
            return items
        return flatten(self.settings)

    def update_from_dict(self, d):
        """Update settings from a nested dict (including lists)."""
        def set_nested(ns, key, value):
            if isinstance(value, list):
                setattr(ns, key, value)
            elif isinstance(value, dict):
                for k, v in value.items():
                    set_nested(getattr(ns, key), k, v)
            else:
                setattr(ns, key, value)
        for k, v in d.items():
            if hasattr(self.settings, k):
                set_nested(self.settings, k, v)
        self.save_settings()
    
    def as_nested_dict(self):
        return self._namespace_to_dict(self.settings)

settingsManager = SettingsManager('app/settings/settings.yml')
