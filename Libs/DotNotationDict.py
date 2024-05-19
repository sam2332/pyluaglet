import json
from collections import UserDict

class DotNotationDict(UserDict):
    def __getattr__(self, item):
        if item in self.data:
            value = self.data[item]
            if isinstance(value, dict):
                return DotNotationDict(value)
            return value
        raise AttributeError(f"'DotNotationDict' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key == 'data':
            super().__setattr__(key, value)
        else:
            self.data[key] = DotNotationDict(value) if isinstance(value, dict) else value

    def __delattr__(self, item):
        if item in self.data:
            del self.data[item]
        else:
            raise AttributeError(f"'DotNotationDict' object has no attribute '{item}'")

    def __getitem__(self, key):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if k in value:
                value = value[k]
                if isinstance(value, dict):
                    value = DotNotationDict(value)
            else:
                raise KeyError(f"Key '{key}' not found in DotNotationDict")
        return value

    def __setitem__(self, key, value):
        keys = key.split('.')
        d = self.data
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
            if isinstance(d, dict):
                d = DotNotationDict(d)
        d[keys[-1]] = DotNotationDict(value) if isinstance(value, dict) else value

    def get(self, item, default=None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def to_dict(self):
        return {key: (value.to_dict() if isinstance(value, DotNotationDict) else value)
                for key, value in self.data.items()}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str):
        return DotNotationDict(json.loads(json_str))

if __name__ == '__main__':
    # Test cases
    data = DotNotationDict({'tiles': {'player': {'up': 'value_up', 'down': 'value_down'}}})
    assert data.tiles.player.up == 'value_up'
    assert data.tiles.player.down == 'value_down'
    assert data['tiles.player.up'] == 'value_up'
    assert data.get('tiles.player.up') == 'value_up'
    assert data.get('tiles.player.down') == 'value_down'
    assert data.get('tiles.player.left') is None
    data.tiles.player.left = 'value_left'
    assert data.get('tiles.player.left') == 'value_left'
    assert data.to_dict() == {'tiles': {'player': {'up': 'value_up', 'down': 'value_down', 'left': 'value_left'}}}
    assert data.to_json() == '{"tiles": {"player": {"up": "value_up", "down": "value_down", "left": "value_left"}}}'
